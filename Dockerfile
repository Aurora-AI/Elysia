# --- Estágio 1: Builder ---
FROM python:3.11-bookworm AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN pip install --no-cache-dir poetry
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --no-ansi

# --- Estágio 2: Runtime (Final) ---
FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY --from=builder /app/.venv ./.venv

# A CORREÇÃO CRÍTICA: Adiciona os executáveis do .venv ao PATH do sistema
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 8080
CMD ["uvicorn", "src.aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8080"]
