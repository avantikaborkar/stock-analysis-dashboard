from src.data_loader import load_data
from src.indicators import add_sma
from src.strategy import generate_signals
from src.backtest import backtest
from src.utils import calculate_metrics, clean_data

def main():
    print("Running Stock Analysis...\n")

    # Load data
    data = load_data("data/sample_stock.csv")
    # Clean data
    data = clean_data(data)

    # Add indicators
    data = add_sma(data, 5)    # Use small values for sample data
    data = add_sma(data, 10)

    # Generate signals
    data = generate_signals(data)

    # Backtest strategy
    data = backtest(data)

    # Calculate metrics
    metrics = calculate_metrics(data)

    # Display results
    print("Strategy Performance:\n")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\nLast 5 Rows:")
    print(data.tail())

if __name__ == "__main__":
    main()