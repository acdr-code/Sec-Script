import socket

def portScan(ip, port, timeout, list):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    if result == 0:
        list.append(port)
    sock.close()