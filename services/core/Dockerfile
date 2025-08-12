FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Pacotes básicos de build (ajudam em wheels nativas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Copiamos manifestos de dependência se existirem
#    (requirements.txt preferido; se não existir, seguimos adiante)
COPY requirements.txt* /tmp/deps/
RUN if [ -f /tmp/deps/requirements.txt ]; then pip install -r /tmp/deps/requirements.txt; fi

# 2) Copiamos TODO o repo (garante que o módulo 'aurora_platform' entre na imagem)
COPY . /app

# 3) Tornamos o código importável em ambos os layouts (src/ e raiz)
#    Sem depender de Poetry: funciona em qualquer ambiente.
ENV PYTHONPATH=/app/src:/app:/app/aurora-core/src

# 4) (Opcional) Se houver pyproject.toml, tenta instalar -e .
RUN if [ -f "pyproject.toml" ]; then pip install -e . || true; fi

# 5) Healthcheck: valida import do módulo
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
  CMD python -c "import aurora_platform; print('ok')"

# 6) O comando de execução real pode estar no docker-compose (command: ...)
#    Mantemos um default seguro que não cai (evita reiniciar em loop)
CMD ["python", "-c", "import time,aurora_platform as _; print('aurora-core container up'); time.sleep(31536000)"]
