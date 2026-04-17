def generate_signals(data):
    data['Signal'] = 0

    data['Signal'] = (data['SMA_5'] > data['SMA_10']).astype(int)

    data['Position'] = data['Signal'].diff()

    return data