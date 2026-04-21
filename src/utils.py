def calculate_metrics(data, initial_capital=100000):
    
    final_value = data['Portfolio'].iloc[-1]
    return_pct = ((final_value - initial_capital) / initial_capital) * 100
    trades = data['Signal'].abs().sum()

    return final_value, return_pct, trades