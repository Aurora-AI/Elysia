# Dockerfile - Versão 1.1 (Production-Ready com Healthcheck)

# --- Estágio 1: Builder ---
# Usamos uma imagem Python completa que contém as ferramentas de build necessárias.
FROM python:3.11-bookworm AS builder

# Configurações críticas do Poetry para um ambiente de CI/CD.
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

# Instalação segura do Poetry.
RUN pip install --no-cache-dir poetry

# Instala as dependências de sistema obrigatórias para compilar pacotes como os do ChromaDB.
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Copia apenas os arquivos de dependência PRIMEIRO para otimizar o cache do Docker.
COPY poetry.lock pyproject.toml ./

# Instala APENAS as dependências, sem o projeto raiz, para evitar problemas de contexto.
RUN poetry install --no-root --no-ansi

# --- Estágio 2: Final (Runtime) ---
# Usamos a imagem slim para um resultado final leve e seguro.
FROM python:3.11-slim-bookworm

WORKDIR /app

# Define o PYTHONPATH para que os imports absolutos da nossa aplicação (a partir de 'src') funcionem.
ENV PYTHONPATH="/app/src"

# Copia o ambiente virtual com as dependências já instaladas do estágio builder.
COPY --from=builder /app/.venv ./.venv

# Adiciona o executável do ambiente virtual ao PATH do sistema.
# Assim, comandos como 'uvicorn' e 'pytest' funcionam diretamente.
ENV PATH="/app/.venv/bin:$PATH"

# Copia todo o código-fonte da aplicação.
COPY . .

# Expõe a porta que a aplicação irá rodar.
EXPOSE 8080

# HEALTHCHECK: Instrui o Docker a verificar a saúde da aplicação a cada 30 segundos.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Define o comando padrão para iniciar a aplicação.
CMD ["uvicorn", "src.aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8080"]
