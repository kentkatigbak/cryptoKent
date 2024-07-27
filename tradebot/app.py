import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Streamlit Configurations
st.set_page_config(page_title="KentBot", layout="wide")

# Titles and subtitles
st.title("Crypto Trading Bot ni Kent")

# Define the list of cryptocurrencies
cryptos = {
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD',
    'Solana': 'SOL-USD'
}

# Calculate the dates for the past 90 days
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

# Convert dates to string format for Yahoo Finance
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Selectbox for choosing cryptocurrency
selected_crypto = st.selectbox("Select a cryptocurrency", list(cryptos.keys()))

# Get the ticker symbol based on selection
ticker = cryptos[selected_crypto]

# Accessing data from Yahoo Finance
data = yf.download(ticker, start=start_date_str, end=end_date_str)

# Function to format the date column without time
def format_date_column(data):
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date  # Extracting only the date component
    data.set_index('Date', inplace=True)
    return data

# Formatting date column
data = format_date_column(data)

# Function to determine Buy or Sell based on the trend
def determine_action(data):
    change = data['Close'].iloc[-1] - data['Close'].iloc[0]
    if change > 0:
        return "<div style='border:1px solid black;padding:10px;color:green;text-align:center;font-weight:bold'>Sell</div>"
    elif change < 0:
        return "<div style='border:1px solid black;padding:10px;color:red;text-align:center;font-weight:bold'>Buy</div>"
    else:
        return "<div style='border:1px solid black;padding:10px;color:blue;text-align:center;font-weight:bold'>Hold</div>"

# Display selected cryptocurrency data
st.write(f"{selected_crypto} ($)")
# Display dataframe
st.table(data)
# Display a chart
st.line_chart(data['Close'])
# Determine and display Buy/Sell action for selected cryptocurrency
action = determine_action(data)
st.markdown(action, unsafe_allow_html=True)

# Add a download button for the data
csv = data.to_csv(index=True)
st.download_button(
    label=f"Download {selected_crypto} Data as CSV",
    data=csv,
    file_name=f"{selected_crypto}_data.csv",
    mime="text/csv"
)
