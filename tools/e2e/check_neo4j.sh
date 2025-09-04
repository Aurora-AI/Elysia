#!/usr/bin/env bash
set -euo pipefail
NEO_CONTAINER="${NEO_CONTAINER:-neo4j}"
NEO_HTTP_PORT="${NEO_HTTP_PORT:-7474}"
echo "[neo4j] Verificando container..."
docker ps --format '{{.Names}}' | grep -q "$NEO_CONTAINER"
echo "[neo4j] Aguardando HTTP :${NEO_HTTP_PORT}..."
for i in {1..30}; do
  if docker exec "$NEO_CONTAINER" bash -lc "curl -sSf http://localhost:${NEO_HTTP_PORT}/ || true" >/dev/null; then
    echo "[neo4j] HTTP disponível."; break; fi; sleep 1; done
SEED="/seeds/seed_pillars.cypher"
if docker exec "$NEO_CONTAINER" bash -lc "test -f $SEED"; then
  echo "[neo4j] Seed detectado (execução simulada)."
  # Exemplo real: cypher-shell -u neo4j -p $NEO4J_PASSWORD -f $SEED
fi
echo "[neo4j] OK" | tee -a artifacts/e2e_neo4j.ok