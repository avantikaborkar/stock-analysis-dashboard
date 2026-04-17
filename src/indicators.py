def add_sma(data, window):
    data[f"SMA_{window}"] = data['Close'].rolling(window).mean()
    return data