# --- Estágio 1: Builder ---
FROM python:3.11-bookworm AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN pip install --no-cache-dir poetry

# A CORREÇÃO: Copia os arquivos de dependência da raiz do contexto
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-ansi

# --- Estágio 2: Runtime (Final) ---
FROM python:3.11-slim-bookworm

WORKDIR /app


COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

# A CORREÇÃO: Copia diretamente o pacote 'aurora_platform' para a raiz do WORKDIR
COPY ./aurora-core/src/aurora_platform ./aurora_platform

EXPOSE 8000
# A CORREÇÃO: Chama o módulo a partir da nova raiz
CMD ["uvicorn", "aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8000"]