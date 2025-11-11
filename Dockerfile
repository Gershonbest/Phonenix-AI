# syntax=docker/dockerfile:1

# Use the official Python base image with Python 3.11
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip (more reliable in Docker)
RUN pip install --no-cache-dir uv

# Verify uv is installed
RUN uv --version

WORKDIR /app

# Copy files needed for package build
COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

RUN uv run python src/agent.py download-files

CMD ["uv", "run", "python", "src/agent.py", "start"]
