import socket
import os
import struct
import threading
from ipaddress import ip_address, ip_network
from ctypes import *

# host que ira ouvir
host = "192.168.0.10"

# subred que queremos ouvir
tgt_subnet = "192.168.0.0/24"

# vamos checar as respostas ICMP por essa mensagem
tgt_message = "PYTHONRULES!"

def udp_sender(sub_net, magic_message):
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in ip_network(sub_net).hosts():
        sender.sendto(magic_message.encode('utf-8'), (str(ip), 65212))


class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_uint32),
        ("dst", c_uint32)]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)


    def __init__(self, socket_buffer=None):
        self.socket_buffer = socket_buffer
        #mapeia constantes do protocolo aos seus nomes
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        #enderecos IP legíveis aos seres humanos
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))

        #protocolo legível aos seres humanos
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except IndexError:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)]
    
    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        self.socket_buffer = socket_buffer


#este código deve parecer familiar, pois foi visto no exemplo anterior
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# comeca a enviar pacotes
t = threading.Thread(target=udp_sender, args=(tgt_subnet, tgt_message))
t.start()

try:
    while True:
        # lê um pacote
        raw_buffer = sniffer.recvfrom(64435)[0]

        # cria um cabecalho IP a partir dos 20 primeiros bytes do buffer
        ip_header = IP(raw_buffer[0:20])

        # exibe o protocolo detectado e os hosts
        print("Protocol: %s %s -> %s" % (ip_header.protocol,ip_header.src_address,ip_header.dst_address))

        # se for ICMP, nos queremos o pacote
        if ip_header.protocol == "ICMP":
            # calcula em que ponto nosso pacote ICMP comeca
            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + sizeof(ICMP)]
            
            # cria nossa estrutura ICMP
            icmp_header = ICMP(buf)
            
            print("ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code))

            if icmp_header.code == 3 and icmp_header.type == 3:
                
                if ip_address(ip_header.src_address) in ip_network(tgt_subnet):

                    if raw_buffer[len(raw_buffer)- len(tgt_message):] == tgt_message:
                        
                        print("Host Up: %s" % ip_header.src_address)



#trata o CTRL-C
except KeyboardInterrupt:
    
    # se estivermos usando Windows, desabilita o modo promiscuo
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
