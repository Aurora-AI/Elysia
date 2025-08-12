#!/usr/bin/env bash
set -euo pipefail

NAME="aurora-plataform-deepseek-r1-1"
BASE="http://localhost:8000"

echo "== DeepSeek: estado do container =="
docker ps --filter "name=${NAME}"

echo "== Health =="
docker inspect -f '{{.State.Health.Status}}' "${NAME}" || true

echo "== Lista de modelos =="
curl -fsS "${BASE}/v1/models" | jq .

echo "== Teste de completion curto =="
curl -fsS -X POST "${BASE}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        "messages": [{"role":"user","content":"Say hello in one sentence."}],
        "max_tokens": 64,
        "temperature": 0.1
      }' | jq .
