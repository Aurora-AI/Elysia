FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl bash ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.7.1
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app


COPY ./pyproject.toml ./poetry.lock* /app/
COPY ./src/aurora_platform /app/aurora_platform
COPY ./entrypoint.sh /entrypoint.sh
RUN poetry config virtualenvs.create false && \
    poetry add firebase-admin && \
    poetry install --no-interaction --no-ansi && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install --no-cache-dir -r requirements.txt
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
