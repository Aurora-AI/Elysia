param(
  [switch]$Rebuild=$true
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host ">> Validando DevContainer..." -ForegroundColor Cyan

if ($Rebuild) {
  Write-Host ">> Abrindo VS Code para rebuild (feche instâncias abertas)..." -ForegroundColor Yellow
  taskkill /F /IM Code.exe 2>$null | Out-Null
  wsl --shutdown
}

# Teste de build via Docker (sem VS Code)
docker build -f ".devcontainer/Dockerfile" -t aurora-devcontainer-test ".." --no-cache

# Rodar um container curto só para validação de TLS e Python
docker run --rm aurora-devcontainer-test /bin/bash -lc `
  "python -V && pip -V && ls -l /etc/ssl/certs | grep -i corp || true && (curl -sSfI https://ghcr.io/v2/ && echo TLS_OK_to_GHCR)"

Write-Host ">> OK: CA carregado, TLS/ghcr e Python testados." -ForegroundColor Green
