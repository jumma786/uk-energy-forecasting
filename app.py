import streamlit as st
import pandas as pd
import joblib

# =========================
# LOAD MODEL
# =========================
model = joblib.load("models/xgboost_energy_forecaster_v3.pkl")

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="UK Electricity Demand Forecasting",
    page_icon="⚡",
    layout="wide"
)

# =========================
# TITLE
# =========================
st.title("⚡ UK Electricity Demand Forecasting")

st.markdown("""
This application predicts UK electricity demand using an XGBoost Machine Learning model trained on:

- Historical Electricity Demand
- Weather Data
- Renewable Energy Generation
- Calendar & Holiday Features
""")

# =========================
# KPI CARDS
# =========================
st.header("Model Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("MAPE", "5.14%")
col2.metric("MAE", "1352 MW")
col3.metric("RMSE", "2396 MW")
col4.metric("Forecast Horizon", "731 Days")

st.markdown("---")

# =========================
# USER INPUTS
# =========================
st.header("Forecast Inputs")

col1, col2 = st.columns(2)

with col1:
    temperature_mean = st.number_input(
        "Temperature Mean (°C)",
        value=10.0
    )

    temperature_max = st.number_input(
        "Temperature Max (°C)",
        value=15.0
    )

    temperature_min = st.number_input(
        "Temperature Min (°C)",
        value=5.0
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        value=1.0
    )

with col2:
    wind_speed = st.number_input(
        "Wind Speed",
        value=10.0
    )

    solar_generation = st.number_input(
        "Solar Generation (MW)",
        value=1000.0
    )

    wind_generation = st.number_input(
        "Wind Generation (MW)",
        value=2000.0
    )

# =========================
# PREDICTION
# =========================
if st.button("🔮 Predict Demand"):

    input_data = pd.DataFrame([{
        "lag_1": 33000,
        "lag_7": 33000,
        "lag_30": 33000,
        "rolling_mean_7": 33000,
        "rolling_mean_30": 33000,
        "rolling_std_7": 1500,
        "rolling_std_30": 1500,
        "year": 2026,
        "month": 6,
        "quarter": 2,
        "day_of_week": 1,
        "day_of_year": 180,
        "is_weekend": 0,
        "is_holiday": 0,
        "is_christmas": 0,
        "is_new_year": 0,
        "is_easter": 0,
        "temperature_mean": temperature_mean,
        "temperature_max": temperature_max,
        "temperature_min": temperature_min,
        "rainfall": rainfall,
        "wind_speed": wind_speed,
        "temp_lag_1": temperature_mean,
        "rainfall_lag_1": rainfall,
        "wind_lag_1": wind_speed,
        "EMBEDDED_SOLAR_GENERATION": solar_generation,
        "EMBEDDED_WIND_GENERATION": wind_generation,
        "solar_available": 1,
        "wind_available": 1
    }])

    prediction = model.predict(input_data)[0]

    st.success(
        f"Predicted Electricity Demand: {prediction:,.0f} MW"
    )

st.markdown("---")

# =========================
# SHAP FEATURE IMPORTANCE
# =========================
st.header("SHAP Feature Importance")

try:
    st.image(
        "reports/figures/shap_v3_importance.png",
        caption="SHAP Feature Importance",
        use_container_width=True
    )
except:
    st.warning(
        "SHAP image not found. Please check reports/figures folder."
    )

st.markdown("---")

# =========================
# POWER BI DASHBOARD
# =========================
st.header("Power BI Dashboard")

dashboard_images = [
    "dashboard/screenshots/executive summary.png",
    "dashboard/screenshots/demand and seasionality analysis.png",
    "dashboard/screenshots/renewable energy impact analysis.png",
    "dashboard/screenshots/weather impact analysis.png",
    "dashboard/screenshots/model explainability.png",
    "dashboard/screenshots/validation and error analysis.png"
]

for image in dashboard_images:
    try:
        st.image(
            image,
            use_container_width=True
        )
    except:
        pass

st.markdown("---")

# =========================
# PROJECT INFORMATION
# =========================
st.header("Project Information")

st.write("👤 Author: Jumma Mohammad")
st.write("🤖 Model: XGBoost Regressor")
st.write("📊 Features Used: 29")
st.write("📅 Forecast Horizon: 731 Days")
st.write("🎯 Forecast Accuracy: 94.86%")

st.markdown("""
### Connect

GitHub:
https://github.com/jumma786

LinkedIn:
https://www.linkedin.com/in/jumma-mohammad/

Email:
jummamohammad477@gmail.com
""")