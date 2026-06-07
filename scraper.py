import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def clean_price(p):
    if not p: return None
    p = re.sub(r'[£,]', '', str(p).strip())
    try: return float(p)
    except: return None

def scrape_argos_top_deals():
    url = "https://www.argos.co.uk/list/shop-top-100-deals"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = []
        for item in soup.find_all('div', {'data-test': 'product-card'})[:15]:
            name = item.find('h3')
            price = item.find('span', {'data-test': 'price'})
            link = item.find('a')
            if name and price:
                products.append({
                    'name': name.get_text(strip=True)[:70],
                    'price': clean_price(price.get_text()),
                    'url': 'https://www.argos.co.uk' + link['href'] if link else ''
                })
        return products
    except:
        return []

def get_top_deals():
    items = scrape_argos_top_deals()
    data = []
    for item in items:
        if not item.get('price'): continue
        suggested = round(item['price'] * 1.20, 2)
        profit = round(suggested - item['price'], 2)
        data.append({
            'Product': item['name'],
            'Argos Price £': item['price'],
            'Suggested Sell £': suggested,
            'Est. Profit £': profit,
            'Link': f'<a href="{item["url"]}" target="_blank">🔗 View</a>'
        })
    return data
