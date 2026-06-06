"""Shared pytest fixtures and skip logic.

Tests that need the trained model or the processed dataset are skipped
gracefully when those artifacts are absent (e.g. a fresh clone without LFS),
so the suite stays green in any environment.
"""

from __future__ import annotations

import pytest

from src.config import FEATURES_PARQUET, MODEL_PATH

model_required = pytest.mark.skipif(
    not MODEL_PATH.exists(), reason=f"Model not available at {MODEL_PATH}"
)
data_required = pytest.mark.skipif(
    not FEATURES_PARQUET.exists(),
    reason=f"Processed data not available at {FEATURES_PARQUET}",
)
