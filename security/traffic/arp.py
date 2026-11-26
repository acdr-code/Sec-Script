
from scapy.all import ARP, Ether, srp
from scapy.error import Scapy_Exception
from mac_vendor_lookup import MacLookup

from core.errorHandler import SecsRuntimeError, SecsTypeError, SecsArgumentError


def arpScannerLan(ip, iface, timeout):
    if not isinstance(ip, str) or not ip:
        raise SecsTypeError("IP must be a non-empty string")

    if not isinstance(iface, str) or not iface:
        raise SecsTypeError("Interface must be a non-empty string")

    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
        raise SecsTypeError("Timeout must be a number")

    if timeout <= 0:
        raise SecsArgumentError("Timeout must be positive")

    try:
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        maclookup = MacLookup()

        answered, unanswered = srp(packet, timeout=timeout, iface=iface, verbose=0)

    except (ValueError, OSError, Scapy_Exception) as e:
        raise SecsRuntimeError(f"ARP scan failed: {e}") from e

    results = []

    for sent, received in answered:
        deviceIp = received.psrc
        mac = received.hwsrc

        try:
            vendor = maclookup.lookup(mac)
        except KeyError:
            vendor = "unknown"

        results.append({
            "ip": deviceIp,
            "mac": mac,
            "vendor": vendor
        })

    return results
