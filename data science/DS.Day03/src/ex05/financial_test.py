#!/usr/bin/env python3
import sys
import os
import pytest
current_dir = os.path.dirname(os.path.abspath(__file__))
ex03_path = os.path.join(current_dir, '..', 'ex03')
sys.path.insert(0, ex03_path)
from financial import get_stock_data, check_ticker_valid

def test_valid_ticker_valid_field():
    result = get_stock_data('AAPL', 'Total Revenue')
    assert isinstance(result, tuple), "Функция должна возвращать кортеж"
    assert len(result) > 1, "Должны быть данные кроме названия поля"
    assert 'Total Revenue' in result[0], "Первый элемент должен содержать название поля"

def test_invalid_ticker_raises_exception():
    with pytest.raises(Exception, match="Тикер.*не найден"):
        get_stock_data('INVALID123', 'Total Revenue')

def test_valid_ticker_invalid_field_raises_exception():
    with pytest.raises(Exception, match="Поле.*не найдено"):
        get_stock_data('AAPL', 'NonExistentField123')

def test_result_is_tuple():
    result = get_stock_data('MSFT', 'Gross Profit')
    assert isinstance(result, tuple), "Функция должна возвращать кортеж"

def test_different_tickers_work():
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    for ticker in tickers:
        result = get_stock_data(ticker, 'Total Revenue')
        assert isinstance(result, tuple), f"Для {ticker} должен возвращаться кортеж"
        assert len(result) > 1, f"Для {ticker} должны быть данные"

def test_ticker_validation_works():
    assert check_ticker_valid('AAPL') == True, "AAPL должен быть валидным"
    assert check_ticker_valid('MSFT') == True, "MSFT должен быть валидным"
    assert check_ticker_valid('INVALID123') == False, "INVALID123 должен быть невалидным"

def test_financial_data_values_not_empty():
    result = get_stock_data('AAPL', 'Gross Profit')
    for value in result[1:]:
        assert value.strip() != '', "Финансовые значения не должны быть пустыми"
        assert value != '0', "Финансовые значения не должны быть нулевыми"