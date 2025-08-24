# STREAMLIT APP CODE - segmentation.py

# ==================== IMPORTS ====================
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ==================== LOAD MODEL AND SCALER ====================
model_path = 'kmeans_model.pkl'
scaler_path = 'scaler.pkl'

if not os.path.exists(model_path) or not os.path.exists(scaler_path):
    st.error(f"Missing model or scaler file. Please ensure '{model_path}' and '{scaler_path}' are in the directory.")
    st.stop()

try:
    kmeans = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    st.error(f"Error loading model or scaler: {e}")
    st.stop()

# ==================== APP TITLE ====================
st.title('Customer Segmentation App')
st.write('Enter customer details to predict the segment')

# ==================== INPUT FIELDS ====================
age = st.number_input('Age', min_value=18, max_value=100, value=35)
income = st.number_input('Income', min_value=0, max_value=200000, value=50000)
total_spending = st.number_input('Total Spending (sum of purchases)', min_value=0, max_value=5000, value=1000)
num_web_purchases = st.number_input('Number of Web Purchases', min_value=0, max_value=100, value=10)
num_store_purchases = st.number_input('Number of Store Purchases', min_value=0, max_value=100, value=10)
num_web_visits = st.number_input('Number of Web Visits per Month', min_value=0, max_value=50, value=3)
recency = st.number_input('Recency (days since last purchase)', min_value=0, max_value=365, value=30)

# ==================== COLLECT INPUT DATA ====================
input_data = pd.DataFrame({
    'Age': [age],
    'Income': [income],
    'Total_Spending': [total_spending],
    'NumWebPurchases': [num_web_purchases],
    'NumStorePurchases': [num_store_purchases],
    'NumWebVisitsMonth': [num_web_visits],
    'Recency': [recency]
})

# ==================== PREDICTION ====================
if st.button('Predict Segment'):
    try:
        # Ensure feature order matches scaler/model expectation
        feature_order = ['Age', 'Income', 'Total_Spending', 'NumWebPurchases', 'NumStorePurchases', 'NumWebVisitsMonth', 'Recency']
        input_data = input_data[feature_order]
        input_scaled = scaler.transform(input_data)
        cluster = kmeans.predict(input_scaled)
        st.success(f'Predicted Segment: Cluster {cluster[0]}')
    except Exception as e:
        st.error(f"Error during prediction: {e}")