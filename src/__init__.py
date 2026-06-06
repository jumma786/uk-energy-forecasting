"""UK Electricity Demand Forecasting — source package.

Reusable, tested modules extracted from the project notebooks:

- ``src.config``   — paths and project-wide constants
- ``src.schema``   — canonical model feature schema
- ``src.data``     — dataset loading helpers
- ``src.features`` — feature engineering (lags, rolling stats, calendar)
- ``src.models``   — model loading and (recursive) prediction
- ``src.api``      — FastAPI prediction service
"""

__version__ = "1.0.0"
