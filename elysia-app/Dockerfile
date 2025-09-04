# /elysia-app/Dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

# Instala a Elysia a partir do PyPI (ajuste se preferir clonar fonte)
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir elysia-ai

ENV PORT=8000
EXPOSE 8000

# Se a CLI "elysia" expõe o servidor:
CMD ["elysia", "start", "--host", "0.0.0.0", "--port", "8000"]