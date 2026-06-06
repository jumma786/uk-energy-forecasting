# UK Electricity Demand Forecasting — API image
FROM python:3.11-slim

# Avoid interactive prompts and reduce image noise.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# libgomp1 is required by XGBoost at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install runtime dependencies first for better layer caching.
COPY requirements-api.txt .
RUN pip install -r requirements-api.txt

# Copy the application code and the trained model.
COPY src/ ./src/
COPY models/ ./models/

EXPOSE 8000

# Container-friendly healthcheck against the API.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
