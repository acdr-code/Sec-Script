from scapy.all import sniff, IP, UDP, TCP
import time
import datetime

#Sniffing
def SniffData(packet, delay, list):
    if not packet.haslayer(IP):
        return

    ipSrc = packet[IP].src
    ipDst = packet[IP].dst

    if packet.haslayer(TCP):
        portSrc = packet[TCP].sport
        portDst = packet[TCP].dport
        proto = "TCP"

    elif packet.haslayer(UDP):
        portSrc = packet[UDP].sport
        portDst = packet[UDP].dport
        proto = "UDP"

    else:
        portSrc = None
        portDst = None
        proto = packet[IP].proto

    list.append({
        "ts": time.time(),
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "src_ip": ipSrc,
        "src_port": portSrc,
        "dst_ip": ipDst,
        "dst_port": portDst,
        "proto": proto,
    })

    if delay > 0:
        time.sleep(delay)


def SniffRun(iface, count, filter, delay, list):
    if filter == "ALL":
        sniff(
            prn=lambda pkt: SniffData(packet=pkt, delay=delay, list=list),
            count=count,
            timeout=None,
            iface=iface,
        )
    else:
        sniff(
            prn=lambda pkt: SniffData(packet=pkt, delay=delay, list=list),
            count=count,
            timeout=None,
            iface=iface,
            filter=filter,
        )
