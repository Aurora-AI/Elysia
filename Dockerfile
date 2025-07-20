FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH /app/src

# Instala o Poetry
RUN pip install poetry

# Copia apenas os arquivos de dependência para aproveitar o cache do Docker
COPY poetry.lock pyproject.toml ./

# Instala as dependências do projeto sem criar um venv dentro do contêiner
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --without dev --no-interaction --no-ansi

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que a aplicação irá rodar
EXPOSE 8080

# Define o comando padrão para iniciar a aplicação
CMD ["poetry", "run", "uvicorn", "src.aurora_platform.main:app", "--host", "0.0.0.0", "--port", "8080"]
