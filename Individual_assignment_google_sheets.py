import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import seaborn as sns
import random
import time
import matplotlib.pyplot as plt



st.title("Diamonds Pricing\n___")
st.header("Which diamond cut has the highest average price?")
st.write("Individual Assignment by Margarita Ivanova")

# Step 1: Connect to Google Sheets API
def get_google_sheet_data(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_creditentials.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(sheet_name).sheet1  # Access first sheet

    # Get all data and convert to Pandas DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df

# Step 2: Fetch live data from Google Sheets
SHEET_NAME = "Diamond Dataset" 
df = get_google_sheet_data(SHEET_NAME)

# Step 3: Display data table to verify
st.write("Diamonds Pricing Data from Google Sheets:")
st.dataframe(df)

# Step 4: Define the Charts
def create_chart_a():
    avg_prices = df.groupby("cut")["price"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    avg_prices.plot(kind="bar", ax=ax, color=['blue', 'orange', 'green', 'red', 'purple'])
    ax.set_title("Average Price by Diamond Cut")
    ax.set_ylabel("Average Price (USD)")
    ax.set_xlabel("Diamond Cut")
    st.pyplot(fig)


#Line Chart - average price trend by diamond cut
def create_chart_b():
    avg_prices = df.groupby("cut")["price"].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots()
    avg_prices.plot(kind="line", ax=ax, marker="o", linestyle="-", color="purple")
    
    ax.set_title("Average Price Trend by Diamond Cut")
    ax.set_ylabel("Average Price (USD)")
    ax.set_xlabel("Diamond Cut")
    ax.grid(True)  # Adds a grid to understand better
    
    st.pyplot(fig)


# Step 5: Custom CSS for Styling Buttons
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4B0082;
        color: white !important;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
        border: 2px solid black;
    }
    .stButton>button:hover {
        background-color: #5A009D; 
        border: 2px solid black; 
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Step 6: Initialize session state variables
if "chart" not in st.session_state:
    st.session_state.chart = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "response_time" not in st.session_state:
    st.session_state.response_time = None
if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = None  

# Step 7: Button to Show Random Chart
if st.button("Show a Chart"):
    st.session_state.chart = random.choice(["A", "B"])  # Randomly pick a chart
    st.session_state.start_time = time.time()  # Start timing

    # Save the last response time before resetting
    if st.session_state.response_time is not None:
        st.session_state.last_response_time = st.session_state.response_time

    # Reset response time for new attempt
    st.session_state.response_time = None  

# Step 8: Display the Selected Chart
if "chart" in st.session_state and st.session_state.chart:
    if st.session_state.chart == "A":
        create_chart_a()
    else:
        create_chart_b()

    # Step 9: Second Button to Record New Response Time
    if st.button("I answered your question"):
        st.session_state.response_time = time.time() - st.session_state.start_time
        st.success(f"You took {st.session_state.response_time:.2f} seconds to answer.")

# Step 10: Show Last Response Time
if st.session_state.last_response_time is not None:
    st.write(f"Your last response time: {st.session_state.last_response_time:.2f} seconds")

# Step 11: Show Current Response Time if Answered
if st.session_state.response_time is not None:
    st.write(f"Your response time: {st.session_state.response_time:.2f} seconds")
