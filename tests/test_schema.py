"""Schema invariants — fast, no artifacts required."""

from src.schema import FEATURE_NAMES, N_FEATURES


def test_feature_count_is_29():
    assert N_FEATURES == 29
    assert len(FEATURE_NAMES) == 29


def test_feature_names_are_unique():
    assert len(set(FEATURE_NAMES)) == len(FEATURE_NAMES)


def test_key_features_present():
    for name in ("lag_1", "rolling_mean_7", "EMBEDDED_SOLAR_GENERATION", "is_holiday"):
        assert name in FEATURE_NAMES
