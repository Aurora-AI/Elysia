#!/bin/bash
# scripts/validate_environment.sh
# Valida todo o ambiente Aurora (Docker, Qdrant, etc.)

set -e

echo "=== Aurora Environment Validation ==="

# 1. Verificar Docker
echo "1. Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found"
    exit 1
fi

docker version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Docker is running"
else
    echo "❌ Docker daemon not accessible"
    exit 1
fi

# 2. Verificar Docker Compose
echo "2. Checking Docker Compose..."
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose not found"
    exit 1
fi

docker compose version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Docker Compose is available"
else
    echo "❌ Docker Compose not working"
    exit 1
fi

# 3. Verificar se o Qdrant está rodando
echo "3. Checking Qdrant..."
if docker ps --filter "name=aurora-qdrant" --format "table {{.Names}}" | grep -q "aurora-qdrant"; then
    echo "✅ Qdrant container is running"

    # Verificar health
    HEALTH=$(docker inspect -f '{{.State.Health.Status}}' aurora-qdrant 2>/dev/null || echo "no-health")
    if [ "$HEALTH" = "healthy" ]; then
        echo "✅ Qdrant is healthy"
    else
        echo "⚠️  Qdrant health status: $HEALTH"
    fi

    # Testar endpoint
    if curl -fsS http://localhost:6333/collections > /dev/null 2>&1; then
        echo "✅ Qdrant HTTP endpoint is responding"
    else
        echo "❌ Qdrant HTTP endpoint not responding"
        exit 1
    fi
else
    echo "⚠️  Qdrant container not running"
    echo "   Run: docker compose up -d qdrant"
fi

# 4. Verificar ferramentas necessárias
echo "4. Checking required tools..."
for tool in curl; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool is available"
    else
        echo "❌ $tool not found"
        exit 1
    fi
done

# jq é opcional no Windows
if command -v jq &> /dev/null; then
    echo "✅ jq is available"
else
    echo "⚠️  jq not found (optional for Windows)"
fi

echo ""
echo "🎉 Environment validation completed successfully!"
echo ""
echo "Available services:"
docker compose ps 2>/dev/null || echo "   (run 'docker compose ps' to see services)"
