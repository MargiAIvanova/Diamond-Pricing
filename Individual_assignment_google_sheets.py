import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import seaborn as sns
import random
import time
import matplotlib.pyplot as plt
import json



st.title("Diamonds Pricing\n___")
st.header("Which diamond cut has the highest average price?")
st.write("Individual Assignment by Margarita Ivanova")

# connect to Google Sheets API
def get_google_sheet_data(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Streamlit Secrets
    creds_dict = json.loads(st.secrets["google"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(sheet_name).sheet1  # Access first sheet

    # Get all data and convert to Pandas DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df

#  live data from Google Sheets
SHEET_NAME = "Diamond Dataset" 
df = get_google_sheet_data(SHEET_NAME)

# Display data table to ensure it's correct (specifically if it updates when we change something in the google sheets)
st.write("Diamonds Pricing Data from Google Sheets:")
st.dataframe(df)

# create the Charts
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


# style the buttons - dark purple wiht white font and a black border when we hover on it it changes to a light purple 
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

# session state time setup
if "chart" not in st.session_state:
    st.session_state.chart = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "response_time" not in st.session_state:
    st.session_state.response_time = None
if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = None  

# button1 to show a random chart
if st.button("Show a Chart"):
    st.session_state.chart = random.choice(["A", "B"])  # Randomly pick a chart
    st.session_state.start_time = time.time()  # Start timing

    # Save the last response time
    if st.session_state.response_time is not None:
        st.session_state.last_response_time = st.session_state.response_time

    # Reset response time for new attempt
    st.session_state.response_time = None  

# Display the chosen Chart
if "chart" in st.session_state and st.session_state.chart:
    if st.session_state.chart == "A":
        create_chart_a()
    else:
        create_chart_b()

    # Button2 to Record New Response Time
    if st.button("I answered your question"):
        st.session_state.response_time = time.time() - st.session_state.start_time
        st.success(f"You took {st.session_state.response_time:.2f} seconds to answer.")

# display the last response time for comparison 
if st.session_state.last_response_time is not None:
    st.write(f"Your last response time: {st.session_state.last_response_time:.2f} seconds")

# Step 11: Show Current Response Time if Answered
if st.session_state.response_time is not None:
    st.write(f"Your response time: {st.session_state.response_time:.2f} seconds")
