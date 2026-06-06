"""Project paths and constants.

Centralises every filesystem location so notebooks, the API and tests all
agree on where data and models live. Paths are derived from this file's
location, so the project works regardless of the current working directory.
"""

from __future__ import annotations

import os
from pathlib import Path

# Project root = parent of the ``src`` directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Canonical processed feature table and the production model.
FEATURES_PARQUET = PROCESSED_DATA_DIR / "energy_features_v3.parquet"
DEFAULT_MODEL_PATH = MODELS_DIR / "xgboost_energy_forecaster_v3.pkl"

# Allow overriding the model path via environment variable (useful in Docker/CI).
MODEL_PATH = Path(os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH))

# Column names in the processed data.
DATE_COLUMN = "SETTLEMENT_DATE"
TARGET_COLUMN = "ND"
