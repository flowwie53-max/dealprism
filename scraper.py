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
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = []
        for item in soup.find_all('div', {'data-test': 'product-card'})[:25]:
            name = item.find('h3')
            price = item.find('span', {'data-test': 'price'})
            link = item.find('a')
            if name and price:
                products.append({
                    'name': name.get_text(strip=True),
                    'argos_price': clean_price(price.get_text()),
                    'url': 'https://www.argos.co.uk' + link['href'] if link else ''
                })
        return products
    except:
        return []

def quick_ebay_check(name):
    try:
        q = '+'.join(name.split()[:5])
        r = requests.get(f"https://www.ebay.co.uk/sch/i.html?_nkw={q}", headers=headers, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        price = soup.find('span', class_='s-item__price')
        return clean_price(price.get_text()) if price else None
    except:
        return None

def get_top_deals():
    items = scrape_argos_top_deals()
    data = []
    for item in items:
        if not item.get('argos_price'): continue
        ebay_p = quick_ebay_check(item['name'])
        avg = round((item['argos_price'] + (ebay_p or item['argos_price'])) / 2, 2)
        suggested = round(item['argos_price'] * 1.20, 2)
        profit = round(suggested - item['argos_price'], 2)
        
        data.append({
            'Product': item['name'][:75],
            'Argos Price £': item['argos_price'],
            'eBay ~£': ebay_p or '—',
            'Avg £': avg,
            'Suggested Sell £': suggested,
            'Est. Profit £': profit,
            'Link': f'<a href="{item["url"]}" target="_blank">🔗 View on Argos</a>'
        })
    return data
