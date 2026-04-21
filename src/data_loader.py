import yfinance as yf
import pandas as pd

def load_data(ticker, start):
    data = yf.download(ticker, start=start)
    data.dropna(inplace=True)
    return data


def load_multiple_data(tickers, start):
    import yfinance as yf

    data = yf.download(tickers, start=start)['Close']

    data.dropna(inplace=True)
    return data