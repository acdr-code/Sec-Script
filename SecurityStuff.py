import socket
import requests
from bs4 import BeautifulSoup

def portScan(ip, port, timeout, list):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    if result == 0:
        list.append(port)
    sock.close()


def WebIndex(target, object, list):
    response = requests.get(target, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    things = soup.find_all(f"{object}")
    
    list.append(things)