import socket
import os
import struct
from ctypes import *

#host que ouvira
host = "192.168.0.10"

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
        ("src", c_ulong),
        ("dst", c_ulong)]

def __new__(cls, socket_buffer=None):
    return cls.from_buffer_copy(socket_buffer)


def __init__(self, socket_buffer=None):

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

try:
    while True:
        # lê um pacote
        raw_buffer = sniffer.recvfrom(64435)[0]

        # cria um cabecalho IP a partir dos 20 primeiros bytes do buffer
        ip_header = IP(raw_buffer[:20])

        # exibe o protocolo detectado e os hosts
        print("Protocol: %s %s -> %s" % (ip_header.protocol,ip_header.src,ip_header.src_address,ip_header.dst_address))

#trata o CTRL-C
except KeyboardInterrupt:
    
    # se estivermos usando Windows, desabilita o modo promiscuo
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
