from src.data_loader import load_data
from src.indicators import add_sma
from src.strategy import generate_signals
from src.backtest import backtest
from src.utils import calculate_metrics

data = load_data("TCS.NS", "2022-01-01")
data = add_sma(data, 5, 10)
data = generate_signals(data)
data = backtest(data)

final_value, return_pct, trades = calculate_metrics(data)

print(final_value, return_pct, trades)