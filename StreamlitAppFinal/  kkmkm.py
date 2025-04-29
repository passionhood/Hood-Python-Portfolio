# Portfolio Analyzer Streamlit App
# Passion Hood
# Course: Elements of Computing II, Spring 2025
# Final Project

# --- Import Necessary Libraries ---
import streamlit as st  # Web app framework
import pandas as pd     # Data manipulation
import numpy as np      # Numerical computations
import yfinance as yf   # Yahoo Finance API for stock data
import matplotlib.pyplot as plt  # Plotting
import seaborn as sns   # Advanced visualization
from datetime import datetime  # Date handling

# --- Set Default Parameters ---
RISK_FREE_RATE = 0.03  # Assume 3% risk-free rate for Sharpe Ratio calculations
START_DATE = '2022-01-01'  # Start pulling data from Jan 2022
END_DATE = datetime.today().strftime('%Y-%m-%d')  # Today's date
SP500_TICKER = '^GSPC'  # S&P 500 index ticker

# --- Streamlit App Config ---
st.set_page_config(page_title='Portfolio Analyzer', layout='wide')

# --- App Title and Instructions ---
st.title('Investment Portfolio Analyzer')
st.write("""
Upload a CSV file containing the following columns:
- **Ticker** (e.g., AAPL)
- **Shares** (number of shares owned)
- **Purchase Price** (optional)

The app will analyze your portfolio's current value, risk, and performance metrics.
""")

# --- Sidebar for File Upload and Chart Selection ---
st.sidebar.header('Upload Your Portfolio CSV')
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
chart_type = st.sidebar.radio("Choose Allocation View", ['Pie Chart', 'Bar Chart'])

