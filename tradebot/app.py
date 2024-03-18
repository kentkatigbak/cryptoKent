import yfinance as yf
import streamlit as st

# Streamlit Configurations
st.set_page_config(page_title="KentBot", layout="wide")

# Titles and subtitles
st.title("Crypto Trading Bot ni Kent")

# Defining ticker variables
Bitcoin ='BTC-USD'
Ethereum = 'ETH-USD'
Litecoin = 'LTC-USD'

# Accessing data from Yahoo Finance
BTC_Data = yf.Ticker(Bitcoin)
ETH_Data = yf.Ticker(Ethereum)
LTC_Data = yf.Ticker(Litecoin)

# Fetch history data from Yahoo Finance
BTCHis = BTC_Data.history(period="max")
ETHHis = ETH_Data.history(period="max")
LTCHis = LTC_Data.history(period="max")

BTC = yf.download(Bitcoin, start="2024-03-01", end="2024-03-18")
ETH = yf.download(Ethereum, start="2024-03-01", end="2024-03-18")
LTC = yf.download(Litecoin, start="2024-03-01", end="2024-03-18")

# Function to format the date column without time
def format_date_column(data):
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date  # Extracting only the date component
    data.set_index('Date', inplace=True)
    return data

# Formatting date columns for each cryptocurrency
BTC = format_date_column(BTC)
ETH = format_date_column(ETH)
LTC = format_date_column(LTC)
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

# Litecoin
st.write("Litecoin ($)")
# Display dataframe
st.table(LTC)
# Display a chart
st.line_chart(LTC['Close'])
# Determine and display Buy/Sell action for Litecoin
ltc_action = determine_action(LTC)
st.markdown(ltc_action, unsafe_allow_html=True)
