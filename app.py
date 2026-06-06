import datetime

import streamlit as st

from src.models import DemandForecaster


# =========================
# LOAD MODEL (cached)
# =========================
@st.cache_resource
def load_forecaster() -> DemandForecaster:
    return DemandForecaster()


forecaster = load_forecaster()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="UK Electricity Demand Forecasting",
    page_icon="⚡",
    layout="wide",
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

st.markdown(
    "Set the **recent demand history** and **date** below — these drive most of "
    "the forecast — then adjust weather and renewables to see their effect."
)

# ---- Date & calendar ----
st.subheader("📅 Forecast Date")
forecast_date = st.date_input(
    "Date to forecast",
    value=datetime.date(2026, 6, 8),
    help="Calendar features (month, day of week, weekend) are derived from this date.",
)

cal_col1, cal_col2, cal_col3 = st.columns(3)
with cal_col1:
    is_holiday = int(st.checkbox("Public holiday"))
with cal_col2:
    is_christmas = int(st.checkbox("Christmas period"))
    is_new_year = int(st.checkbox("New Year period"))
with cal_col3:
    is_easter = int(st.checkbox("Easter period"))

# ---- Recent demand history (the dominant features) ----
st.subheader("📈 Recent Demand History (MW)")
st.caption(
    "These are the strongest predictors. In production they come from the most "
    "recent metered demand; here you set them manually."
)

hist_col1, hist_col2 = st.columns(2)
with hist_col1:
    lag_1 = st.number_input("Demand yesterday (lag 1 day)", value=33000.0, step=500.0)
    lag_7 = st.number_input("Demand 7 days ago", value=33000.0, step=500.0)
    lag_30 = st.number_input("Demand 30 days ago", value=33000.0, step=500.0)
with hist_col2:
    rolling_mean_7 = st.number_input("7-day average demand", value=33000.0, step=500.0)
    rolling_mean_30 = st.number_input("30-day average demand", value=33000.0, step=500.0)
    rolling_std_7 = st.number_input("7-day demand variability (std)", value=1500.0, step=100.0)

rolling_std_30 = rolling_std_7  # low-importance feature; tie to the 7-day std

# ---- Weather ----
st.subheader("🌦️ Weather")
w_col1, w_col2 = st.columns(2)
with w_col1:
    temperature_mean = st.number_input("Temperature Mean (°C)", value=10.0)
    temperature_max = st.number_input("Temperature Max (°C)", value=15.0)
    temperature_min = st.number_input("Temperature Min (°C)", value=5.0)
with w_col2:
    rainfall = st.number_input("Rainfall (mm)", value=1.0)
    wind_speed = st.number_input("Wind Speed", value=10.0)

# ---- Renewables ----
st.subheader("🔋 Renewable Generation")
r_col1, r_col2 = st.columns(2)
with r_col1:
    solar_generation = st.number_input("Solar Generation (MW)", value=1000.0)
with r_col2:
    wind_generation = st.number_input("Wind Generation (MW)", value=2000.0)

# =========================
# PREDICTION
# =========================
if st.button("🔮 Predict Demand"):

    # Derive calendar features from the chosen date.
    d = forecast_date
    quarter = (d.month - 1) // 3 + 1
    day_of_week = d.weekday()  # Monday = 0
    day_of_year = d.timetuple().tm_yday
    is_weekend = int(day_of_week >= 5)

    input_row = {
        # Demand history (user-driven)
        "lag_1": lag_1,
        "lag_7": lag_7,
        "lag_30": lag_30,
        "rolling_mean_7": rolling_mean_7,
        "rolling_mean_30": rolling_mean_30,
        "rolling_std_7": rolling_std_7,
        "rolling_std_30": rolling_std_30,
        # Calendar (date-driven)
        "year": d.year,
        "month": d.month,
        "quarter": quarter,
        "day_of_week": day_of_week,
        "day_of_year": day_of_year,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "is_christmas": is_christmas,
        "is_new_year": is_new_year,
        "is_easter": is_easter,
        # Weather (user-driven); lags default to same-day values
        "temperature_mean": temperature_mean,
        "temperature_max": temperature_max,
        "temperature_min": temperature_min,
        "rainfall": rainfall,
        "wind_speed": wind_speed,
        "temp_lag_1": temperature_mean,
        "rainfall_lag_1": rainfall,
        "wind_lag_1": wind_speed,
        # Renewables (user-driven)
        "EMBEDDED_SOLAR_GENERATION": solar_generation,
        "EMBEDDED_WIND_GENERATION": wind_generation,
        "solar_available": 1,
        "wind_available": 1,
    }

    prediction = forecaster.predict_one(input_row)

    delta = prediction - rolling_mean_7
    st.success(f"Predicted Electricity Demand: {prediction:,.0f} MW")
    st.metric(
        "Forecast vs your 7-day average",
        f"{prediction:,.0f} MW",
        delta=f"{delta:,.0f} MW",
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
        use_container_width=True,
    )
except Exception:
    st.warning("SHAP image not found. Please check reports/figures folder.")

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
    "dashboard/screenshots/validation and error analysis.png",
]

for image in dashboard_images:
    try:
        st.image(image, use_container_width=True)
    except Exception:
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
