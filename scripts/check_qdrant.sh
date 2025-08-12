#!/bin/bash
# scripts/check_qdrant.sh
# Valida o healthcheck do Qdrant e imprime status legível

set -e

QDRANT_URL="http://localhost:6333/collections"

response=$(curl -s "$QDRANT_URL")
status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d':' -f2 | tr -d '"')

if [ "$status" = "ok" ]; then
  echo "Qdrant HEALTHY: status=ok"
  exit 0
else
  echo "Qdrant UNHEALTHY: status=$status"
  exit 1
fi
