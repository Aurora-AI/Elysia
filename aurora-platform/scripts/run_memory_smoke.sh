#!/usr/bin/env bash
set -euo pipefail

# run_memory_smoke.sh
# Helper to run Qdrant schema, ingest, start API and collect smoke logs into smoke_memory.txt
# Usage:
#   ./run_memory_smoke.sh            # runs checks, schema, ingest (expects Qdrant running)
#   ./run_memory_smoke.sh --install  # also (re)creates venv and installs requirements

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$ROOT_DIR"

LOGFILE="$ROOT_DIR/smoke_memory.txt"
UVICORN_LOG="$ROOT_DIR/uvicorn_smoke.log"
PYTHON=${PYTHON:-python3}
VENV_DIR="$ROOT_DIR/.venv"
INSTALL_DEPS=false

for arg in "$@"; do
  case "$arg" in
    --install) INSTALL_DEPS=true ;;
    *) echo "Unknown arg: $arg" ;;
  esac
done

echo "SMOKE RUN: $(date --iso-8601=seconds)" > "$LOGFILE"
echo "Repo root: $ROOT_DIR" >> "$LOGFILE"

# 0) quick checks
echo "\n--- Quick checks ---" | tee -a "$LOGFILE"
$PYTHON --version 2>&1 | tee -a "$LOGFILE"
make --version 2>&1 | tee -a "$LOGFILE" || true

# Check Qdrant health
QDRANT_URL=${QDRANT_URL:-http://localhost:6333}
echo "QDRANT_URL=$QDRANT_URL" | tee -a "$LOGFILE"
if curl -sSf "$QDRANT_URL/healthz" >/dev/null 2>&1; then
  echo "Qdrant health: OK" | tee -a "$LOGFILE"
else
  echo "ERROR: Qdrant is not responding at $QDRANT_URL/healthz" | tee -a "$LOGFILE"
  echo "Please start Qdrant first (docker compose up -d qdrant or docker run ...). Exiting." | tee -a "$LOGFILE"
  exit 2
fi

# 1) create/activate venv and optionally install
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv at $VENV_DIR" | tee -a "$LOGFILE"
  $PYTHON -m venv "$VENV_DIR"
fi

# Activate in-posix manner
# shellcheck disable=SC1090
. "$VENV_DIR/bin/activate"

if [ "$INSTALL_DEPS" = true ]; then
  echo "Installing dependencies from requirements.txt" | tee -a "$LOGFILE"
  pip install -U pip 2>&1 | tee -a "$LOGFILE"
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt 2>&1 | tee -a "$LOGFILE"
  else
    echo "No requirements.txt found in $ROOT_DIR" | tee -a "$LOGFILE"
  fi
fi

# 2) make schema
echo "\n--- make schema (Qdrant collections) ---" | tee -a "$LOGFILE"
if make -n schema >/dev/null 2>&1; then
  echo "Running: make schema" | tee -a "$LOGFILE"
  make schema 2>&1 | tee -a "$LOGFILE"
else
  echo "Fallback: PYTHONPATH=. python -m src.memory.qdrant_schema" | tee -a "$LOGFILE"
  PYTHONPATH=. python -m src.memory.qdrant_schema 2>&1 | tee -a "$LOGFILE"
fi

# 3) ingest trf1 and trt9
echo "\n--- Ingest TRF1 (./data/datajud/trf1) ---" | tee -a "$LOGFILE"
if make -n ingest-trf1 >/dev/null 2>&1; then
  make ingest-trf1 2>&1 | tee -a "$LOGFILE" | tail -n 20 >> "$LOGFILE"
else
  PYTHONPATH=. python -m src.memory.ingest_to_qdrant --input ./data/datajud/trf1 2>&1 | tee -a "$LOGFILE" | tail -n 20 >> "$LOGFILE"
fi

echo "\n--- Ingest TRT9 (./data/datajud/trt9) ---" | tee -a "$LOGFILE"
if make -n ingest-trt9 >/dev/null 2>&1; then
  make ingest-trt9 2>&1 | tee -a "$LOGFILE" | tail -n 20 >> "$LOGFILE"
else
  PYTHONPATH=. python -m src.memory.ingest_to_qdrant --input ./data/datajud/trt9 2>&1 | tee -a "$LOGFILE" | tail -n 20 >> "$LOGFILE"
fi

# 4) start API (uvicorn) in background
echo "\n--- Start API (uvicorn) on 8089 ---" | tee -a "$LOGFILE"
if pgrep -f "search_local:app" >/dev/null 2>&1; then
  echo "search_local already running" | tee -a "$LOGFILE"
else
  PYTHONPATH=. uvicorn src.memory.search_local:app --host 0.0.0.0 --port 8089 --reload > "$UVICORN_LOG" 2>&1 &
  UVICORN_PID=$!
  echo "uvicorn started (pid=$UVICORN_PID), log -> $UVICORN_LOG" | tee -a "$LOGFILE"
  # give it a moment
  sleep 2
fi

# 5) smoke requests
echo "\n--- Smoke requests ---" | tee -a "$LOGFILE"
curl -sS "http://localhost:8089/healthz" | tee -a "$LOGFILE"
curl -sS "http://localhost:8089/search?query=prazo%20recurso&k=5&alpha=0.5" | tee -a "$LOGFILE"
curl -sS "http://localhost:8089/search?query=penhora%20on-line&k=5&alpha=0.5" | tee -a "$LOGFILE"

# 6) counts per collection
echo "\n--- Qdrant collection counts ---" | tee -a "$LOGFILE"
PYTHONPATH=. python - <<'PY' 2>&1 | tee -a "$LOGFILE"
import os
from qdrant_client import QdrantClient
c = QdrantClient(url=os.getenv('QDRANT_URL','http://localhost:6333'))
for coll in ['cases_raw','cases_norm','cases_chunks']:
    info = c.get_collection(coll)
    print(coll, '→', getattr(info, 'points_count', 'N/A'), 'pontos')
PY

# 7) cleanup: kill uvicorn if we started it
if [ -n "${UVICORN_PID:-}" ]; then
  echo "\nKilling uvicorn (pid=$UVICORN_PID)" | tee -a "$LOGFILE"
  kill $UVICORN_PID || true
fi

echo "\nSMOKE RUN COMPLETE: $(date --iso-8601=seconds)" | tee -a "$LOGFILE"

echo "Smoke log saved to: $LOGFILE"

exit 0
