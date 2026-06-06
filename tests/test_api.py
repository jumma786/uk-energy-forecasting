"""API tests via FastAPI's TestClient."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.main import app
from src.config import MODEL_PATH

from .conftest import model_required

client = TestClient(app)


def test_root_ok():
    r = client.get("/")
    assert r.status_code == 200
    assert "service" in r.json()


def test_health_reports_feature_count():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["n_features"] == 29


@model_required
def test_predict_with_defaults():
    r = client.post("/predict", json={})
    assert r.status_code == 200
    assert "predicted_demand_mw" in r.json()


@model_required
def test_predict_with_cold_day():
    r = client.post("/predict", json={"temperature_mean": -2.0, "temperature_max": 1.0})
    assert r.status_code == 200
    assert r.json()["predicted_demand_mw"] > 0


def test_predict_rejects_bad_month():
    # month=13 fails Pydantic validation regardless of model availability.
    r = client.post("/predict", json={"month": 13})
    assert r.status_code == 422


# Reference the import so linters don't flag it when model is absent.
_ = MODEL_PATH
