#!/usr/bin/env bash
set -euo pipefail

# 0) Pastas de trabalho
mkdir -p artifacts/ci .github/workflows

REL="artifacts/ci/diag_127_report.txt"
: > "$REL"

log() { echo "[$(date +'%F %T')] $*" | tee -a "$REL"; }

log "Iniciando diagnóstico rápido de exit 127 (command not found)."

# 1) Checagem de disponibilidade de comandos
declare -a CMDS=("docker" "actionlint" "pre-commit" "git" "python3" "pip3" "pipx")
for c in "${CMDS[@]}"; do
  if command -v "$c" >/dev/null 2>&1; then
    log "CMD OK   : $c -> $(command -v "$c")"
  else
    log "CMD MISS : $c (provável fonte de exit 127 se invocado)"
  fi
done

# 2) Validações que poderiam gerar 127 (skips na opção A)
log "Validação actionlint: SKIP por opção A (sem Docker/sem binário)."
log "Validação actionlint via Docker: SKIP (docker possivelmente ausente)."

# 3) Validação YAML
log "Validando YAML (.github/workflows/*.yml) via Python (yaml.safe_load)..."
python3 - <<'PY' || { echo "[YAML ERR] Validação falhou" | tee -a "artifacts/ci/diag_127_report.txt"; exit 2; }
import sys, glob
try:
    import yaml
except ImportError:
    print("[YAML ERR] PyYAML não instalado; instale com 'pip install pyyaml'")
    sys.exit(1)
fails = 0
for p in sorted(glob.glob('.github/workflows/*.yml')):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"[YAML OK] {p}")
    except Exception as e:
        print(f"[YAML ERR] {p}: {e}")
        fails += 1
if fails:
    sys.exit(1)
PY
log "YAML parse: OK"

# 4) Snapshot do CODEOWNERS Guard
if [ -f ".github/workflows/codeowners-guard.yml" ]; then
  log "Snapshot de .github/workflows/codeowners-guard.yml (primeiras 120 linhas):"
  nl -ba ".github/workflows/codeowners-guard.yml" | sed -n '1,120p' | tee -a "$REL" >/dev/null
else
  log "AVISO: .github/workflows/codeowners-guard.yml não encontrado."
fi

# 5) Commit idempotente
log "Preparando commit idempotente..."
git add .github/workflows/*.yml || true
if git diff --cached --quiet; then
  log "Nenhuma alteração a commitar (idempotente)."
else
  if git commit -m "ci: validate workflows without actionlint; add 127 diagnosis report"; then
    if git push 2>&1 | tee -a "$REL"; then
      log "Push realizado com sucesso."
    else
      log "Push falhou (sem upstream/permissões?). Sugestão: git push --set-upstream origin $(git branch --show-current)"
    fi
  else
    log "Commit falhou (possível hook ou conflito)."
  fi
fi

log "Diagnóstico concluído. Relatório salvo em: $REL"
echo
echo "──────────────────────────────────────────────────────────────────────────────"
echo "Relatório resumido:"
tail -n +1 "$REL"
