#!/usr/bin/env python3
import sys
import httpx
from bs4 import BeautifulSoup
import time

def get_stock_data(symbol, field):
    try:
        search_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = httpx.get(search_url, headers=headers, timeout=10)
        data = response.json()
        if not any(result['symbol'] == symbol for result in data.get('quotes', [])):
            raise Exception(f"Тикер '{symbol}' не найден")
    except:
        raise Exception(f"Тикер '{symbol}' не найден")
    url = f"https://finance.yahoo.com/quote/{symbol}/financials"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
   
     #cоздаем HTTP-клиент с поддержкой редиректов, иначе будет плохо
    with httpx.Client(follow_redirects=True) as client:
         #передаем гет-запрос для получения данных из сервера
        response = client.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Страница недоступна. Статус: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all('div', class_='row lv-0 yf-t22klz') #ищем все строки по классу строк таблицы на юхуфинанс
        for row in rows:
            title = row.find('div', class_='rowTitle') #перебираем все строки и ищем заголовок
            if title and field.lower() in title.get_text(strip=True).lower():
                values = row.find_all('div', class_='column yf-t22klz')
                alt_values = row.find_all('div', class_='column yf-t22klz alt')
                
                clean_values = [v.get_text(strip=True) for v in values]
                clean_alt_values = [v.get_text(strip=True) for v in alt_values]
                combined_values = []   #наш пустой список для хранения объединенных белых и серых ячеек без пробелов
                i, j = 0, 0
                for idx in range(len(clean_values) + len(clean_alt_values)): #цикл по общему количеству значений
                    if idx % 2 == 0 and j < len(clean_alt_values):
                        combined_values.append(clean_alt_values[j])
                        j += 1
                    elif i < len(clean_values):
                        combined_values.append(clean_values[i])
                        i += 1
                return tuple([title.get_text(strip=True)] + combined_values)
    raise Exception(f"Поле '{field}' не найдено")

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