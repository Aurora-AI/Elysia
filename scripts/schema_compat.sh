#!/bin/bash
# Configuração de compatibilidade Schema Registry

REGISTRY_URL="http://localhost:8081"

echo "Configurando compatibilidade BACKWARD_TRANSITIVE..."

curl -X PUT -H "Content-Type: application/json" \
  --data '{"compatibility": "BACKWARD_TRANSITIVE"}' \
  $REGISTRY_URL/config/kg_entity_upsert-value

curl -X PUT -H "Content-Type: application/json" \
  --data '{"compatibility": "BACKWARD_TRANSITIVE"}' \
  $REGISTRY_URL/config/kg_relation_upsert-value

echo "✅ Compatibilidade configurada"
