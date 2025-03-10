import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

#business question
st.title("Diamonds Pricing\n___")
st.header("Which diamond cut has the highest average price?")
st.write("Individual Assignment by Margarita Ivanova", fontsize=5)

# Dataset - diamonds from seaborn
df = sns.load_dataset("diamonds")

#charts

#bar chart - for average price by diamond cut
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



#Session State
if "chart" not in st.session_state:
    st.session_state.chart = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "response_time" not in st.session_state:
    st.session_state.response_time = None
# Store the last recorded response time so we can have both the last and the current respnse time for the user
if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = None  

#Button1 to show random chart and both buttons to be dark purple with white font and a black border
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4B0082;
        color: white !important;
        font-size: 16px;
        border-radius: 10px;
        padding: 20px;
        border: 2px solid black;
    }
    .stButton>button:hover {
        background-color: #5A009D; 
    }
    </style>
""", unsafe_allow_html=True)

if st.button("Show a Chart"):
    st.session_state.chart = random.choice(["A", "B"]) 
    st.session_state.start_time = time.time()  # Start timing

    if st.session_state.response_time is not None:
        st.session_state.last_response_time = st.session_state.response_time

    # Reset response time for new attempt
    st.session_state.response_time = None  

    if st.session_state.chart == "A":
        create_chart_a()
    else:
        create_chart_b()

# Show the button 2
    st.session_state.show_answer_button = True  

# Button2 to measure response time
if "show_answer_button" in st.session_state and st.session_state.show_answer_button:
    if st.button("I answered your question"):
        st.session_state.response_time = time.time() - st.session_state.start_time
        st.success(f"You took {st.session_state.response_time:.2f} seconds to answer.")

# When clicking on button1 to show a random chart again --> show last response time
if st.session_state.last_response_time is not None:
    st.write(f"Your last response time: {st.session_state.last_response_time:.2f} seconds")

# show current response time if answered
if st.session_state.response_time is not None:
    st.write(f"Your response time: {st.session_state.response_time:.2f} seconds")
