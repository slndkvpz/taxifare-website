import streamlit as st
import requests
import datetime

CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url('https://res.cloudinary.com/dtljonz0f/image/upload/c_auto,ar_4:3,w_3840,g_auto/f_auto/q_auto/shutterstock_329662223_ss_non-editorial_3_csm8lw?_a=BAVARSDW0');
    background-size: cover;
}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# Title and instructions
st.title("🚕 TaxiFare 🚕")
st.write("💸 Please enter the details below to get the fare price 💸")


# Input fields
ride_date = st.date_input(label="Select Pickup Date", value="default_value_today", min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
ride_time = st.time_input(label="Select Pickup Time", value="now", key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible", step=datetime.timedelta(minutes=1))

pickup_longitude = st.number_input("Pickup Longitude", format="%.6f")
pickup_latitude = st.number_input("Pickup Latitude", format="%.6f")
dropoff_longitude = st.number_input("Dropoff Longitude", format="%.6f")
dropoff_latitude = st.number_input("Dropoff Latitude", format="%.6f")
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=6)

# Submit button
if st.button("Get Fare Prediction"):
    # Ensure all inputs are filled
    if not ride_date or not ride_time:
        st.error("Please enter the date and time.")
    else:
        # Prepare data dictionary
        params = {
            "pickup_datetime": ride_date.strftime("%Y-%m-%d") + " " + ride_time.strftime("%H:%M:%S"),
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count
        }

        # API call
        url = 'https://taxifare.lewagon.ai/predict'
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            prediction = response.json().get("fare", "Prediction not available")
            
            # Display prediction
            st.subheader(f"Predicted Fare: ${prediction:.2f}")
        except Exception as e:
            st.error(f"Error occurred while calling the API: {e}")
