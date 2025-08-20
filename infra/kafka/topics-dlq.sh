#!/bin/bash
# Criação de tópicos DLQ para mensagens problemáticas

BOOTSTRAP="localhost:9092"

echo "Criando tópicos DLQ..."

kafka-topics --bootstrap-server $BOOTSTRAP --create \
  --topic kg.entity.upsert.dlq \
  --partitions 3 \
  --replication-factor 1 \
  --config cleanup.policy=delete,retention.ms=604800000

kafka-topics --bootstrap-server $BOOTSTRAP --create \
  --topic kg.relation.upsert.dlq \
  --partitions 3 \
  --replication-factor 1 \
  --config cleanup.policy=delete,retention.ms=604800000

echo "✅ Tópicos DLQ criados"
