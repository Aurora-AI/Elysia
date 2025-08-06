# --- Estágio 1: Builder ---
# Usamos uma imagem completa para ter as ferramentas de build necessárias
FROM python:3.11-bookworm AS builder

# Configura o Poetry para não ser interativo e criar o .venv dentro do projeto
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

# Instala o Poetry
RUN pip install --no-cache-dir poetry

# Copia os arquivos de dependência da raiz do projeto (contexto) para o WORKDIR
# Esta é a correção crucial para a estrutura do monorepo
COPY pyproject.toml poetry.lock ./

# Instala apenas as dependências, sem o projeto em si (mais rápido para build)
RUN poetry install --no-root --no-ansi

# --- Estágio 2: Runtime (Final) ---
# Usamos uma imagem 'slim' para uma imagem final menor e mais segura
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copia o ambiente virtual com as dependências já instaladas do estágio de 'builder'
COPY --from=builder /app/.venv ./.venv

# Adiciona os executáveis do ambiente virtual ao PATH do sistema
ENV PATH="/app/.venv/bin:$PATH"

# Copia o código-fonte específico do serviço 'aurora-core' para dentro da imagem
COPY ./aurora-core/src/aurora_platform ./aurora_platform

# Expõe a porta que a aplicação usará
EXPOSE 8000

# Comando para iniciar a aplicação, referenciando o módulo a partir da nova raiz
CMD ["uvicorn", "aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8000"]
