FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates gnupg lsb-release sudo unzip jq iproute2 bash-completion \
    zsh locales git-lfs \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i 's/# \(en_US.UTF-8\)/\1/' /etc/locale.gen \
    && sed -i 's/# \(pt_BR.UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen

RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

RUN git lfs install --system

RUN if ! id -u ${USERNAME} >/dev/null 2>&1; then \
      groupadd --gid ${USER_GID} ${USERNAME} && \
      useradd -s /bin/bash --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}; \
    fi && \
    usermod -aG sudo ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-vscode-nopasswd

RUN chsh -s /bin/bash ${USERNAME}

RUN python -m pip install --upgrade pip setuptools wheel pipx && \
    pipx ensurepath

USER ${USERNAME}
