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

def scrape_argos_top_deals():
    url = "https://www.argos.co.uk/list/shop-top-100-deals"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = []
        for item in soup.find_all('div', {'data-test': 'product-card'})[:20]:  # Top 20 for speed
            name_tag = item.find('h3')
            price_tag = item.find('span', {'data-test': 'price'})
            link_tag = item.find('a')
            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = clean_price(price_tag.get_text())
                url = 'https://www.argos.co.uk' + link_tag['href'] if link_tag else ''
                products.append({'source': 'Argos', 'name': name, 'price': price, 'url': url})
        return products
    except:
        return []

def quick_ebay_search(name):
    # Simple fuzzy search on eBay
    query = name[:60]  # limit length
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={query.replace(' ', '+')}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_tag = soup.find('span', class_='s-item__price')
        if price_tag:
            return clean_price(price_tag.get_text())
        return None
    except:
        return None

def get_comparison_data():
    argos_items = scrape_argos_top_deals()
    results = []
    for item in argos_items:
        if not item['price']: continue
        ebay_price = quick_ebay_search(item['name'])
        prices = [p for p in [item['price'], ebay_price] if p]
        avg_price = round(sum(prices)/len(prices), 2) if prices else item['price']
        suggested_sell = round(item['price'] * 1.15, 2)  # 15% markup example
        profit = round(suggested_sell - item['price'], 2)
        
        results.append({
            'Product': item['name'][:80],
            'Argos Price': item['price'],
            'eBay Price': ebay_price,
            'Avg Price': avg_price,
            'Suggested Sell': suggested_sell,
            'Est. Profit': profitcd C:\Users\Phill\Downloads\dealprism\dealprism

# New scraper focused on Top Deals
@"
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

def scrape_argos_top_deals():
    url = "https://www.argos.co.uk/list/shop-top-100-deals"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = []
        for item in soup.find_all('div', {'data-test': 'product-card'})[:20]:  # Top 20 for speed
            name_tag = item.find('h3')
            price_tag = item.find('span', {'data-test': 'price'})
            link_tag = item.find('a')
            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = clean_price(price_tag.get_text())
                url = 'https://www.argos.co.uk' + link_tag['href'] if link_tag else ''
                products.append({'source': 'Argos', 'name': name, 'price': price, 'url': url})
        return products
    except:
        return []

def quick_ebay_search(name):
    # Simple fuzzy search on eBay
    query = name[:60]  # limit length
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={query.replace(' ', '+')}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_tag = soup.find('span', class_='s-item__price')
        if price_tag:
            return clean_price(price_tag.get_text())
        return None
    except:
        return None

def get_comparison_data():
    argos_items = scrape_argos_top_deals()
    results = []
    for item in argos_items:
        if not item['price']: continue
        ebay_price = quick_ebay_search(item['name'])
        prices = [p for p in [item['price'], ebay_price] if p]
        avg_price = round(sum(prices)/len(prices), 2) if prices else item['price']
        suggested_sell = round(item['price'] * 1.15, 2)  # 15% markup example
        profit = round(suggested_sell - item['price'], 2)
        
        results.append({
            'Product': item['name'][:80],
            'Argos Price': item['price'],
            'eBay Price': ebay_price,
            'Avg Price': avg_price,
            'Suggested Sell': suggested_sell,
            'Est. Profit': profit,
            'Argos Link': item['url']
        })
    return results
