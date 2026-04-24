import numpy as np

def generate_signals(data):
    short = data['SMA_Short'].values
    long = data['SMA_Long'].values

    signal = np.zeros(len(data))

    # Detect crossovers
    signal[1:] = np.where(
        (short[1:] > long[1:]) & (short[:-1] <= long[:-1]), 1,
        np.where(
            (short[1:] < long[1:]) & (short[:-1] >= long[:-1]), -1, 0
        )
    )

    data['Signal'] = signal
    return data