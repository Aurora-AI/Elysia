# --- Estágio 1: Builder ---
FROM python:3.11-bookworm AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN pip install --no-cache-dir poetry

# Usa o pyproject.toml da raiz do monorepo
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-ansi --only main

# --- Estágio 2: Runtime (Final) ---
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

# Copia o código-fonte (atualmente vazio) para consistência
COPY ./aurora-crawler /app/aurora-crawler

EXPOSE 8001

# Comando temporário para manter o container rodando
# até que o código do serviço seja implementado.
CMD ["tail", "-f", "/dev/null"]
