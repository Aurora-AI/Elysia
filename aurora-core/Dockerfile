
# --- Estágio 1: Builder ---
FROM python:3.11-bookworm AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN pip install --no-cache-dir poetry

# Copia os arquivos de dependência da raiz do projeto para o WORKDIR
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-ansi

# --- Estágio 2: Runtime (Final) ---
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copia o ambiente virtual com as dependências do estágio de 'builder'
COPY --from=builder /app/.venv ./.venv

# Adiciona os executáveis do ambiente virtual ao PATH
ENV PATH="/app/.venv/bin:$PATH"

 # A CORREÇÃO CRÍTICA: Copia o código-fonte de DENTRO do contexto de build
COPY ./aurora-core/src/aurora_platform ./aurora_platform
EXPOSE 8000
# Chama o módulo a partir da nova raiz do WORKDIR
CMD ["uvicorn", "aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8000"]
