# Passion Hood
# CSE 10102: Elements of Computing II, Spring 2025
# Final Project: Portfolio Analyzer Streamlit App

# --- Import Necessary Libraries ---
import streamlit as st  # Streamlit for web UI
import pandas as pd  # Data processing
import numpy as np  # Numeric operations
import yfinance as yf  # Yahoo Finance API
import matplotlib.pyplot as plt  # Data visualization
import seaborn as sns  # Enhanced plotting
from datetime import datetime  # For dynamic date handling

# --- Global Constants ---
RISK_FREE_RATE = 0.03  # Assumed 3% risk-free rate for Sharpe Ratio
START_DATE = '2022-01-01'  # Data start date
END_DATE = datetime.today().strftime('%Y-%m-%d')  # Today's date
SP500_TICKER = '^GSPC'  # S&P 500 index ticker

# --- Streamlit Configurations ---
st.set_page_config(page_title='Portfolio Analyzer', layout='wide')

# --- App Introduction ---
st.title('Investment Portfolio Analyzer')
st.write("""
Upload a CSV file with your portfolio to analyze:
- **Ticker** (e.g., AAPL)
- **Shares** (quantity owned)
- **Purchase Price** (optional)

We'll compute allocations, performance, and risk metrics.
""")

# --- Example Portfolio Downloads ---
with st.sidebar.expander("Need a sample file?"):
    st.markdown("Download ready-to-use example portfolios:")
    st.markdown("🔹 [With Purchase Price](https://nd4-my.sharepoint.com/:x:/g/personal/phood_nd_edu/EVoFtlq33cNIoWQQQInbAWEBsIyOXWq6OOn-zuM4Xxtd1w?e=r9zNeL)")
    st.markdown("🔹 [Without Purchase Price](https://nd4-my.sharepoint.com/:x:/g/personal/phood_nd_edu/Efvj1CE5HfpMsPZ6Uypm_FYBqJpKsvDCFl8SKsQZwZsV3g?e=r7KA1f)")
    st.caption("Use these to test features like gain/loss calculations and chart visualizations.")

# --- Sidebar Inputs ---
st.sidebar.header('Upload Your Portfolio CSV')
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
chart_type = st.sidebar.radio("Choose Allocation View", ['Pie Chart', 'Bar Chart'])

if uploaded_file:
    try:
        # --- Load and Clean Data ---
        portfolio_df = pd.read_csv(uploaded_file)
        portfolio_df.columns = portfolio_df.columns.str.strip()  # Clean column names
        portfolio_df['Ticker'] = portfolio_df['Ticker'].astype(str).str.upper().str.strip()  # Normalize tickers

        # --- Validate Required Columns ---
        if not {'Ticker', 'Shares'}.issubset(portfolio_df.columns):
            st.error("CSV must include 'Ticker' and 'Shares' columns.")
        else:
            tickers = portfolio_df['Ticker'].tolist()

            # --- Download Stock Data ---
            data = yf.download(tickers, start=START_DATE, end=END_DATE, auto_adjust=True, threads=True)

            # --- Flatten MultiIndex columns (e.g., ('Close', 'AAPL') → 'AAPL_Close') ---
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = ['{}_{}'.format(col[1], col[0]) for col in data.columns]

            # --- Fetch Latest Closing Prices ---
            latest_prices = {}
            for ticker in tickers:
                col_name = f"{ticker}_Close"
                if col_name in data.columns:
                    latest_prices[ticker] = data[col_name].dropna().iloc[-1]
                else:
                    st.warning(f"Data for {ticker} not found. Skipping.")

            # --- Calculate Current Price and Market Value ---
            portfolio_df['Current Price'] = portfolio_df['Ticker'].map(latest_prices)
            portfolio_df.dropna(subset=['Current Price'], inplace=True)
            st.warning("Tickers with missing data were removed.")
            portfolio_df['Market Value'] = portfolio_df['Shares'] * portfolio_df['Current Price']

            # --- Calculate Allocation Percentage ---
            total_value = portfolio_df['Market Value'].sum()
            portfolio_df['Allocation %'] = (portfolio_df['Market Value'] / total_value) * 100

            # --- Optional: Calculate Unrealized Gains/Losses ---
            if 'Purchase Price' in portfolio_df.columns:
                portfolio_df['Unrealized Gain ($)'] = (portfolio_df['Current Price'] - portfolio_df['Purchase Price']) * portfolio_df['Shares']
                portfolio_df['Unrealized Gain (%)'] = ((portfolio_df['Current Price'] - portfolio_df['Purchase Price']) / portfolio_df['Purchase Price']) * 100
            else:
                st.info("Purchase Price column not found. Unrealized gains/losses omitted.")

            # --- Portfolio Overview Table ---
            st.subheader('Portfolio Overview')
            st.dataframe(portfolio_df.style.format({
                'Current Price': '${:.2f}',
                'Market Value': '${:,.2f}',
                'Allocation %': '{:.2f}%',
                'Unrealized Gain ($)': '${:,.2f}',
                'Unrealized Gain (%)': '{:.2f}%'
            }))

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.warning("Please check your CSV file format and try again.")

else:
    st.info('👈 Upload a CSV file to get started!')

import yfinance as yf
print(yf.download('AAPL', period='5d'))