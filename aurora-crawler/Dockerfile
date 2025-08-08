# --- Estágio 1: Builder ---
FROM python:3.11-bookworm AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN pip install --no-cache-dir poetry

RUN python -m venv .venv

COPY pyproject.toml poetry.lock ./

# OTIMIZAÇÃO: Usamos --no-dev para instalar apenas as dependências de produção.
RUN . .venv/bin/activate && poetry install --only main --no-root --no-ansi

# VERIFICAÇÃO: Garante que o ambiente foi criado antes de prosseguir.
RUN ls -la .venv/bin

# --- Estágio 2: Runtime (Final) ---
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

# ---- SEÇÃO ESPECIALIZADA POR SERVIÇO ----
COPY ./aurora-crawler /app/aurora-crawler
CMD ["tail", "-f", "/dev/null"]
