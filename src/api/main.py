"""FastAPI service exposing the demand forecasting model.

Run locally:
    uvicorn src.api.main:app --reload

Endpoints:
    GET  /health   — liveness + model status
    POST /predict  — single-day demand forecast
    GET  /          — basic service metadata

Interactive docs are served at /docs.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from src.api.schemas import HealthResponse, PredictionRequest, PredictionResponse
from src.models import DemandForecaster
from src.schema import N_FEATURES

app = FastAPI(
    title="UK Electricity Demand Forecasting API",
    description="Serves the XGBoost demand model as a REST endpoint.",
    version="1.0.0",
)

# Loaded lazily on first use so the app can import even if the model file is
# absent (e.g. during certain CI steps); the error then surfaces per-request.
_forecaster: DemandForecaster | None = None


def get_forecaster() -> DemandForecaster:
    global _forecaster
    if _forecaster is None:
        _forecaster = DemandForecaster()
    return _forecaster


@app.get("/", tags=["meta"])
def root() -> dict:
    return {
        "service": "UK Electricity Demand Forecasting API",
        "version": app.version,
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    """Report service health and whether the model can be loaded."""
    try:
        get_forecaster()
        model_loaded = True
    except Exception:
        model_loaded = False
    return HealthResponse(
        status="ok" if model_loaded else "degraded",
        model_loaded=model_loaded,
        n_features=N_FEATURES,
    )


@app.post("/predict", response_model=PredictionResponse, tags=["forecast"])
def predict(request: PredictionRequest) -> PredictionResponse:
    """Predict electricity demand (MW) for a single day's feature row."""
    try:
        forecaster = get_forecaster()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    try:
        prediction = forecaster.predict_one(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return PredictionResponse(predicted_demand_mw=round(prediction, 2))
