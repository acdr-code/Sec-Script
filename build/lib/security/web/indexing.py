import requests
from bs4 import BeautifulSoup

#BetterBs4
def WebIndex(target, object, list):
    response = requests.get(target, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    things = soup.find_all(f"{object}")
    
    list.append(things)