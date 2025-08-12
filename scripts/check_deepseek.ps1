#!/usr/bin/env pwsh
# Script de verificação do DeepSeek R1

$NAME = "aurora-plataform-deepseek-r1-1"
$BASE = "http://localhost:8010"

Write-Host "== DeepSeek: estado do container ==" -ForegroundColor Green
docker ps --filter "name=$NAME"

Write-Host "`n== Health ==" -ForegroundColor Green
try {
    $health = docker inspect -f '{{.State.Health.Status}}' $NAME
    Write-Host "Health: $health"
} catch {
    Write-Host "Erro ao verificar health: $_" -ForegroundColor Red
}

Write-Host "`n== Teste de health endpoint ==" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$BASE/health" -Method Get
    Write-Host "Health endpoint OK:"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Erro no health endpoint: $_" -ForegroundColor Red
}

Write-Host "`n== Lista de modelos ==" -ForegroundColor Green
try {
    $models = Invoke-RestMethod -Uri "$BASE/v1/models" -Method Get
    Write-Host "Modelos disponíveis:"
    $models | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Erro ao listar modelos: $_" -ForegroundColor Red
}

Write-Host "`n== Teste de completion curto ==" -ForegroundColor Green
try {
    $body = @{
        model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        messages = @(
            @{
                role = "user"
                content = "Say hello in one sentence."
            }
        )
        max_tokens = 64
        temperature = 0.1
    } | ConvertTo-Json -Depth 3

    $completion = Invoke-RestMethod -Uri "$BASE/v1/chat/completions" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Completion OK:"
    $completion | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Erro no completion: $_" -ForegroundColor Red
}
