#!/usr/bin/env bash
set -euo pipefail
echo "[migrate] Consolidando código em src/aurora_platform/"

# Criar diretório de destino
mkdir -p src/aurora_platform

# Migrar de aurora_platform/ (raiz)
if [ -d "aurora_platform" ]; then
  echo "[migrate] Copiando aurora_platform/ -> src/aurora_platform/"
  rsync -a --delete aurora_platform/ src/aurora_platform/
fi

# Migrar de aurora-core/src/aurora_platform/
if [ -d "aurora-core/src/aurora_platform" ]; then
  echo "[migrate] Mesclando aurora-core/src/aurora_platform/ -> src/aurora_platform/"
  rsync -a aurora-core/src/aurora_platform/ src/aurora_platform/
fi

echo "[migrate] Verificando resultado..."
python tools/check_duplicate_packages.py || echo "[warn] Ainda há duplicatas - verificar manualmente"
echo "[migrate] Concluído. Revisar conflitos em src/aurora_platform/"