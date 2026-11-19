FROM python:3.11-slim

# Patch the OS package Trivy flagged (zlib1g), then clean the apt cache
RUN apt-get update \
    && apt-get install -y --only-upgrade zlib1g \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# setuptools and wheel are build tools; the app never imports them at runtime
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y setuptools wheel

# Unprivileged user that owns only /app
RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin appuser \
    && chown appuser:appuser /app

COPY --chown=appuser:appuser app/ ./app/

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
