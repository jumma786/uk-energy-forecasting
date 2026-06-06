"""Load the processed feature dataset.

Thin wrapper around the canonical parquet table so callers don't hard-code
paths. Returns a date-sorted frame ready for feature engineering or evaluation.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import DATE_COLUMN, FEATURES_PARQUET


def load_processed_features(path: str | Path | None = None) -> pd.DataFrame:
    """Return the processed feature table, sorted by settlement date.

    Args:
        path: Optional override for the parquet location. Defaults to
            ``src.config.FEATURES_PARQUET``.

    Raises:
        FileNotFoundError: If the parquet file does not exist.
    """
    path = Path(path) if path is not None else FEATURES_PARQUET
    if not path.exists():
        raise FileNotFoundError(f"Processed features not found at {path}")
    df = pd.read_parquet(path)
    if DATE_COLUMN in df.columns:
        df = df.sort_values(DATE_COLUMN).reset_index(drop=True)
    return df
