import sys

def get_stock_data():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    return COMPANIES, STOCKS

def process_query(query):
    COMPANIES, STOCKS = get_stock_data()
    
  
    ticker_to_company = {ticker.lower(): company for company, ticker in COMPANIES.items()}
    company_to_ticker = {company.lower(): ticker for company, ticker in COMPANIES.items()}
    
    expressions = [e.strip() for e in query.split(',') if e.strip()]
    if not expressions or len(expressions) != len([e for e in query.split(',')]):
        return None
    
    results = []
    for expr in expressions:
        expr_lower = expr.lower()
        
        if expr_lower in ticker_to_company:  
            company = ticker_to_company[expr_lower]
            results.append(f"{expr.upper()} is a ticker symbol for {company}")
        elif expr_lower in company_to_ticker:  
            ticker = company_to_ticker[expr_lower]
            price = STOCKS[ticker]
            results.append(f"{expr.capitalize()} stock price is {price}")
        else:
            results.append(f"{expr.capitalize()} is an unknown company or an unknown ticker symbol")
    return results

def main():
    if len(sys.argv) != 2:
        return
    query = sys.argv[1]
    if ',,' in query or ', ,' in query:
        return
    results = process_query(query)
    if results:
        print('\n'.join(results))

if __name__ == '__main__':
    main()