FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências básicas
RUN pip install fastapi uvicorn
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install transformers

# Copiar aplicação
COPY main.py /app/

EXPOSE 8000

CMD ["python", "main.py"]
