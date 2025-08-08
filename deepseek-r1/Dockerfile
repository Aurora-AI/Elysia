# --- Estágio 1: Builder ---
# Usamos uma imagem Python padrão, sem CUDA
FROM python:3.11-bookworm AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

# Instala as dependências. Note que o vLLM pode exigir compilação,
# então garantimos que as ferramentas de build estejam presentes.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential
RUN poetry install --no-root --no-ansi

# --- Estágio 2: Runtime (Final) ---
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# O vLLM atualmente tem suporte limitado ou complexo para CPU.
# Para manter a simplicidade e garantir que funcione, usamos um servidor de inferência
# mais tradicional para o modo CPU, como o da biblioteca 'transformers'.
# ADICIONAMOS UM ARQUIVO 'main.py' SIMPLES PARA SERVIR O MODELO.
COPY ./deepseek-r1/main.py /app/main.py

# Comando para iniciar o servidor de inferência em modo CPU
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
