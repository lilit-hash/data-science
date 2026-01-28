#!/usr/bin/env python3
import sys
import time
import requests
from bs4 import BeautifulSoup

def check_ticker_valid(ticker):
    try:
        search_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}"
        search_headers = {'User-Agent': 'Mozilla/5.0'}
        search_response = requests.get(search_url, headers=search_headers, timeout=10)
        search_data = search_response.json()
        return any(result['symbol'] == ticker for result in search_data.get('quotes', []))
    except:
        return False

def get_page_content(stock_symbol):
    if not check_ticker_valid(stock_symbol):
        raise Exception(f"Тикер '{stock_symbol}' не найден")
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/financials"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    time.sleep(5)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Страница недоступна. Статус: {response.status_code}")

    return response.text

def parse_html(content):
    return BeautifulSoup(content, "html.parser")

def find_data_row(soup, target_field):
    rows = soup.find_all('div', class_='row lv-0 yf-t22klz')
    for row in rows:
        title = row.find('div', class_='rowTitle')
        if title and target_field.lower() in title.get_text(strip=True).lower():
            values = row.find_all('div', class_='column yf-t22klz')
            alt_values = row.find_all('div', class_='column yf-t22klz alt')
            
            clean_values = [v.get_text(strip=True) for v in values]
            clean_alt_values = [v.get_text(strip=True) for v in alt_values]
            combined_values = []
            i, j = 0, 0
            for idx in range(len(clean_values) + len(clean_alt_values)):
                if idx % 2 == 0 and j < len(clean_alt_values):
                    combined_values.append(clean_alt_values[j])
                    j += 1
                elif i < len(clean_values):
                    combined_values.append(clean_values[i])
                    i += 1
            return tuple([title.get_text(strip=True)] + combined_values)
    raise Exception(f"Поле '{target_field}' не найдено")

def get_stock_data(symbol, field):
    html = get_page_content(symbol)
    soup = parse_html(html)
    return find_data_row(soup, field)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    symbol = sys.argv[1].upper()
    field = sys.argv[2]
    try:
        result = get_stock_data(symbol, field)
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)