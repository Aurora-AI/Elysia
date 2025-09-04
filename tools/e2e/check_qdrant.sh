#!/usr/bin/env bash
set -euo pipefail
QDRANT_CONTAINER="${QDRANT_CONTAINER:-qdrant}"
COLLECTION="${AURORA_E2E_COLLECTION:-aurora_e2e_test}"
echo "[qdrant] Verificando container..."
docker ps --format '{{.Names}}' | grep -q "$QDRANT_CONTAINER"
echo "[qdrant] Testando /ready..."
docker exec "$QDRANT_CONTAINER" wget -qO- http://localhost:6333/ready
echo "[qdrant] Criando coleção E2E..."
docker exec "$QDRANT_CONTAINER" curl -sS -X PUT "http://localhost:6333/collections/$COLLECTION" \
  -H 'Content-Type: application/json' \
  -d '{"vectors": {"size": 384, "distance": "Cosine"}}'
echo "[qdrant] Inserindo vetor teste..."
docker exec "$QDRANT_CONTAINER" curl -sS -X PUT "http://localhost:6333/collections/$COLLECTION/points" \
  -H 'Content-Type: application/json' \
  -d '{"points": [{"id": 1, "vector": [0.1, 0.2, 0.3], "payload": {"test": "e2e", "timestamp": "'$(date -Iseconds)'"}}]}'
echo "[qdrant] Verificando inserção..."
docker exec "$QDRANT_CONTAINER" curl -sS "http://localhost:6333/collections/$COLLECTION/points/1"
echo "[qdrant] OK" | tee -a artifacts/e2e_qdrant.ok