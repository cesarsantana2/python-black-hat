import socket
import os

#host que ouvira
host = "192.168.0.196"

#cria um socket puro e associa-o à interface pública
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host,0))

#queremos os cabeçalhos IP incluidos na captura
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#se estivermos usando Windows, deveremos enviar um IOCTL
#para configurar o modo promíscuo

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

#lê um único pacote
print(sniffer.recvfrom(65565))

#se estivermos usando Windows, desabilitará o modo promiscuo
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)