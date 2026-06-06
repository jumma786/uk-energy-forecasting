"""Pydantic request/response models for the prediction API.

The request mirrors the 29 model features. Defaults reflect a "typical" UK
day so callers can probe the endpoint by sending only the fields they care
about, while still producing a valid, fully-specified feature row.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """A single feature row for one day's demand forecast."""

    # Autoregressive demand features (MW).
    lag_1: float = Field(33000, description="Demand 1 day ago (MW)")
    lag_7: float = Field(33000, description="Demand 7 days ago (MW)")
    lag_30: float = Field(33000, description="Demand 30 days ago (MW)")
    rolling_mean_7: float = Field(33000, description="7-day rolling mean demand (MW)")
    rolling_mean_30: float = Field(33000, description="30-day rolling mean demand (MW)")
    rolling_std_7: float = Field(1500, description="7-day rolling std of demand (MW)")
    rolling_std_30: float = Field(1500, description="30-day rolling std of demand (MW)")

    # Calendar features.
    year: int = 2026
    month: int = Field(6, ge=1, le=12)
    quarter: int = Field(2, ge=1, le=4)
    day_of_week: int = Field(0, ge=0, le=6, description="0=Monday")
    day_of_year: int = Field(157, ge=1, le=366)
    is_weekend: int = Field(0, ge=0, le=1)
    is_holiday: int = Field(0, ge=0, le=1)
    is_christmas: int = Field(0, ge=0, le=1)
    is_new_year: int = Field(0, ge=0, le=1)
    is_easter: int = Field(0, ge=0, le=1)

    # Weather features.
    temperature_mean: float = 10.0
    temperature_max: float = 15.0
    temperature_min: float = 5.0
    rainfall: float = 1.0
    wind_speed: float = 10.0
    temp_lag_1: float = 10.0
    rainfall_lag_1: float = 1.0
    wind_lag_1: float = 10.0

    # Renewable generation features.
    EMBEDDED_SOLAR_GENERATION: float = 1000.0
    EMBEDDED_WIND_GENERATION: float = 2000.0
    solar_available: int = Field(1, ge=0, le=1)
    wind_available: int = Field(1, ge=0, le=1)


class PredictionResponse(BaseModel):
    predicted_demand_mw: float = Field(..., description="Forecast demand (MW)")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    n_features: int
