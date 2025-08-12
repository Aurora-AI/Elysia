#!/usr/bin/env bash
set -euo pipefail

echo "[init] Iniciando setup do ambiente Aurora-Plataform..."

if [[ -f "pyproject.toml" ]]; then
  echo "[init] Detected pyproject.toml → instalando Poetry"
  pipx install poetry || true
  poetry config virtualenvs.in-project true
  poetry install --no-interaction --no-ansi
fi

if [[ -f "requirements.txt" ]]; then
  echo "[init] Detected requirements.txt → pip install -r requirements.txt"
  python -m pip install -r requirements.txt
fi

python --version
pip --version
echo "[init] Ambiente pronto."
