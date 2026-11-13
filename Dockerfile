FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH" \
    GRPC_HOST="0.0.0.0" \
    GRPC_PORT="50051" \
    GATEWAY_HOST="0.0.0.0" \
    GATEWAY_PORT="8000" \
    MAAS_MODELS_DIR="/app/models"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgomp1 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock .python-version README.md LICENSE ./
RUN uv sync --frozen --no-dev --no-install-project

COPY protos ./protos
COPY scripts ./scripts
COPY src ./src

RUN uv sync --frozen --no-dev \
    && uv run --no-sync python scripts/descargar_modelo.py \
    && useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 50051 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=25s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8000/health || exit 1

CMD ["python", "-m", "defect_inspector.api.run_backend"]
