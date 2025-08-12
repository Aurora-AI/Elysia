FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=/opt/venv

# venv único para toda a imagem
RUN python -m venv ${VENV_PATH} \
 && ${VENV_PATH}/bin/pip install --upgrade pip setuptools wheel

# Dependências nativas mínimas (adicione libs de sistema se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia apenas o que é necessário para resolver deps
COPY pyproject.toml poetry.lock* /app/
COPY requirements.txt /app/requirements.txt

# Instala dependências no MESMO venv do runtime
RUN ${VENV_PATH}/bin/pip install --no-cache-dir -r /app/requirements.txt

# Agora copie só o código-fonte e configs mínimas
COPY aurora-core/src/ /app/aurora-core/src/
COPY alembic/ /app/alembic/
COPY alembic.ini /app/alembic.ini
COPY config/ /app/config/
COPY README.md /app/README.md

# PATH prioriza o venv e PYTHONPATH para encontrar os módulos
ENV PATH="${VENV_PATH}/bin:${PATH}"
ENV PYTHONPATH="/app/aurora-core/src:${PYTHONPATH}"

# Parâmetros do app/porta ajustáveis em build/run
ARG APP_MODULE=aurora-core.src.aurora_platform.main:app
ARG PORT=8000
ENV APP_MODULE=${APP_MODULE}
ENV PORT=${PORT}

# Smoke checks de build — falham cedo se algo estiver errado
RUN python -V \
 && which python \
 && python -c "import sys,site; print(sys.executable); print(site.getsitepackages())" \
 && python -c "import firebase_admin; print('firebase_admin OK (build)')"

EXPOSE ${PORT}

# Executa uvicorn usando o MESMO Python do venv
CMD ["python", "-m", "uvicorn", "aurora_platform.main:app", "--host","0.0.0.0","--port","8000"]
