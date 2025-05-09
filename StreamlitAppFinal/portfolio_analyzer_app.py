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
    st.markdown("Download ready-to-use example portfolios:") # Provides the user with example portfolios
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

        # --- Validate Required Columns ---
        if not {'Ticker', 'Shares'}.issubset(portfolio_df.columns):
            st.error("CSV must include 'Ticker' and 'Shares' columns.")
        else:
            tickers = portfolio_df['Ticker'].tolist()

            # --- Download Stock Data ---
            data = yf.download(tickers, start=START_DATE, end=END_DATE, group_by='ticker', auto_adjust=True, threads=True)

            # --- Fetch Latest Closing Prices from multi-index dataframe ---
            latest_prices = {}
            for ticker in tickers:
                try:
                    latest_prices[ticker] = data['Close'][ticker].dropna().iloc[-1]
                except:
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

            # --- Allocation Visualization (Pie or Bar Chart) ---
            st.subheader('Asset Allocation')
            fig1, ax1 = plt.subplots(figsize=(10, 6))

            if chart_type == 'Pie Chart':
                # Format slice labels and percentages for readability
                def autopct_format(p):
                    return f'{p:.1f}%' if p > 3 else ''

                def label_format(label, pct):
                    return label if pct > 3 else ''

                sizes = portfolio_df['Allocation %']
                labels = portfolio_df['Ticker']
                formatted_labels = [label_format(label, pct) for label, pct in zip(labels, sizes)]

                ax1.pie(sizes, labels=formatted_labels, autopct=autopct_format, startangle=140, textprops={'fontsize': 9})
                ax1.axis('equal')  # Ensure circular pie
                ax1.legend(portfolio_df['Ticker'], title="Tickers", bbox_to_anchor=(1, 0.5), loc="center left", fontsize=9)
            else:
                # Display bar chart if selected
                sns.barplot(data=portfolio_df.sort_values('Allocation %', ascending=False), x='Ticker', y='Allocation %', palette='pastel', ax=ax1)
                ax1.set_ylabel('Allocation (%)')
                ax1.set_title('Portfolio Allocation by Ticker')

            st.pyplot(fig1)

            # --- Portfolio vs. Market Performance ---
            st.subheader('Portfolio Performance vs. S&P 500')

            # Compute daily returns for each stock
            portfolio_returns = pd.DataFrame()
            for ticker in tickers:
                try:
                    portfolio_returns[ticker] = data[ticker]['Close'].pct_change()
                except:
                    continue

            # Weighted portfolio return = sum of (asset return * allocation weight)
            weighted_returns = (portfolio_returns * (portfolio_df.set_index('Ticker')['Allocation %'] / 100)).sum(axis=1)
            cumulative_returns = (1 + weighted_returns).cumprod()

            # S&P 500 comparison returns
            sp500 = yf.download(SP500_TICKER, start=START_DATE, end=END_DATE, auto_adjust=True)
            sp500_returns = sp500['Close'].pct_change()
            sp500_cumulative = (1 + sp500_returns).cumprod()

            # Plot cumulative returns
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            ax2.plot(cumulative_returns.index, cumulative_returns.values, label='Your Portfolio', linewidth=2)
            ax2.plot(sp500_cumulative.index, sp500_cumulative.values, label='S&P 500', linewidth=2)
            ax2.set_ylabel('Growth of $1')
            ax2.set_title('Cumulative Return Since 2022')
            ax2.legend()
            st.pyplot(fig2)

            # --- Risk Metrics Calculation ---
            st.subheader('Portfolio Risk Metrics')

            # Annualized volatility = std dev of daily returns * sqrt(252 trading days)
            volatility = weighted_returns.std() * np.sqrt(252)

            # Sharpe ratio = (return - risk-free rate) / volatility
            sharpe = ((weighted_returns.mean() * 252) - RISK_FREE_RATE) / volatility

            # Beta = Covariance(portfolio, market) / Variance(market)
            aligned = pd.concat([weighted_returns, sp500_returns], axis=1).dropna()
            aligned.columns = ['Portfolio', 'S&P 500']
            beta = aligned.cov().iloc[0, 1] / aligned['S&P 500'].var()

            # Max drawdown = largest historical drop from peak
            rolling_max = cumulative_returns.cummax()
            drawdown = cumulative_returns / rolling_max - 1
            max_drawdown = drawdown.min()

            # Display metrics
            st.markdown(f"""
            - **Portfolio Volatility (Annualized)**: `{volatility:.2%}`
            - **Sharpe Ratio (Risk-Free Rate 3%)**: `{sharpe:.2f}`
            - **Beta (vs. S&P 500)**: `{beta:.2f}`
            - **Maximum Drawdown**: `{max_drawdown:.2%}`
            """)

            # --- Asset Correlation Matrix ---
            st.subheader('Correlation Heatmap')
            fig3, ax3 = plt.subplots(figsize=(12, 10))
            sns.heatmap(portfolio_returns.corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0, annot_kws={'size': 7}, ax=ax3)
            ax3.set_title('Correlation Between Assets')
            st.pyplot(fig3)

            # --- Export Summary ---
            st.subheader('Download Summary Report')
            report = portfolio_df[['Ticker', 'Shares', 'Current Price', 'Market Value', 'Allocation %']]
            st.download_button(
                label="Download Portfolio Report (CSV)",
                data=report.to_csv(index=False),
                file_name='portfolio_summary.csv',
                mime='text/csv'
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.warning("Please check your CSV file format and try again.")

else:
    st.info('👈 Upload a CSV file to get started!')