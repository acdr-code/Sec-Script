from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup

def arpScannerLan(ip, iface, timeout):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

    maclookup = MacLookup()

    answered, unanswered = srp(
        packet,
        timeout=timeout,
        iface=iface,
        verbose=0
    )

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

