#!/usr/bin/env bash
set -euo pipefail
NEO_CONTAINER="${NEO_CONTAINER:-neo4j}"
echo "[neo4j] Verificando container..."
docker ps --format '{{.Names}}' | grep -q "$NEO_CONTAINER"
echo "[neo4j] Testando conectividade..."
docker exec "$NEO_CONTAINER" cypher-shell -u neo4j -p password "RETURN 1 AS health_check"
echo "[neo4j] Executando seed dos pilares..."
docker exec "$NEO_CONTAINER" cypher-shell -u neo4j -p password -f /seeds/seed_pillars.cypher
echo "[neo4j] Verificando dados inseridos..."
docker exec "$NEO_CONTAINER" cypher-shell -u neo4j -p password "MATCH (n:TestNode {id: 'e2e_marker'}) RETURN count(n) AS test_nodes"
echo "[neo4j] OK" | tee -a artifacts/e2e_neo4j.ok