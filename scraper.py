import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0 Safari/537.36"
}

def clean_price(price_text):
    if not price_text:
        return None
    price_text = re.sub(r'[£,]', '', price_text.strip())
    try:
        return float(price_text)
    except:
        return None

def scrape_argos(query=""):
    url = f"https://www.argos.co.uk/search/{query.replace(' ', '+')}" if query else "https://www.argos.co.uk/"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        items = soup.find_all('div', {'data-test': 'product-card'}) or soup.find_all('div', class_='ProductCard')
        
        for item in items[:15]:
            name_tag = item.find('h3') or item.find('a', class_='product-name')
            price_tag = item.find('span', class_='price') or item.find('span', {'data-test': 'price'})
            
            name = name_tag.get_text(strip=True) if name_tag else "No name"
            price_text = price_tag.get_text(strip=True) if price_tag else ""
            price = clean_price(price_text)
            
            if price:
                products.append({
                    'source': 'Argos',
                    'name': name,
                    'price': price,
                    'url': 'https://www.argos.co.uk' + (item.find('a')['href'] if item.find('a') else '')
                })
        return products
    except Exception as e:
        print(f"Argos error: {e}")
        return []

def scrape_ebay(query=""):
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={query.replace(' ', '+')}" if query else "https://www.ebay.co.uk/"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        items = soup.find_all('li', class_='s-item')
        
        for item in items[:12]:
            name = item.find('div', class_='s-item__title')
            price = item.find('span', class_='s-item__price')
            
            name_text = name.get_text(strip=True) if name else "No name"
            price_text = price.get_text(strip=True) if price else ""
            
            cleaned_price = clean_price(price_text)
            if cleaned_price:
                products.append({
                    'source': 'eBay',
                    'name': name_text,
                    'price': cleaned_price,
                    'url': item.find('a')['href'] if item.find('a') else ''
                })
        return products
    except Exception as e:
        print(f"eBay error: {e}")
        return []

def scrape_pcworld(query=""):
    # Placeholder - Currys/PC World selectors change often
    return []