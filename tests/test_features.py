"""Feature engineering tests.

Where the processed dataset is available, we assert the rebuilt features match
the stored training columns position-for-position — guarding against silent
drift in the lag/rolling/calendar conventions.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.features import (
    add_calendar_features,
    add_lag_features,
    add_rolling_features,
    build_features,
)

from .conftest import data_required


def _toy_frame(n: int = 40) -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    return pd.DataFrame(
        {
            "SETTLEMENT_DATE": dates,
            "ND": np.arange(n, dtype=float) * 100 + 30000,
            "temperature_mean": np.linspace(0, 10, n),
            "rainfall": np.ones(n),
            "wind_speed": np.full(n, 5.0),
        }
    )


def test_lag_features_shift_correctly():
    out = add_lag_features(_toy_frame())
    assert out["lag_1"].iloc[1] == out["ND"].iloc[0]
    assert out["lag_7"].iloc[7] == out["ND"].iloc[0]
    assert pd.isna(out["lag_1"].iloc[0])


def test_rolling_includes_current_row():
    out = add_rolling_features(_toy_frame())
    # rolling_mean_7 at index 6 is the mean of the first 7 ND values.
    expected = out["ND"].iloc[0:7].mean()
    assert np.isclose(out["rolling_mean_7"].iloc[6], expected)


def test_calendar_features():
    out = add_calendar_features(_toy_frame())
    # 2024-01-01 is a Monday.
    assert out["day_of_week"].iloc[0] == 0
    assert out["month"].iloc[0] == 1
    assert out["is_weekend"].iloc[5] == 1  # 2024-01-06 is Saturday


@data_required
def test_rebuilt_features_match_training_data():
    from src.data import load_processed_features

    df = load_processed_features()
    rebuilt = build_features(
        df[["SETTLEMENT_DATE", "ND", "temperature_mean", "rainfall", "wind_speed"]]
    )
    for col in ["lag_1", "lag_7", "lag_30", "rolling_mean_7", "rolling_std_30"]:
        a = rebuilt[col].to_numpy()
        b = df[col].to_numpy()
        mask = ~(np.isnan(a) | np.isnan(b))
        assert np.allclose(a[mask], b[mask], atol=1e-3), col
