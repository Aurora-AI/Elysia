# Estágio de construção
FROM python:3.11-bookworm AS builder

ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-ansi --only main

# Estágio final de execução
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copia o código da aplicação de embedding
COPY ./gpt-oss/app /app/app

EXPOSE 8002
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
