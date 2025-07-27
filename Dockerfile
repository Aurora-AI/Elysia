
# --- Estágio 1: Builder ---
FROM python:3.11-bookworm AS builder

# Configurações críticas do Poetry para um ambiente de CI/CD
ENV POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Instalação segura do Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Instala as dependências de sistema obrigatórias para compilar pacotes como chroma-hnswlib
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Copia apenas os arquivos de dependência PRIMEIRO para otimizar o cache do Docker
COPY poetry.lock pyproject.toml ./

# Instala APENAS as dependências, sem o projeto raiz, para evitar problemas de contexto
RUN poetry install --no-root --no-ansi --only main

# Copia código e instala a aplicação
COPY . .
RUN poetry install --no-ansi --only main

# --- Estágio 2: Runtime ---
FROM python:3.11-slim-bookworm AS runtime

WORKDIR /app

# Define o PYTHONPATH para que os imports absolutos da nossa aplicação funcionem
ENV PYTHONPATH /app/src

# Copia o ambiente virtual com as dependências já instaladas do estágio builder
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app .

# Adiciona o executável do ambiente virtual ao PATH do sistema
ENV PATH="/app/.venv/bin:$PATH"

# Expõe a porta que a aplicação irá rodar
EXPOSE 8080

# Configurações de ambiente
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src \
    CHROMA_SERVER_HOST=chromadb \
    REDIS_URL=redis://redis:6379/0

# Health check para orquestração
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl --fail http://localhost:8080/health || exit 1

CMD ["uvicorn", "aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8080"]
