"""Model loading and prediction tests (require the trained model)."""

from __future__ import annotations

import pytest

from src.models import DemandForecaster, load_model
from src.schema import FEATURE_NAMES

from .conftest import model_required


def _valid_row() -> dict:
    return {name: 1.0 for name in FEATURE_NAMES}


@model_required
def test_model_loads_and_is_cached():
    a = load_model()
    b = load_model()
    assert a is b  # lru_cache returns the same instance


@model_required
def test_predict_one_returns_float():
    f = DemandForecaster()
    pred = f.predict_one(_valid_row())
    assert isinstance(pred, float)
    # UK national demand realistically sits well within these bounds.
    assert 5000 < pred < 70000


@model_required
def test_predict_batch_matches_length():
    f = DemandForecaster()
    preds = f.predict([_valid_row(), _valid_row(), _valid_row()])
    assert len(preds) == 3


@model_required
def test_missing_feature_raises():
    f = DemandForecaster()
    bad = _valid_row()
    del bad["lag_1"]
    with pytest.raises(ValueError):
        f.predict_one(bad)
