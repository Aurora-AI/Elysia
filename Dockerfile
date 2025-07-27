# --- Estágio 1: Builder ---
# Usamos uma imagem Python mais completa que contém as ferramentas de build
FROM python:3.11-bookworm AS builder

# Configurações críticas do Poetry para um ambiente de CI/CD
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

# Instalação segura do Poetry
RUN pip install --no-cache-dir poetry

# Instala as dependências de sistema obrigatórias para compilar pacotes
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Copia apenas os arquivos de dependência PRIMEIRO para otimizar o cache do Docker
COPY poetry.lock pyproject.toml ./

# Instala as dependências do projeto
RUN poetry install --no-ansi

# --- Estágio 2: Runtime (Final) ---
# Usamos a imagem slim para um resultado final leve e seguro
FROM python:3.11-slim-bookworm AS runtime

WORKDIR /app

# Define o PYTHONPATH para que os imports da nossa aplicação funcionem
ENV PYTHONPATH=/app

# Copia o ambiente virtual com as dependências já instaladas do estágio builder
COPY --from=builder /app/.venv ./.venv

# A CORREÇÃO CRÍTICA: Adiciona os executáveis do .venv ao PATH do sistema
ENV PATH="/app/.venv/bin:$PATH"

# Copia todo o código-fonte da aplicação
COPY . .

# Expõe a porta que a aplicação irá rodar
EXPOSE 8080

# Define o comando padrão para iniciar a aplicação
CMD ["uvicorn", "src.aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8080"]