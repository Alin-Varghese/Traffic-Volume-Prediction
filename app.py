import streamlit as st
import joblib
import pandas as pd

model = joblib.load("traffic_model.pkl")

st.title("Traffic Volume Prediction")

temp = st.number_input("Temperature")
rain = st.number_input("Rain (mm)")
snow = st.number_input("Snow (mm)")
clouds = st.number_input("Cloud Coverage (%)")

if st.button("Predict"):
    data = pd.DataFrame([[temp, rain, snow, clouds]])
    prediction = model.predict(data)
    st.success(f"Predicted Traffic Volume: {int(prediction[0])}")