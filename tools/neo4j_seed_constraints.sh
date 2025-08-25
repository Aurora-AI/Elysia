#!/usr/bin/env bash
set -euo pipefail
NEO4J_URL="${NEO4J_URL:-http://localhost:7474}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-neo4j}"

make_payload() { printf '{"statements":[{"statement":"%s"}]}' "$1"; }

while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  curl -sS -u "$NEO4J_USER:$NEO4J_PASSWORD" \
    -H "Content-Type: application/json" \
    -d "$(make_payload "$line")" \
    "$NEO4J_URL/db/neo4j/tx/commit" >/dev/null
done < "$(dirname "$0")/neo4j_seed_constraints.cypher"

echo "Constraints applied."
