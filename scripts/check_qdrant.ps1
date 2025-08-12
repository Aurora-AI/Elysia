Param(
  [string]$ContainerName = "aurora-qdrant",
  [string]$Http = "http://localhost:6333"
)

Write-Host "== Qdrant: estado do container ==" -ForegroundColor Cyan
docker ps --filter "name=$ContainerName"

Write-Host "== Health ==" -ForegroundColor Cyan
$health = docker inspect -f '{{.State.Health.Status}}' $ContainerName 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "Health: N/A" -ForegroundColor Yellow } else { Write-Host "Health: $health" }

Write-Host "== Ping endpoint /collections ==" -ForegroundColor Cyan
try {
  $r = Invoke-RestMethod -Uri "$Http/collections" -Method GET -TimeoutSec 5
  Write-Host "HTTP OK em $Http/collections"
} catch {
  Write-Error "FALHA HTTP em $Http/collections: $($_.Exception.Message)"
  exit 2
}

Write-Host "== Portas expostas ==" -ForegroundColor Cyan
docker inspect $ContainerName --format "{{range .NetworkSettings.Ports}}{{println .}}{{end}}" 2>$null

if ($health -and $health -ne "healthy") { exit 1 } else { exit 0 }
