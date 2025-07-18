# ---------- build stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app
COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir .

# ---------- runtime stage ----------
FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r app && useradd -r -g app app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src src
COPY .env.example .env

USER app

CMD ["python", "-m", "weather_pipeline.main"]
