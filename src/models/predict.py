"""Load the trained model and produce predictions.

Wraps the pickled XGBoost regressor behind a small class that guarantees
features are always passed in the canonical order/shape the model expects. This
removes the brittle, hard-coded feature dict that lived in ``app.py``.
"""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Iterable

import joblib
import pandas as pd

from src.config import MODEL_PATH
from src.schema import FEATURE_NAMES


@functools.lru_cache(maxsize=2)
def load_model(path: str | Path | None = None):
    """Load and cache the trained model.

    Args:
        path: Optional model path. Defaults to ``src.config.MODEL_PATH``.

    Raises:
        FileNotFoundError: If the model file is missing.
    """
    path = Path(path) if path is not None else MODEL_PATH
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at {path}")
    return joblib.load(path)


def _to_feature_frame(rows: pd.DataFrame | dict | Iterable[dict]) -> pd.DataFrame:
    """Coerce input into a DataFrame with exactly the model's feature columns."""
    if isinstance(rows, dict):
        frame = pd.DataFrame([rows])
    elif isinstance(rows, pd.DataFrame):
        frame = rows.copy()
    else:
        frame = pd.DataFrame(list(rows))

    missing = [c for c in FEATURE_NAMES if c not in frame.columns]
    if missing:
        raise ValueError(f"Missing required features: {missing}")
    # Reorder (and drop extras) to match the trained model exactly.
    return frame[FEATURE_NAMES]


class DemandForecaster:
    """Convenience wrapper around the trained demand model."""

    def __init__(self, path: str | Path | None = None):
        self.model = load_model(path)

    def predict(self, rows: pd.DataFrame | dict | Iterable[dict]) -> list[float]:
        """Predict demand (MW) for one or more feature rows.

        Accepts a single dict, an iterable of dicts, or a DataFrame. Returns a
        list of floats so the result is JSON-serialisable.
        """
        frame = _to_feature_frame(rows)
        preds = self.model.predict(frame)
        return [float(p) for p in preds]

    def predict_one(self, row: dict) -> float:
        """Predict demand for a single feature dict."""
        return self.predict(row)[0]
