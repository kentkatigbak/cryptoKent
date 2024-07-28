import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Streamlit Configurations
st.set_page_config(page_title="KentTrades", layout="wide", page_icon="💰")

# Remove header and footer
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
        <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Titles and subtitles
with st.sidebar:
    st.write("")
    st.image("tradebot/logoWhiteBG.png")
    st.title("")
    st.title("")
    st.title("")
    st.title("")
    st.write("____________________________________")
    st.title("KENT KATIGBAK")

st.title("KENT TRADES")
st.write("""
        This is a crypto data mining app that collects actual data of selected crypto currencies
        within the selected number of days in the past. It also displays the descriptive statistics
        of the gathered data to make a quick and easy analysis.
        """)
st.write("____________________________________")

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

# View actual data or descriptive statistics
view_select = st.selectbox("Select data to view", ["View Actual Data", "View Descriptive Statistics"])
st.write("____________________________________")

# Calculate the dates based on user input
end_date = datetime.now()
start_date = end_date - timedelta(days=num_days)

# Convert dates to string format for Yahoo Finance
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Get the ticker symbol based on selection
ticker = cryptos[selected_crypto]

# Function to get the most recent price of a cryptocurrency
def get_current_price(ticker):
    try:
        data = yf.download(ticker, period='1d')  # Get the most recent data
        if not data.empty and 'Close' in data.columns:
            return data['Close'].iloc[-1]
    except Exception as e:
        st.error(f"Error fetching current price: {e}")
    return None

# Accessing data from Yahoo Finance
data = yf.download(ticker, start=start_date_str, end=end_date_str)
if data.empty:
    st.error(f"No data found for {ticker}.")
else:
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
        
        # Date of max and min values
        max_date = df.idxmax()
        min_date = df.idxmin()
        stats['Max Date'] = max_date
        stats['Min Date'] = min_date
        
        return stats

    # Calculate descriptive statistics for each column
    stats = descriptive_statistics(data)
    mean_closing_price = stats.loc['Close', 'Mean']

    # Get and format the current price
    current_price = get_current_price(ticker)
    current_price_display = f"${current_price:.2f}" if current_price is not None else "Current price not available."

    # Determine if the current price is above or below the mean
    if current_price is not None:
        if current_price > mean_closing_price:
            price_comparison = f"Current price is above the historical mean closing price (${mean_closing_price:.2f})."
        elif current_price < mean_closing_price:
            price_comparison = f"Current price is below the historical mean closing price (${mean_closing_price:.2f})."
        else:
            price_comparison = "Current price is equal to the historical mean closing price."

    # View actual data
    if view_select == "View Actual Data":
        # Add a download button for the data
        csv = data.to_csv(index=True)
        st.download_button(
            label=f"Download {selected_crypto} Data as CSV",
            data=csv,
            file_name=f"{selected_crypto}_data.csv",
            mime="text/csv"
        )
        # Display selected cryptocurrency data
        st.write(f"{selected_crypto} ($)")
        
        # Display the current price of the selected cryptocurrency
        st.write(f"Current Price: {current_price_display}")
        st.write(price_comparison)
        
        # Display dataframe
        data = data.round(2)
        st.dataframe(data, use_container_width=True)

    # View descriptive statistics
    if view_select == "View Descriptive Statistics":
        # Display descriptive statistics
        st.write("Descriptive Statistics:")
        
        # Display the current price of the selected cryptocurrency
        st.write(f"Current Price: {current_price_display}")
        st.write(price_comparison)
        
        # Display descriptive statistics
        stats = stats.round(2)
        st.dataframe(stats.T, use_container_width=True)
