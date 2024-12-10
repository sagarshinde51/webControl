import streamlit as st
import mysql.connector  # Corrected import statement
from mysql.connector import OperationalError, IntegrityError  # For error handling
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Custom Toggle Switches App with Database Update")

# Function to connect to the database
def connect_to_db():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="82.180.143.66",
            user="u263681140_students",
            password="testStudents@123",
            database="u263681140_students"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to update the values in the UpdateFlag table
def update_flag(id, value):
    try:
        connection = connect_to_db()
        if connection is None:
            return
        cursor = connection.cursor()
        query = "UPDATE UpdateFlag SET F1 = %s WHERE id = %s"
        cursor.execute(query, (value, id))
        connection.commit()
        cursor.close()
        connection.close()
        st.success(f"Successfully updated ID {id} to {value}")
    except mysql.connector.Error as err:
        st.error(f"Failed to update ID {id}: {err}")

# Function to fetch temperature and humidity data
def fetch_temperature_humidity():
    try:
        connection = connect_to_db()
        if connection is None:
            return None, None
        
        cursor = connection.cursor()
        query = "SELECT temp, humi FROM TempHumi WHERE id = 1"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            return result  # Returns temp, humi as a tuple
        else:
            return None, None
    except mysql.connector.Error as err:
        st.error(f"Error fetching temperature and humidity: {err}")
        return None, None

# Fetch temperature and humidity for id 1
temperature, humidity = fetch_temperature_humidity()

# Display temperature and humidity in the sidebar
if temperature is not None and humidity is not None:
    st.sidebar.write(f"Temperature: {temperature}°C")
    st.sidebar.write(f"Humidity: {humidity}%")
    
    # Create a DataFrame for plotting the chart
    data = {
        'Metric': ['Temperature (°C)', 'Humidity (%)'],
        'Value': [temperature, humidity]
    }
    
    df = pd.DataFrame(data)
    
    # Plot the chart in the sidebar
    fig, ax = plt.subplots()
    ax.bar(df['Metric'], df['Value'], color=['blue', 'green'])
    ax.set_title('Temperature and Humidity')
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Values')
    st.sidebar.pyplot(fig)  # Display the plot in the sidebar
else:
    st.sidebar.write("No temperature and humidity data available.")

# Custom CSS to style the toggle switch
toggle_css = """
    <style>
    .toggle-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 30px;
    }
    .toggle-container div {
        text-align: center;
        cursor: pointer;
        padding: 10px 20px;
        border: 1px solid #ddd;
        border-radius: 25px;
        background-color: #f1f1f1;
        transition: background-color 0.3s;
    }
    .toggle-container div:hover {
        background-color: #ddd;
    }
    .active {
        background-color: #4CAF50;
        color: white;
    }
    </style>
"""
st.markdown(toggle_css, unsafe_allow_html=True)

# Create custom toggle switches using select_slider
switch1 = st.select_slider("Switch 1", options=["off", "on"], key="switch1")
switch2 = st.select_slider("Switch 2", options=["off", "on"], key="switch2")
switch3 = st.select_slider("Switch 3", options=["off", "on"], key="switch3")

# Display the values (1 if ON, 0 if OFF)
st.write("Switch 1 value:", 1 if switch1 == 'on' else 0)
st.write("Switch 2 value:", 1 if switch2 == 'on' else 0)
st.write("Switch 3 value:", 1 if switch3 == 'on' else 0)

# Update database values when button is clicked
update_flag(1, 1 if switch1 == 'on' else 0)
update_flag(2, 1 if switch2 == 'on' else 0)
update_flag(3, 1 if switch3 == 'on' else 0)
