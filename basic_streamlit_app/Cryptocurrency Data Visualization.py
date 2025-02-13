import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the cryptocurrency data
csv_path = "data/CryptocurrencyData.csv"
df = pd.read_csv(csv_path)

# Clean column names (strip spaces)
df.columns = df.columns.str.strip()

# Convert numerical columns to float (removing "$" and ",")
def clean_currency(value):
    if isinstance(value, str):
        # Remove the "$" and "," symbols, and check for invalid values like ' - '
        value = value.replace("$", "").replace(",", "")
        # If the value is empty or invalid, return NaN
        if value == '' or value == ' - ':
            return float('nan')
    # Attempt to convert the value to a float, returning NaN if not possible
    try:
        return float(value)
    except ValueError:
        return float('nan')

numeric_cols = ["Price", "24h Volume", "Market Cap"]
for col in numeric_cols:
    df[col] = df[col].apply(clean_currency)

# Streamlit app title
st.title("📊 Cryptocurrency Dashboard")

# App description
st.write("This app allows users to explore and filter cryptocurrency data interactively.")

# Display the dataset
st.subheader("🔍 Sample Data")
st.write(df.head())

# Interactive filtering options
st.sidebar.header("🎛️ Filter Options")

# Dropdown for selecting a cryptocurrency
crypto_choice = st.sidebar.selectbox("Select a Cryptocurrency:", df["Coin Name"].unique())
df_filtered = df[df["Coin Name"] == crypto_choice]

# Numeric filter for Market Cap
min_cap, max_cap = st.sidebar.slider("Market Cap Range:",
                                     float(df["Market Cap"].min()),
                                     float(df["Market Cap"].max()),
                                     (float(df["Market Cap"].min()), float(df["Market Cap"].max())))
df_filtered = df_filtered[(df_filtered["Market Cap"] >= min_cap) & (df_filtered["Market Cap"] <= max_cap)]

# Display the filtered dataset
st.subheader("📜 Filtered Data")
st.write(df_filtered)

# --- Visualization Section ---

# 1️⃣ **Bar Chart - Top 10 Cryptos by Market Cap**
st.subheader("🏆 Top 10 Cryptocurrencies by Market Cap")
top_10 = df.nlargest(10, "Market Cap")
fig, ax = plt.subplots()
ax.barh(top_10["Coin Name"], top_10["Market Cap"], color='skyblue')
ax.set_xlabel("Market Cap (in billions)")
ax.set_ylabel("Cryptocurrency")
ax.set_title("Top 10 Cryptos by Market Cap")
st.pyplot(fig)

# 2️⃣ **Line Chart - Price Trend of Selected Crypto (if multiple entries exist)**
if len(df_filtered) > 1:
    st.subheader(f"📈 Price Trend for {crypto_choice}")
    st.line_chart(df_filtered.set_index("Rank")["Price"])

# 3️⃣ **Pie Chart - Market Cap Distribution**
st.subheader("📊 Market Cap Distribution of Top 5 Cryptos")
top_5 = df.nlargest(5, "Market Cap")
fig, ax = plt.subplots()
ax.pie(top_5["Market Cap"], labels=top_5["Coin Name"], autopct="%1.1f%%", colors=["gold", "silver", "blue", "red", "green"])
ax.set_title("Market Cap Share of Top 5 Cryptos")
st.pyplot(fig)

st.write("📌 *Data sourced from a cryptocurrency dataset. *")
