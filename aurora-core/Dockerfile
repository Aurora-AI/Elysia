# --- Estágio 1: Builder ---
FROM python:3.11-slim AS builder

# Configura o Poetry para criar o .venv dentro do diretório do projeto
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

# Instala o Poetry
RUN pip install --no-cache-dir poetry

# Copia apenas os arquivos de dependência para otimizar o cache do Docker
COPY pyproject.toml poetry.lock ./

# Instala as dependências de produção (CPU only)
RUN poetry install --no-root --no-ansi --only main


# --- Estágio 2: Runtime (Final) ---
FROM python:3.11-slim

WORKDIR /app

# Copia o ambiente virtual já pronto e populado do estágio builder
COPY --from=builder /app/.venv ./.venv

# A CORREÇÃO DEFINITIVA: Adiciona os executáveis do .venv ao PATH do sistema
ENV PATH="/app/.venv/bin:$PATH"

# Copia o código-fonte da aplicação para o diretório de trabalho
# Atenção: O caminho reflete a estrutura do monorepo
COPY ./aurora-core/src/aurora_platform ./aurora_platform

EXPOSE 8000

# Comando final que agora encontrará 'uvicorn' no PATH
CMD ["uvicorn", "aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8000"]
