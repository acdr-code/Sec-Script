
from scapy.all import sniff, IP, UDP, TCP
from scapy.error import Scapy_Exception
import time
import datetime

from core.errorHandler import SecsRuntimeError, SecsTypeError, SecsArgumentError


# Sniffing
def SniffData(packet, delay, result):
    if not isinstance(delay, (int, float)) or isinstance(delay, bool):
        raise SecsTypeError("Delay must be a number")

    if delay < 0:
        raise SecsArgumentError("Delay cannot be negative")

    if not isinstance(result, list):
        raise SecsTypeError("Packet storage must be a list")

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

    result.append({
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


def SniffRun(iface, count, filter, delay, result):
    if iface is not None and (not isinstance(iface, str) or not iface):
        raise SecsTypeError("Interface must be a non-empty string")

    if not isinstance(count, int) or isinstance(count, bool):
        raise SecsTypeError("Count must be an integer")

    if count < 0:
        raise SecsArgumentError("Count cannot be negative")

    if not isinstance(filter, str):
        raise SecsTypeError("Filter must be a string")

    if not isinstance(delay, (int, float)) or isinstance(delay, bool):
        raise SecsTypeError("Delay must be a number")

    if delay < 0:
        raise SecsArgumentError("Delay cannot be negative")

    if not isinstance(result, list):
        raise SecsTypeError("Packet storage must be a list")

    try:
        if filter == "ALL":
            sniff(prn=lambda pkt: SniffData(packet=pkt, delay=delay, result=result), count=count, timeout=None, iface=iface)
        else:
            sniff(prn=lambda pkt: SniffData(packet=pkt, delay=delay, result=result), count=count, timeout=None, iface=iface, filter=filter)

    except (Scapy_Exception, OSError, ValueError) as e:
        raise SecsRuntimeError(f"Packet sniffing failed: {e}") from e
