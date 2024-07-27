import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Streamlit Configurations
st.set_page_config(page_title="KentTrades", layout="wide")

# Titles and subtitles
st.title("Kent Crypto Data Mining")

# Define the list of cryptocurrencies
cryptos = {
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD',
    'Solana': 'SOL-USD',
    'BNB': 'BNB-USD',
    'XRP': 'XRP-USD',
    'DOGE': 'DOGE-USD',
    'TRX': 'TRX-USD',
    'DOT': 'DOT-USD',
    'ATOM': 'ATOM-USD',
    'MKR': 'MKR-USD'
}

# Selectbox for choosing cryptocurrency
selected_crypto = st.selectbox("Select a cryptocurrency", list(cryptos.keys()))

# Input for number of days
num_days = st.number_input("Enter the number of days for the data", min_value=1, max_value=365, value=90)

# Calculate the dates based on user input
end_date = datetime.now()
start_date = end_date - timedelta(days=num_days)

# Convert dates to string format for Yahoo Finance
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

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

# Descriptive statistics
def descriptive_statistics(df):
    stats = pd.DataFrame()
    stats['Max'] = df.max()
    stats['Min'] = df.min()
    stats['Mean'] = df.mean()
    stats['Median'] = df.median()
    stats['Mode'] = df.mode().iloc[0]  # Mode may have multiple values, take the first
    stats['Variance'] = df.var()
    stats['Std Dev'] = df.std()
    
    # Drop 'Min' and 'Max' columns from the final output
    stats = stats.drop(['Min', 'Max'], axis=1)
    
    # Transpose the DataFrame to match the format of the data table
    stats = stats.T
    stats.columns = ['Value']  # Set column name for clarity
    
    return stats

# Calculate descriptive statistics for each column
stats = descriptive_statistics(data)

# Display selected cryptocurrency data
st.write(f"{selected_crypto} ($)")
# Display dataframe
st.table(data)
# Display descriptive statistics
st.write("Descriptive Statistics:")
st.table(stats)

# Add a download button for the data
csv = data.to_csv(index=True)
st.download_button(
    label=f"Download {selected_crypto} Data as CSV",
    data=csv,
    file_name=f"{selected_crypto}_data.csv",
    mime="text/csv"
)
