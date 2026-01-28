#!/usr/bin/env python3
import sys
import time
import requests
from bs4 import BeautifulSoup

def check_ticker_valid(ticker):
    #проверяем, существует ли наш тикер и обманываем сайт, притворившись браузером
    try:
        search_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}"
        search_headers = {'User-Agent': 'Mozilla/5.0'}
        search_response = requests.get(search_url, headers=search_headers, timeout=10)
        #json нам отвечает, а мы преобразовываем его ответ в словарь
        search_data = search_response.json()
        #вернем тру, если хотя бы один результат совпадает
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
    # oтправляем get-запрос к странице с финансовыми данными
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Страница недоступна. Статус: {response.status_code}")
#возвращаем текстовое содержимое HTML-страницы
    return response.text

def parse_html(content):
    #создаем наш объект для помощи в парсинге
    return BeautifulSoup(content, "html.parser")

def find_data_row(soup, target_field):
     # ищем в разобранном html нужные строки, а класс 'row lv-0 yf-t22klz' - это стиль строк в Yahoo Finance
    rows = soup.find_all('div', class_='row lv-0 yf-t22klz')
    for row in rows:
        #в каждой строке ищем заголовок и проверяем его существование
        title = row.find('div', class_='rowTitle')
        if title and target_field.lower() in title.get_text(strip=True).lower():
            values = row.find_all('div', class_='column yf-t22klz') # ячейки с обычными значениями
            alt_values = row.find_all('div', class_='column yf-t22klz alt') #а это с альтернативными
            
            clean_values = [v.get_text(strip=True) for v in values]
            clean_alt_values = [v.get_text(strip=True) for v in alt_values] 
            #из обеих извлекли текст и убрали пробелы
            combined_values = []
            i, j = 0, 0
            for idx in range(len(clean_values) + len(clean_alt_values)):
                if idx % 2 == 0 and j < len(clean_alt_values): #чередуем четные индексы с альтернативными значениями
                    combined_values.append(clean_alt_values[j])
                    j += 1 #и увеличиваем счетчик
                elif i < len(clean_values):
                    combined_values.append(clean_values[i])
                    i += 1
            return tuple([title.get_text(strip=True)] + combined_values)
    raise Exception(f"Поле '{target_field}' не найдено")

def get_stock_data(symbol, field):
    #разбираем полученный html и находим в нем данные
    html = get_page_content(symbol)
    soup = parse_html(html)
    return find_data_row(soup, field)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    symbol = sys.argv[1].upper() #получаем тикер из аргументов
    field = sys.argv[2]
    try:
        result = get_stock_data(symbol, field)
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)