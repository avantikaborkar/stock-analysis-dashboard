def backtest(data, initial_cash=10000):
    cash = initial_cash
    position = 0
    portfolio_value = []

    for i in range(len(data)):
        price = data['Close'].iloc[i]

        if data['Position'].iloc[i] == 1:  # BUY
            position = cash // price
            cash -= position * price

        elif data['Position'].iloc[i] == -1:  # SELL
            cash += position * price
            position = 0

        total = cash + position * price
        portfolio_value.append(total)

    data['Portfolio'] = portfolio_value
    return data