#!/usr/bin/env bash
set -euo pipefail

wait_for() {
  local hostport="$1"
  local timeout="${2:-20}"
  local start=$(date +%s)
  while ! (exec 3<>/dev/tcp/${hostport%:*}/${hostport#*:} 2>/dev/null); do
    now=$(date +%s)
    if (( now - start > timeout )); then
      echo "Timeout ao esperar ${hostport}"
      break
    fi
    sleep 1
  done
}

# Descomente se quiser bloquear até subir:
# [[ -n "${DB_HOSTPORT:-}" ]] && wait_for "$DB_HOSTPORT" 30
# [[ -n "${QDRANT_HOSTPORT:-}" ]] && wait_for "$QDRANT_HOSTPORT" 30

: "${UVICORN_HOST:=0.0.0.0}"
: "${UVICORN_PORT:=8000}"
: "${UVICORN_WORKERS:=1}"
: "${ASGI_APP:=aurora_platform.main:app}"

exec uvicorn "$ASGI_APP" --host "$UVICORN_HOST" --port "$UVICORN_PORT" --workers "$UVICORN_WORKERS"
