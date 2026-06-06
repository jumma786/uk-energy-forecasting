"""Canonical model feature schema.

The production XGBoost model (``xgboost_energy_forecaster_v3.pkl``) was trained
on these 29 features, in this exact order. Prediction code must always supply
columns in this order, so this list is the single source of truth shared by the
feature pipeline, the API and the tests.
"""

from __future__ import annotations

# Ordered exactly as the trained booster expects them.
FEATURE_NAMES: list[str] = [
    "lag_1",
    "lag_7",
    "lag_30",
    "rolling_mean_7",
    "rolling_mean_30",
    "rolling_std_7",
    "rolling_std_30",
    "year",
    "month",
    "quarter",
    "day_of_week",
    "day_of_year",
    "is_weekend",
    "is_holiday",
    "is_christmas",
    "is_new_year",
    "is_easter",
    "temperature_mean",
    "temperature_max",
    "temperature_min",
    "rainfall",
    "wind_speed",
    "temp_lag_1",
    "rainfall_lag_1",
    "wind_lag_1",
    "EMBEDDED_SOLAR_GENERATION",
    "EMBEDDED_WIND_GENERATION",
    "solar_available",
    "wind_available",
]

N_FEATURES: int = len(FEATURE_NAMES)
