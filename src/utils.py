import numpy as np
def calculate_metrics(data, initial_capital=100000):
    
    final_value = data['Portfolio'].iloc[-1]
    return_pct = ((final_value - initial_capital) / initial_capital) * 100
    trades = data['Signal'].abs().sum()

    return final_value, return_pct, trades

#Daily Returns
def compute_returns(data):
    prices = data['Close'].values
    returns = np.diff(prices) / prices[:-1]

    data = data.iloc[1:].copy()
    data['Returns'] = returns
    return data


#Volatility (Annualized)
def compute_volatility(data):
    return np.std(data['Returns']) * np.sqrt(252)

#Max Drawdown
def max_drawdown(portfolio):
    values = portfolio.values
    peak = np.maximum.accumulate(values)
    drawdown = (values - peak) / peak
    return np.min(drawdown)