# Base Python (Debian Bookworm) com user 'vscode'
FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copia o CA corporativo (substitua corp.crt pelo seu real)
# Mantemos também o example no contexto para orientar outros times.
COPY .devcontainer/certs/corp.crt /usr/local/share/ca-certificates/corp.crt

# Atualiza a store de certificados do sistema (inclui nosso CA)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Ferramentas Python: versões reproduzíveis, sem pós-criação
RUN python -m pip install --upgrade pip setuptools wheel

# (Opcional) Args de proxy, se necessário no futuro
# ARG HTTP_PROXY
# ARG HTTPS_PROXY
# ARG NO_PROXY
# ENV http_proxy=${HTTP_PROXY} https_proxy=${HTTPS_PROXY} no_proxy=${NO_PROXY}

# Pronto. Features GHCR serão injetadas pelo Dev Containers (Dockerfile-with-features).
