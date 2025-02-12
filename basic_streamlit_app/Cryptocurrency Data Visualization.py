import streamlit as st
import pandas as pd

# Load the CSV data
@st.cache_data #cache functions that returns data
def load_data():
    data = pd.read_csv("./data/CryptocurrencyData.csv")
    return data

df = load_data()

st.title("Cryptocurrency Data Explorer")

# Short description of what the app does
st.write("""
This app allows you to explore cryptocurrency data. You can filter the data based on various criteria such as market cap, price, and more.
""")

# Display the sample DataFrame
st.subheader("Sample Cryptocurrency Data")
st.write(df.head())

# Interactive filtering options
st.sidebar.header("Filter Options")

# Filter by Market Cap
market_cap_range = st.sidebar.slider(
    "Select Market Cap Range (in billions)",
    float(df[" Market Cap "].min() / 1e9),
    float(df[" Market Cap "].max() / 1e9),
    (float(df[" Market Cap "].min() / 1e9), float(df[" Market Cap "].max() / 1e9))
)

# Filter by Price
price_range = st.sidebar.slider(
    "Select Price Range",
    float(df[" Price "].min()),
    float(df[" Price "].max()),
    (float(df[" Price "].min()), float(df[" Price "].max()))
)

# Filter by Coin Name
coin_name = st.sidebar.multiselect(
    "Select Coin Name",
    df["Coin Name"].unique()
)

# Apply filters
filtered_df = df[
    (df[" Market Cap "] >= market_cap_range[0] * 1e9) & 
    (df[" Market Cap "] <= market_cap_range[1] * 1e9) &
    (df[" Price "] >= price_range[0]) &
    (df[" Price "] <= price_range[1])
]

if coin_name:
    filtered_df = filtered_df[filtered_df["Coin Name"].isin(coin_name)]

# Display the filtered DataFrame
st.subheader("Filtered Cryptocurrency Data")
st.write(filtered_df)

# Additional visualizations (optional)
st.subheader("Market Cap Distribution")
st.bar_chart(filtered_df.set_index("Coin Name")[" Market Cap "])

st.subheader("Price Distribution")
st.bar_chart(filtered_df.set_index("Coin Name")[" Price "])