import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def clean_price(price_text):
    if not price_text: return None
    price_text = re.sub(r'[£,]', '', str(price_text).strip())
    try: return float(price_text)
    except: return None

def scrape_argos(query=""):
    url = f"https://www.argos.co.uk/search/{query.replace(' ', '+')}" if query else "https://www.argos.co.uk/"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = []
        for item in soup.find_all('div', {'data-test': 'product-card'})[:8]:
            name = item.find('h3')
            price = item.find('span', {'data-test': 'price'})
            if name and price:
                products.append({'source': 'Argos', 'name': name.get_text(strip=True), 'price': clean_price(price.get_text()), 'url': 'https://www.argos.co.uk' + (item.find('a')['href'] if item.find('a') else '')})
        return products
    except: return []

def scrape_ebay(query=""):
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={query.replace(' ', '+')}" if query else "https://www.ebay.co.uk/"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = []
        for item in soup.find_all('li', class_='s-item')[:8]:
            name = item.find('div', class_='s-item__title')
            price = item.find('span', class_='s-item__price')
            if name and price:
                products.append({'source': 'eBay', 'name': name.get_text(strip=True), 'price': clean_price(price.get_text()), 'url': item.find('a')['href'] if item.find('a') else ''})
        return products
    except: return []

def scrape_currys(query=""):
    # Placeholder - can improve later
    return []
