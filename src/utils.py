# src/utils.py

import pandas as pd

def calculate_returns(data):
    """
    Calculate daily returns
    """
    data['Returns'] = data['Close'].pct_change()
    return data


def calculate_volatility(data, window=20):
    """
    Rolling volatility (standard deviation of returns)
    """
    data['Volatility'] = data['Returns'].rolling(window).std()
    return data


def calculate_metrics(data, initial_cash=10000):
    """
    Calculate performance metrics
    """
    final_value = data['Portfolio'].iloc[-1]
    total_return = (final_value - initial_cash) / initial_cash * 100

    trades = data['Position'].value_counts()
    num_trades = trades.get(1, 0) + trades.get(-1, 0)

    return {
        "Initial Capital": initial_cash,
        "Final Portfolio Value": round(final_value, 2),
        "Total Return (%)": round(total_return, 2),
        "Number of Trades": int(num_trades)
    }


def clean_data(data):
    """
    Basic cleaning (handle missing values)
    """
    data = data.copy()
    data.ffill(inplace=True)
    data.dropna(inplace=True)
    return data


def format_currency(value):
    """
    Format number into currency string
    """
    return f"₹{value:,.2f}"