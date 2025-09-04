#!/usr/bin/env bash
set -euo pipefail
KAFKA_CONTAINER="${KAFKA_CONTAINER:-kafka}"
TOPIC="${AURORA_E2E_TOPIC:-aurora.e2e.ping}"
echo "[kafka] Verificando container..."
docker ps --format '{{.Names}}' | grep -q "$KAFKA_CONTAINER"
echo "[kafka] Testando conectividade..."
docker exec "$KAFKA_CONTAINER" kafka-broker-api-versions --bootstrap-server localhost:9092
echo "[kafka] Criando tópico E2E..."
docker exec "$KAFKA_CONTAINER" kafka-topics --create --topic "$TOPIC" --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 || true
echo "[kafka] Produzindo mensagem teste..."
echo '{"test":"e2e","timestamp":"'$(date -Iseconds)'"}' | docker exec -i "$KAFKA_CONTAINER" kafka-console-producer --topic "$TOPIC" --bootstrap-server localhost:9092
echo "[kafka] Consumindo mensagem teste..."
timeout 10s docker exec "$KAFKA_CONTAINER" kafka-console-consumer --topic "$TOPIC" --bootstrap-server localhost:9092 --from-beginning --max-messages 1 || true
echo "[kafka] OK" | tee -a artifacts/e2e_kafka.ok