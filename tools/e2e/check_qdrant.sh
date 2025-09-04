#!/usr/bin/env bash
set -euo pipefail
QDRANT_CONTAINER="${QDRANT_CONTAINER:-qdrant}"
QDRANT_HTTP_PORT="${QDRANT_HTTP_PORT:-6333}"
echo "[qdrant] Verificando container..."
docker ps --format '{{.Names}}' | grep -q "$QDRANT_CONTAINER"
echo "[qdrant] Chamando /ready…"
docker exec "$QDRANT_CONTAINER" bash -lc "curl -sSf http://localhost:${QDRANT_HTTP_PORT}/ready" >/dev/null
echo "[qdrant] Criando coleção temporária…"
docker exec "$QDRANT_CONTAINER" bash -lc "curl -sS -X PUT http://localhost:${QDRANT_HTTP_PORT}/collections/e2e_temp -H 'Content-Type: application/json' -d '{\"vectors\": {\"size\": 4, \"distance\": \"Cosine\"}}'"
echo "[qdrant] OK" | tee -a artifacts/e2e_qdrant.ok