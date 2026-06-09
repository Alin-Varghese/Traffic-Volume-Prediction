import streamlit as st
import joblib
import pandas as pd

# Load model and feature order
model = joblib.load("traffic_model.pkl")
cols = joblib.load("feature_columns.pkl")

st.title("🚦 Traffic Volume Prediction App")

# --------------------------
# USER INPUTS
# --------------------------

temp = st.number_input("Temperature (K)")
rain = st.number_input("Rain (mm)")
snow = st.number_input("Snow (mm)")
clouds = st.number_input("Cloud Coverage (%)")

hour = st.selectbox("Hour (0-23)", list(range(24)))
month = st.selectbox("Month (1-12)", list(range(1, 13)))

# Extract categorical options from training columns
holiday_options = ["None"] + [c.replace("holiday_", "") for c in cols if c.startswith("holiday_")]
weather_main_options = [c.replace("weather_main_", "") for c in cols if c.startswith("weather_main_")]
weather_desc_options = [c.replace("weather_description_", "") for c in cols if c.startswith("weather_description_")]

day_options = [c.replace("day_", "") for c in cols if c.startswith("day_")]

holiday = st.selectbox("Holiday", holiday_options)
weather_main = st.selectbox("Weather Main", weather_main_options)
weather_desc = st.selectbox("Weather Description", weather_desc_options)
day = st.selectbox("Day of Week", day_options)

# --------------------------
# PREDICTION
# --------------------------
if st.button("Predict Traffic Volume"):

    # Start with all zeros
    input_data = {col: 0 for col in cols}

    # Fill numeric values
    input_data["temp"] = temp
    input_data["rain_1h"] = rain
    input_data["snow_1h"] = snow
    input_data["clouds_all"] = clouds
    input_data["hour"] = hour
    input_data["month"] = month

    # Fill categorical values safely (only if column exists)
    if holiday != "None":
        col_name = "holiday_" + holiday
        if col_name in input_data:
            input_data[col_name] = 1

    col_name = "weather_main_" + weather_main
    if col_name in input_data:
        input_data[col_name] = 1

    col_name = "weather_description_" + weather_desc
    if col_name in input_data:
        input_data[col_name] = 1

    col_name = "day_" + day
    if col_name in input_data:
        input_data[col_name] = 1

    # Convert to DataFrame in correct order
    df = pd.DataFrame([input_data])[cols]

    # Prediction
    prediction = model.predict(df)[0]

    st.success(f"🚗 Predicted Traffic Volume: {int(prediction)}")
