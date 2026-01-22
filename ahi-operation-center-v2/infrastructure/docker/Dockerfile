# =============================================================================
# AHI Operation Center - Dockerfile
# =============================================================================
# Multi-stage build for development and production environments
# =============================================================================

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Development Stage
# =============================================================================
FROM base as development

# Install dev dependencies
COPY pyproject.toml .
RUN pip install -e ".[dev]"

# Copy source code
COPY packages/ packages/
COPY research/ research/

# Install packages in editable mode
RUN pip install -e packages/meba-core \
    && pip install -e packages/sap-pilot-kit \
    && pip install -e packages/ahi-cli

# Default command
CMD ["ahi", "info"]

# =============================================================================
# Production Stage
# =============================================================================
FROM base as production

# Copy only necessary files
COPY pyproject.toml .
COPY packages/ packages/

# Install in production mode
RUN pip install . \
    && pip install packages/meba-core \
    && pip install packages/sap-pilot-kit \
    && pip install packages/ahi-cli

# Run as non-root user
RUN useradd --create-home appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ahi info || exit 1

# Default command
CMD ["ahi", "info"]

# =============================================================================
# API Stage (for api-gateway)
# =============================================================================  
FROM base as api

# Install API dependencies
COPY pyproject.toml .
RUN pip install ".[api]"

COPY packages/ packages/
COPY apps/api-gateway/ apps/api-gateway/

# Install packages
RUN pip install packages/meba-core \
    && pip install packages/sap-pilot-kit

WORKDIR /app/apps/api-gateway

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