if uploaded_file:
    try:
        # --- Read and Clean Uploaded CSV ---
        portfolio_df = pd.read_csv(uploaded_file)
        portfolio_df.columns = portfolio_df.columns.str.strip()

        # --- Validate Required Columns ---
        if not {'Ticker', 'Shares'}.issubset(portfolio_df.columns):
            st.error("CSV must include at least 'Ticker' and 'Shares' columns.")
        else:
            # --- Download Historical Stock Data ---
            tickers = portfolio_df['Ticker'].tolist()
            data = yf.download(tickers, start=START_DATE, end=END_DATE, group_by='ticker', auto_adjust=True, threads=True)

            # --- Map Latest Prices to Tickers ---
            latest_prices = {}
            for ticker in tickers:
                try:
                    latest_prices[ticker] = data[ticker]['Close'][-1]
                except:
                    st.warning(f"Data for {ticker} not found. Skipping.")

            # --- Calculate Market Values ---
            portfolio_df['Current Price'] = portfolio_df['Ticker'].map(latest_prices)
            portfolio_df.dropna(subset=['Current Price'], inplace=True)
            st.warning("Some tickers were removed because price data was unavailable.")
            portfolio_df['Market Value'] = portfolio_df['Shares'] * portfolio_df['Current Price']

            # --- Calculate Portfolio Allocation ---
            total_value = portfolio_df['Market Value'].sum()
            portfolio_df['Allocation %'] = (portfolio_df['Market Value'] / total_value) * 100

            # --- Calculate Unrealized Gains/Losses if Purchase Price is Provided ---
            if 'Purchase Price' in portfolio_df.columns:
                portfolio_df['Unrealized Gain ($)'] = (portfolio_df['Current Price'] - portfolio_df['Purchase Price']) * portfolio_df['Shares']
                portfolio_df['Unrealized Gain (%)'] = ((portfolio_df['Current Price'] - portfolio_df['Purchase Price']) / portfolio_df['Purchase Price']) * 100
            else:
                st.info("**Note:** Purchase Price column missing. Unrealized gains/losses will not be displayed.")

            # --- Display Portfolio Table ---
            st.subheader('Portfolio Overview')
            st.dataframe(portfolio_df.style.format({
                'Current Price': '${:.2f}',
                'Market Value': '${:,.2f}',
                'Allocation %': '{:.2f}%',
                'Unrealized Gain ($)': '${:,.2f}',
                'Unrealized Gain (%)': '{:.2f}%'
            }))

            # --- Asset Allocation Chart (Toggleable) ---
            st.subheader('Asset Allocation')
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            if chart_type == 'Pie Chart':
                ax1.pie(
                    portfolio_df['Allocation %'],
                    labels=portfolio_df['Ticker'],
                    autopct=lambda p: f'{p:.1f}%' if p > 2 else '',
                    startangle=140,
                    textprops={'fontsize': 10}
                )
                ax1.axis('equal')
            else:
                sns.barplot(data=portfolio_df.sort_values('Allocation %', ascending=False), x='Ticker', y='Allocation %', palette='pastel', ax=ax1)
                ax1.set_ylabel('Allocation (%)')
                ax1.set_title('Portfolio Allocation by Ticker')
            st.pyplot(fig1)

            # --- Portfolio vs S&P 500 Performance ---
            st.subheader('Portfolio Performance vs. S&P 500')
            portfolio_returns = pd.DataFrame()
            for ticker in tickers:
                try:
                    portfolio_returns[ticker] = data[ticker]['Close'].pct_change()
                except:
                    continue

            weighted_returns = (portfolio_returns * (portfolio_df.set_index('Ticker')['Allocation %'] / 100)).sum(axis=1)
            cumulative_returns = (1 + weighted_returns).cumprod()

            sp500 = yf.download(SP500_TICKER, start=START_DATE, end=END_DATE, auto_adjust=True)
            sp500_returns = sp500['Close'].pct_change()
            sp500_cumulative = (1 + sp500_returns).cumprod()

            fig2, ax2 = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=cumulative_returns, label='Your Portfolio', ax=ax2)
            sns.lineplot(data=sp500_cumulative, label='S&P 500', ax=ax2)
            ax2.set_ylabel('Growth of $1')
            ax2.set_title('Cumulative Return Since 2022')
            ax2.legend()
            st.pyplot(fig2)

            # --- Portfolio Risk Metrics ---
            st.subheader('Portfolio Risk Metrics')

            # Volatility (Annualized Std Dev)
            volatility = weighted_returns.std() * np.sqrt(252)

            # Sharpe Ratio
            sharpe = ((weighted_returns.mean() * 252) - RISK_FREE_RATE) / volatility

            # Beta vs. S&P 500
            aligned = pd.concat([weighted_returns, sp500_returns], axis=1).dropna()
            aligned.columns = ['Portfolio', 'S&P 500']
            beta = aligned.cov().iloc[0, 1] / aligned['S&P 500'].var()

            # Maximum Drawdown
            rolling_max = cumulative_returns.cummax()
            drawdown = cumulative_returns / rolling_max - 1
            max_drawdown = drawdown.min()

            # Display Risk Metrics
            st.markdown(f"""
            - **Portfolio Volatility (Annualized)**: `{volatility:.2%}`
            - **Sharpe Ratio (Risk-Free Rate 3%)**: `{sharpe:.2f}`
            - **Beta (vs. S&P 500)**: `{beta:.2f}`
            - **Maximum Drawdown**: `{max_drawdown:.2%}`
            """)

            # --- Correlation Heatmap ---
            st.subheader('Correlation Heatmap')
            fig3, ax3 = plt.subplots(figsize=(12, 10))
            sns.heatmap(portfolio_returns.corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0, annot_kws={'size': 7}, ax=ax3)
            ax3.set_title('Correlation Between Assets')
            st.pyplot(fig3)

            # --- Download Portfolio Report ---
            st.subheader('Download Summary Report')
            report = portfolio_df[['Ticker', 'Shares', 'Current Price', 'Market Value', 'Allocation %']]
            st.download_button(label="Download Portfolio Report (CSV)",
                               data=report.to_csv(index=False),
                               file_name='portfolio_summary.csv',
                               mime='text/csv')

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.warning("Please check your CSV file format and try again.")
else:
    st.info('👈 Upload a CSV file to get started!')

