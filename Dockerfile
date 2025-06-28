# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# --- Builder stage ---
FROM base AS builder

# Install system dependencies required for psycopg2 and other packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt only (for better cache usage)
COPY --link requirements.txt ./

# Create virtual environment and install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# --- Final stage ---
FROM base AS final

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy app source code (excluding .env, .git, etc. via .dockerignore)
COPY --link . .

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Set permissions
RUN chown -R appuser:appgroup /app
USER appuser

# Expose the default FastAPI port
EXPOSE 8000

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
