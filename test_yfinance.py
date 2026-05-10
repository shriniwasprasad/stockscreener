import yfinance as yf
import time

tickers = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'SBIN.NS']

for ticker in tickers:
    print(f'\n=== Testing {ticker} ===')
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        print(f'forwardPE: {info.get("forwardPE")}')
        print(f'trailingPE: {info.get("trailingPE")}')
        print(f'pegRatio: {info.get("pegRatio")}')
        print(f'trailingEps: {info.get("trailingEps")}')

        hist = stock.history(period='60d')
        if not hist.empty:
            print(f'Close: {hist["Close"].iloc[-1]}')
            print(f'Volume: {hist["Volume"].iloc[-1]}')
            print(f'Avg Volume 20d: {hist["Volume"].iloc[-20:].mean()}')

            delta = hist['Close'].diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            print(f'RSI: {rsi.iloc[-1]}')
        else:
            print('No historical data')
    except Exception as e:
        print(f'Error: {e}')
    time.sleep(1)