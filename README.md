# UK Electricity Demand Forecasting Using XGBoost

## Project Overview

This project develops an end-to-end machine learning solution for forecasting UK electricity demand using historical demand data, weather conditions, calendar effects, and renewable energy generation data.

The objective is to improve electricity demand forecasting accuracy and support better energy planning, grid management, and renewable energy integration.

The project includes:

- Exploratory Data Analysis (EDA)
- Feature Engineering
- Machine Learning Forecasting using XGBoost
- SHAP Explainability Analysis
- Power BI Dashboard Development
- Model Validation and Error Analysis

---

## Business Problem

Accurate electricity demand forecasting is critical for:

- Grid stability
- Capacity planning
- Energy trading
- Renewable energy integration
- Cost optimization

Traditional forecasting approaches often struggle to capture the effects of weather conditions, renewable generation, seasonal demand patterns, and calendar events.

This project addresses these challenges using machine learning and advanced feature engineering techniques.

---

## Dataset Description

The dataset combines multiple sources of information:

### Electricity Demand Data

- National Demand (ND)
- Settlement Date

### Renewable Energy Data

- Embedded Solar Generation
- Embedded Wind Generation

### Weather Data

- Mean Temperature
- Maximum Temperature
- Rainfall
- Wind Speed

### Calendar Data

- Day of Week
- Month
- Weekend Indicator
- Holiday Indicator
- Easter Indicator

---

## Data Preparation

The following preprocessing steps were performed:

### Missing Value Handling

- Renewable generation data contained missing values.
- Missing values were imputed using availability indicators and appropriate replacement techniques.

### Feature Engineering

#### Lag Features

Historical demand values were used to capture temporal dependencies:

- lag_1
- lag_7
- lag_30

#### Rolling Statistics

Rolling window calculations were created to capture demand trends:

- rolling_mean_7
- rolling_mean_30
- rolling_std_7

#### Calendar Features

- day_of_week
- month
- is_weekend
- is_holiday
- is_easter

#### Renewable Energy Features

- EMBEDDED_SOLAR_GENERATION
- EMBEDDED_WIND_GENERATION

#### Weather Features

- temperature_mean
- temperature_max
- rainfall
- wind_speed

---

## Exploratory Data Analysis

The analysis identified several important patterns:

### Demand Trends

- Electricity demand has gradually declined over time.
- Strong seasonal patterns exist throughout the year.
- Winter months experience higher demand levels.

### Renewable Energy Trends

- Solar generation has increased significantly since 2009.
- Wind generation has grown steadily over time.
- Renewable energy exhibits an inverse relationship with grid demand.

### Weather Effects

- Lower temperatures are associated with higher electricity demand.
- Temperature is the most influential weather-related variable.
- Rainfall and wind speed have smaller effects on demand.

---

## Machine Learning Model

### Model Selection

The final forecasting model uses:

**XGBoost Regressor**

### Why XGBoost?

XGBoost was selected because it:

- Handles nonlinear relationships effectively
- Captures feature interactions
- Provides excellent predictive performance
- Is robust against overfitting
- Supports model explainability

---

## Model Performance

### Final Results

| Metric | Value |
|----------|----------|
| MAPE | 5.14% |
| MAE | 1,352 MW |
| RMSE | 2,396 MW |
| Forecast Days | 731 |
| Forecast Accuracy | 94.86% |

### Performance Improvement

The inclusion of renewable energy and weather variables improved forecasting accuracy and reduced prediction errors compared with baseline models.

---

## Explainable AI (SHAP)

SHAP (SHapley Additive exPlanations) was used to understand model predictions and feature importance.

### Most Important Features

1. rolling_mean_7
2. rolling_mean_30
3. lag_1
4. day_of_week
5. lag_7
6. is_weekend
7. EMBEDDED_SOLAR_GENERATION
8. temperature_max

### SHAP Insights

- Historical demand patterns are the strongest drivers of predictions.
- Solar generation significantly impacts electricity demand forecasts.
- Temperature is the most important weather-related feature.
- Calendar effects improve prediction accuracy.

---

## Power BI Dashboard

A six-page interactive Power BI dashboard was developed to communicate insights and model performance.

### Page 1 – Executive Summary

Displays:

- Forecasting KPIs
- Actual vs Predicted Demand
- Model Performance Metrics

### Page 2 – Demand & Seasonality Analysis

Displays:

- Monthly Demand Trends
- Seasonal Demand Patterns
- Peak Demand Analysis

### Page 3 – Renewable Energy Impact Analysis

Displays:

- Solar Generation Trends
- Wind Generation Trends
- Demand vs Renewable Generation
- Renewable Energy Insights

### Page 4 – Weather Impact Analysis

Displays:

- Temperature vs Demand
- Monthly Temperature Trends
- Demand by Temperature Range
- Weather Feature Importance

### Page 5 – Model Explainability (SHAP Analysis)

Displays:

- Top Predictive Features
- Feature Group Contributions
- Business Impact Analysis

### Page 6 – Model Validation & Error Analysis

Displays:

- Error Distribution
- Model Performance Improvement
- Largest Forecast Errors
- Forecast Error Statistics

---

## Key Business Insights

### Demand Behaviour

- Electricity demand is highly seasonal.
- Winter periods exhibit significantly higher demand.

### Renewable Energy

- Solar generation demonstrates a strong inverse relationship with electricity demand.
- Renewable energy contributes to improved forecasting performance.

### Weather

- Temperature is the strongest weather-related demand driver.
- Demand increases significantly during colder periods.

### Forecasting

- Historical demand remains the strongest predictor.
- Renewable and weather variables improve model robustness and accuracy.

---

## Business Impact

The forecasting framework can support:

- Energy trading strategies
- Grid capacity planning
- Renewable energy integration
- Operational efficiency improvements
- Risk reduction through more accurate forecasts

---

## Technology Stack

### Programming

- Python

### Data Analysis

- Pandas
- NumPy

### Machine Learning

- Scikit-Learn
- XGBoost

### Explainable AI

- SHAP

### Visualization

- Matplotlib
- Power BI

### Development Environment

- Jupyter Notebook
- VS Code

---

## Project Structure

```text
UK-Electricity-Demand-Forecasting/
│
├── data/
│
├── notebooks/
│
├── models/
│
├── dashboard/
│   └── UK_Electricity_Demand_Forecasting.pbix
│
├── screenshots/
│
├── README.md
│
├── requirements.txt
│
└── app.py
```

---

## Future Improvements

Potential enhancements include:

- Real-time forecasting API
- Streamlit web application
- Automated retraining pipeline
- Cloud deployment using Azure
- Deep learning forecasting models (LSTM)
- MLOps integration

---

## Conclusion

This project demonstrates a complete end-to-end data science workflow, combining exploratory analysis, feature engineering, machine learning, explainable AI, and business intelligence reporting.

The final XGBoost model achieved a forecasting accuracy of 94.86% and successfully captured seasonal demand patterns, renewable energy impacts, and weather-related effects on UK electricity demand.

---

## Author

### Jumma Mohammad

Aspiring Data Scientist with experience in:

- Machine Learning
- Data Analytics
- Forecasting Models
- Power BI Dashboard Development
- SQL
- Python
- Explainable AI (SHAP)
- MLOps Fundamentals

### Contact Information

Email: jummamohammad477@gmail.com

LinkedIn: https://www.linkedin.com/in/jumma-mohammad/

GitHub: https://github.com/jumma786

Location: Birmingham, United Kingdom

---

## License

This project is intended for educational, research, and portfolio purposes.

© 2026 Jumma Mohammad. All rights reserved.