import sys
import os
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.data_loader import load_data
from src.indicators import add_sma
from src.strategy import generate_signals
from src.backtest import backtest
from src.utils import clean_data

st.title("Stock Analysis Dashboard")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    data = load_data(file)
    data = clean_data(data)

    #IMPORTANT: SMA must be created BEFORE strategy
    data = add_sma(data, 5)
    data = add_sma(data, 10)

    data = generate_signals(data)
    data = backtest(data)

    st.write(data.tail())

    #SMA5 crossing above SMA10 → BUY signal, SMA5 crossing below SMA10 → SELL, signal The graph helps you see WHY a trade happened, not just numbers.

    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        name="Close Price"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['SMA_5'],
        name="SMA 5"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['SMA_10'],
        name="SMA 10"
    ))

    fig.update_layout(
        title="Stock Analysis Dashboard",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )

    st.plotly_chart(fig)