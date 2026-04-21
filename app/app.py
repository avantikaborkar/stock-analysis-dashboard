import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from src.data_loader import load_data, load_multiple_data
from src.indicators import add_sma
from src.strategy import generate_signals
from src.backtest import backtest
from src.utils import calculate_metrics



#Page Config
st.set_page_config(layout="wide")
st.title("Trading Dashboard")
st.caption("Backtesting + Strategy Analysis + Multi-Stock Comparison")


# Sidebar
st.sidebar.header("Controls")

ticker = st.sidebar.text_input("Stock", "TCS.NS")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))

st.sidebar.subheader("Strategy Settings")
short_window = st.sidebar.slider("Short SMA", 3, 20, 5)
long_window = st.sidebar.slider("Long SMA", 10, 50, 10)

st.sidebar.subheader("Comparison")
show_compare = st.sidebar.checkbox("Enable Multi-Stock Comparison")

tickers = []
if show_compare:
    tickers = st.sidebar.multiselect(
        "Select Stocks (max 3)",
        ["TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS", "^NSEI"],
        default=["TCS.NS", "INFY.NS"]
    )

    if len(tickers) > 3:
        st.warning("Select max 3 stocks")
        st.stop()


# Data validation
min_days = long_window * 3
if (datetime.today().date() - start_date).days < min_days:
    st.warning("⚠️ Not enough data. Select an earlier start date.")
    st.stop()


# Load data
data = load_data(ticker, start_date)

# FIX: Flatten MultiIndex columns (CRITICAL)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# FIX: Remove duplicate columns
data = data.loc[:, ~data.columns.duplicated()]


#Strategy
data = add_sma(data, short_window, long_window)
data.dropna(inplace=True)

data = generate_signals(data)
data = backtest(data)

final_value, return_pct, trades = calculate_metrics(data)


# metrics
st.markdown("Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Final Value", f"₹{final_value:,.2f}")
col2.metric("Return %", f"{return_pct:.2f}%")
col3.metric("Trades", int(trades))


# Multi-Stock Comparison
if show_compare and len(tickers) > 0:

    st.markdown("---")
    st.markdown("Multi-Stock Comparison")

    multi_data = load_multiple_data(tickers, start_date)

    # Normalize
    normalized = multi_data / multi_data.iloc[0] * 100

    fig_multi = go.Figure()

    for col in normalized.columns:
        fig_multi.add_trace(go.Scatter(
            x=normalized.index,
            y=normalized[col],
            name=str(col)
        ))

    st.plotly_chart(fig_multi, use_container_width=True)

# Strategy Analysis
st.markdown("---")
st.markdown("Strategy Analysis")

#CLEAN DATA FOR PLOTTING
plot_data = data[['Close', 'SMA_Short', 'SMA_Long', 'Signal']].copy()
plot_data.dropna(inplace=True)

#ENSURE NUMERIC TYPES
plot_data['Close'] = plot_data['Close'].astype(float)
plot_data['SMA_Short'] = plot_data['SMA_Short'].astype(float)
plot_data['SMA_Long'] = plot_data['SMA_Long'].astype(float)

#Plotting

fig = go.Figure()

# Price
fig.add_trace(go.Scatter(
    x=plot_data.index,
    y=plot_data['Close'],
    mode='lines',
    name='Price'
))

# SMA Short
fig.add_trace(go.Scatter(
    x=plot_data.index,
    y=plot_data['SMA_Short'],
    mode='lines',
    name='SMA Short'
))

# SMA Long
fig.add_trace(go.Scatter(
    x=plot_data.index,
    y=plot_data['SMA_Long'],
    mode='lines',
    name='SMA Long'
))

# Buy signals
buy = plot_data[plot_data['Signal'] == 1]
fig.add_trace(go.Scatter(
    x=buy.index,
    y=buy['Close'],
    mode='markers',
    marker=dict(symbol='triangle-up', size=10),
    name='Buy'
))

# Sell signals
sell = plot_data[plot_data['Signal'] == -1]
fig.add_trace(go.Scatter(
    x=sell.index,
    y=sell['Close'],
    mode='markers',
    marker=dict(symbol='triangle-down', size=10),
    name='Sell'
))

st.plotly_chart(fig, use_container_width=True)


#Portfolio Performance

st.markdown("---")
st.markdown("Portfolio Performance")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=data.index,
    y=data['Portfolio'],
    name="Portfolio"
))

st.plotly_chart(fig2, use_container_width=True)