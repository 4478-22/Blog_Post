# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps for psycopg2, Pillow (future), etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Add entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user
RUN useradd -m appuser
USER appuser

# Expose (Render sets $PORT dynamically; we still expose 8000 for local)
EXPOSE 8000

# Healthcheck (simple)
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s CMD curl -f http://localhost:${PORT:-8000}/api/health/ || exit 1

# Start: migrate, collectstatic, run Daphne (ASGI)
CMD ["/entrypoint.sh", "daphne", "-b", "0.0.0.0", "-p", "${PORT:-8000}", "config.asgi:application"]
