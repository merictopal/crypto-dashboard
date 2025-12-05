import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(
    page_title="Crypto Tracker Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Title and Description ---
st.title("📈 Real-Time Crypto & Stock Tracker")
st.markdown("""
This dashboard retrieves real-time data using **Yahoo Finance API** and visualizes trends.
Select a ticker symbol from the sidebar to analyze performance.
""")

# --- Sidebar Controls ---
st.sidebar.header("Configuration")

# Dropdown for selecting assets
ticker_symbol = st.sidebar.selectbox(
    "Select Asset:",
    ("BTC-USD", "ETH-USD", "SOL-USD", "AAPL", "GOOGL", "TSLA", "AMZN")
)

# Date range selection
time_period = st.sidebar.selectbox(
    "Select Time Period:",
    ("1mo", "3mo", "6mo", "1y", "5y", "max")
)

# --- Data Fetching Function ---
@st.cache_data
def load_data(symbol, period):
    """
    Fetches historical data from Yahoo Finance.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return data, ticker.info
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None

# Load Data
with st.spinner('Loading data...'):
    df, info = load_data(ticker_symbol, time_period)

# --- Display Content ---
if df is not None and not df.empty:
    
    # 1. Key Metrics Row
    col1, col2, col3 = st.columns(3)
    
    current_price = df['Close'].iloc[-1]
    previous_close = df['Close'].iloc[-2]
    price_change = current_price - previous_close
    percent_change = (price_change / previous_close) * 100

    col1.metric("Current Price", f"${current_price:.2f}", f"{percent_change:.2f}%")
    col2.metric("High (Period)", f"${df['High'].max():.2f}")
    col3.metric("Low (Period)", f"${df['Low'].min():.2f}")

    # 2. Charts
    st.subheader(f"Price History: {ticker_symbol}")
    st.line_chart(df['Close'])

    st.subheader("Volume Analysis")
    st.bar_chart(df['Volume'])

    # 3. Raw Data (Expandable)
    with st.expander("View Raw Data"):
        st.dataframe(df.sort_index(ascending=False))

    # 4. Download Button
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=f'{ticker_symbol}_data.csv',
        mime='text/csv',
    )
else:
    st.warning("No data found for the selected ticker.")

# --- Footer ---
st.markdown("---")
st.caption("Built with Streamlit & Python • Data provided by Yahoo Finance")