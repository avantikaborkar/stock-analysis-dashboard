def backtest(data, initial_capital=100000):
    position = 0
    cash = initial_capital
    portfolio_values = []


    data['Signal'] = data['Signal'].fillna(0).astype(int)

    for i in range(len(data)):
        signal = int(data['Signal'].iloc[i])   # force scalar
        price = float(data['Close'].iloc[i])

        # Buy
        if signal == 1 and position == 0:
            position = cash / price
            cash = 0

        # Sell
        elif signal == -1 and position > 0:
            cash = position * price
            position = 0

        portfolio_value = cash + (position * price)
        portfolio_values.append(portfolio_value)

    data['Portfolio'] = portfolio_values
    return data