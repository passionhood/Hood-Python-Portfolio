import streamlit as st 
import pandas as pd 

st.cache_data  #cache functions that return data

def load_data(): #loads the dataset
    return pd.read_csv("CryptocurrencyData.csv")

data = load_data()

st.title('Cryptocurrency Data Explorer') #title app

st.write("Explore various cryptocurrencies and their market data based on name and minimum market capitalization.") ## Description of the app


selected_crypto = st.selectbox('Select a Cryptocurrency:', data['Name'].unique()) #creates a dropdown to select the cryptocurrency name

st.write("Here's a table displaying the data:")
st.dataframe("CryptocurrencyData.csv") 

# Slider to select the minimum market cap
# Assuming the MarketCap column is numeric and represents the market capitalization in some units
min_market_cap = st.slider('Minimum Market Cap:', min_value=int(data['MarketCap'].min()), 
                           max_value=int(data['MarketCap'].max()), 
                           value=int(data['MarketCap'].min()))

# Filter data based on user selection from the dropdown and slider
filtered_data = data[(data['Name'] == selected_crypto) & (data['MarketCap'] >= min_market_cap)]
st.write(filtered_data)