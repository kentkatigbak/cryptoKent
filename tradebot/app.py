import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta

# Streamlit Configurations
st.set_page_config(page_title="KentBot", layout="wide")

# Titles and subtitles
st.title("Crypto Trading Bot ni Kent")

# Defining ticker variables
Bitcoin = 'BTC-USD'
Ethereum = 'ETH-USD'
Solana = 'SOL-USD'

# Calculate the dates for the past 60 days
end_date = datetime.now()
start_date = end_date - timedelta(days=60)

# Convert dates to string format for Yahoo Finance
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Accessing data from Yahoo Finance
BTC_Data = yf.Ticker(Bitcoin)
ETH_Data = yf.Ticker(Ethereum)
SOL_Data = yf.Ticker(Solana)

# Fetch history data from Yahoo Finance
BTC = yf.download(Bitcoin, start=start_date_str, end=end_date_str)
ETH = yf.download(Ethereum, start=start_date_str, end=end_date_str)
SOL = yf.download(Solana, start=start_date_str, end=end_date_str)

# Function to format the date column without time
def format_date_column(data):
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date  # Extracting only the date component
    data.set_index('Date', inplace=True)
    return data

# Formatting date columns for each cryptocurrency
BTC = format_date_column(BTC)
ETH = format_date_column(ETH)
SOL = format_date_column(SOL)

# Function to determine Buy or Sell based on the trend
def determine_action(data):
    change = data['Close'].iloc[-1] - data['Close'].iloc[0]
    if change > 0:
        return "<div style='border:1px solid black;padding:10px;color:green;text-align:center;font-weight:bold'>Sell</div>"
    elif change < 0:
        return "<div style='border:1px solid black;padding:10px;color:red;text-align:center;font-weight:bold'>Buy</div>"
    else:
        return "<div style='border:1px solid black;padding:10px;color:blue;text-align:center;font-weight:bold'>Hold</div>"

# Bitcoin
st.write("Bitcoin ($)")
# Display dataframe
st.table(BTC)
# Display a chart
st.line_chart(BTC['Close'])
# Determine and display Buy/Sell action for Bitcoin
btc_action = determine_action(BTC)
st.markdown(btc_action, unsafe_allow_html=True)

# Ethereum
st.write("Ethereum ($)")
# Display dataframe
st.table(ETH)
# Display a chart
st.line_chart(ETH['Close'])
# Determine and display Buy/Sell action for Ethereum
eth_action = determine_action(ETH)
st.markdown(eth_action, unsafe_allow_html=True)

# Solana
st.write("Solana ($)")
# Display dataframe
st.table(SOL)
# Display a chart
st.line_chart(SOL['Close'])
# Determine and display Buy/Sell action for Solana
sol_action = determine_action(SOL)
st.markdown(sol_action, unsafe_allow_html=True)
