#!/usr/bin/env bash
set -euo pipefail
KAFKA_CONTAINER="${KAFKA_CONTAINER:-kafka}"
KAFKA_PORT="${KAFKA_PORT:-9092}"
echo "[kafka] Verificando container..."
docker ps --format '{{.Names}}' | grep -q "$KAFKA_CONTAINER"
echo "[kafka] Verificando porta $KAFKA_PORT (TCP)…"
docker exec "$KAFKA_CONTAINER" bash -lc "bash -c '</dev/tcp/localhost/${KAFKA_PORT}'"
echo "[kafka] OK" | tee -a artifacts/e2e_kafka.ok