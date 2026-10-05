import socket
import requests
from bs4 import BeautifulSoup
from scapy.all import sniff, IP, UDP, TCP
import time
import datetime
import paramiko
import hashlib, base64, binascii, urllib.parse
from errorHandler import SecScriptError
import dns.resolver

#portscan
def portScan(ip, port, timeout, list):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    if result == 0:
        list.append(port)
    sock.close()

#BetterBs4
def WebIndex(target, object, list):
    response = requests.get(target, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    things = soup.find_all(f"{object}")
    
    list.append(things)

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

#Ssh session
def ConnectSsh(target, port, password):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    usrname, host = target.split("@")

    client.connect(
        hostname=host,
        username=usrname,
        port=port,
        password=password,
        timeout=10
    )

    return client

def RunSsh(command, client):
    stdin, stdout, stderr = client.exec_command(command)
    raw = stdout.read().decode("utf-8")
    error = stderr.read().decode("utf-8")
    exit_code = stdout.channel.recv_exit_status()

    return {
        "raw": raw,
        "lines": raw.splitlines(),
        "exit_code": exit_code,
        "error": error
    }

def CloseSsh(client):
    client.close()

# hashing
#hashing algors
HASH_FUNCS = {
    "md5": lambda s: hashlib.md5(s.encode()).hexdigest(),
    "sha1": lambda s: hashlib.sha1(s.encode()).hexdigest(),
    "sha256": lambda s: hashlib.sha256(s.encode()).hexdigest(),
    "sha512": lambda s: hashlib.sha512(s.encode()).hexdigest(),
}

ENCODE_FUNCS = {
    "base64": lambda s: base64.b64encode(s.encode()).decode(),
    "hex": lambda s: s.encode().hex(),
    "url": lambda s: urllib.parse.quote(s),
}

DECODE_FUNCS = {
    "base64": lambda s: base64.b64decode(s.encode()).decode(),
    "hex": lambda s: bytes.fromhex(s).decode(),
    "url": lambda s: urllib.parse.unquote(s),
}

#main func
def hedIt(node):
    if node.name == "hash":
        if len(node.argument) != 2:
            raise SecScriptError("hash should have only 2 arguments", line=node.line)

        from interpreter import evaluate
        algo = evaluate(node.argument[0])
        data = evaluate(node.argument[1])

        if not isinstance(algo, str):
            raise SecScriptError("algorithm should be in string format", line=node.line)
        if algo not in HASH_FUNCS:
            raise SecScriptError(f"Unknows hash algorithm: {algo}", line=node.line)
        if not isinstance(data, str):
            raise SecScriptError("hash data should be in string format", line=node.line)

        return HASH_FUNCS[algo](data)

    elif node.name == "encode":
        if len(node.argument) != 2:
            raise SecScriptError("encode should have only 2 arguments", line=node.line)

        from interpreter import evaluate
        fmt = evaluate(node.argument[0])
        data = evaluate(node.argument[1])

        if not isinstance(fmt, str):
            raise SecScriptError("encoding format should be in string", line=node.line)
        if fmt not in ENCODE_FUNCS:
            raise SecScriptError(f"Unknown encoding format: {fmt}", line=node.line)
        if not isinstance(data, str):
            raise SecScriptError("hash data should be in string", line=node.line)

        return ENCODE_FUNCS[fmt](data)

    elif node.name == "decode":
        if len(node.argument) != 2:
            raise SecScriptError("decode should have only 2 arguments", line=node.line)

        from interpreter import evaluate
        fmt = evaluate(node.argument[0])
        data = evaluate(node.argument[1])

        if not isinstance(fmt, str):
            raise SecScriptError("decoding format should be in string", line=node.line)
        if fmt not in DECODE_FUNCS:
            raise SecScriptError(f"Unknown decoding format: {fmt}", line=node.line)
        if not isinstance(data, str):
            raise SecScriptError("hash data should be in string", line=node.line)

        try:
            return DECODE_FUNCS[fmt](data)
        except Exception:
            raise SecScriptError("Decoding failed, check if the entered data was really one of the valid formats: base64, hex, url", line=node.line)
    
    return None

#http request handeling
def httpRequest(node):
    from interpreter import evaluate
    if node.name == "httpRequest":

        if len(node.argument) != 3:
            raise SecScriptError("httpRequest function only gets 3 arguments (method, url, response form)")
    
        method = evaluate(node.argument[0])
        lowerMethod = method.lower()
        url = evaluate(node.argument[1])
        responseForm = evaluate(node.argument[2]).lower()

        if not isinstance(method, str):
            raise SecScriptError("Method should be only in string format", line=node.line)

        if not isinstance(url, str):
            raise SecScriptError("URL should be in string format", line=node.line)

        if not isinstance(responseForm, str):
            raise SecScriptError("Response form should be in string and one of (text, statusCode, headers)", line=node.line)

        try:
            if lowerMethod == "get":
                if responseForm == "text":
                    return requests.get(url).text

                elif responseForm == "statusCode":
                    return requests.get(url).status_code

                elif responseForm == "headers":
                    return requests.get(url).headers

                else:
                    raise SecScriptError("Unknown responseForm, it should be one of: (text, statusCode, headers)", line=node.line)

            elif lowerMethod == "post":
                if responseForm == "text":
                    return requests.get(url).text

                elif responseForm == "statusCode":
                    return requests.get(url).status_code

                elif responseForm == "headers":
                    return requests.get(url).headers

                else:
                    raise SecScriptError("Unknown responseForm, it should be one of: (text, statusCode, headers)", line=node.line)

            else:
                raise SecScriptError("Method not in range of available methods (post and get)", line=node.line)

        except:
            raise SecScriptError("Error in handling http request", line=node.line)

    return None

#Dns record
def dnsRecords(node):
    from interpreter import evaluate
    import dns.resolver

    domain = evaluate(node.ip)
    record = evaluate(node.record)

    allRecordType = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "SRV", "CAA", "PTR"]

    if record in allRecordType:
        try:
            answers = dns.resolver.resolve(domain, record)
            results = [rdata.to_text() for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                dns.resolver.NoNameservers, dns.exception.Timeout):
            results = []

    elif record == "ALL":
        results = {}
        for rtype in allRecordType:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results[rtype] = [rdata.to_text() for rdata in answers]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                    dns.resolver.NoNameservers, dns.exception.Timeout):
                pass

    else:
        raise SecScriptError("Unknown DNS record wanted", line=node.line)

    return results