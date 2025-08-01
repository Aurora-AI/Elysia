#!/bin/bash
# setup_runner.sh - Instala e configura um runner auto-hospedado do GitHub Actions
# Uso: sudo ./setup_runner.sh <REPO_URL> <REGISTRATION_TOKEN>

set -e

REPO_URL="$1"
TOKEN="$2"
RUNNER_NAME="aurora-ci-runner-24-7"
LABELS="gcp-always-free"

if [ -z "$REPO_URL" ] || [ -z "$TOKEN" ]; then
  echo "Uso: $0 <REPO_URL> <REGISTRATION_TOKEN>"
  exit 1
fi

# Instala dependências básicas
sudo apt-get update && sudo apt-get install -y curl tar gzip

# Cria diretório de trabalho
mkdir -p actions-runner && cd actions-runner

# Baixa a versão mais recente do runner
LATEST_URL=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | grep browser_download_url | grep linux-x64 | cut -d '"' -f 4)
curl -O -L "$LATEST_URL"

# Extrai o pacote
tar xzf actions-runner-linux-x64-*.tar.gz

# Configura o runner de forma não interativa
./config.sh --unattended --url "$REPO_URL" --token "$TOKEN" --name "$RUNNER_NAME" --labels "$LABELS"

# Instala e inicia o serviço systemd
sudo ./svc.sh install
sudo ./svc.sh start

# Verifica o status do serviço
sudo ./svc.sh status
