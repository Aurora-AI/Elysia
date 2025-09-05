#!/usr/bin/env bash
set -euo pipefail

AURA_BRANCH="${AURA_BRANCH:-test/ci-validation-20250905}"
AURA_REPORT="${AURA_REPORT:-docs/reports/RELATORIO_VALIDACAO_CI_20250905.md}"
AURA_TOUCH_FILE="${AURA_TOUCH_FILE:-docs/README.md}"
AURA_PR_TITLE="[QA] Validação Final da Arquitetura de CI/CD — ${AURA_BRANCH}"
AURA_PR_BODY="Executa validação completa dos 7 workflows essenciais (push/PR/dispatch) e inclui relatório consolidado."
AURA_DISPATCH_WORKFLOWS=("ops-audit.yml" "ops-kg-health.yml")

echo ">> [1/8] Preparar branch de teste"
git fetch --all --prune
git checkout main
git pull --ff-only || git merge --no-ff origin/main || echo "Usando branch atual como base"
if git rev-parse --verify "$AURA_BRANCH" >/dev/null 2>&1; then
  git checkout "$AURA_BRANCH"
  git rebase main || git merge main
else
  git checkout -b "$AURA_BRANCH" main
fi

echo ">> [2/8] Modificação trivial para gatilho"
mkdir -p "$(dirname "$AURA_TOUCH_FILE")"
touch "$AURA_TOUCH_FILE"
if ! grep -q "Teste de validação CI" "$AURA_TOUCH_FILE"; then
  echo -e "\n# Teste de validação CI" >> "$AURA_TOUCH_FILE"
fi

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "test(ci): validar execução da pipeline após refatoração"
fi

echo ">> [3/8] Push do branch de teste"
git push -u origin "$AURA_BRANCH" || true

echo ">> [4/8] Abrir/atualizar PR de validação"
if gh pr view "$AURA_BRANCH" >/dev/null 2>&1; then
  echo "PR já existe."
else
  gh pr create --fill --title "$AURA_PR_TITLE" --body "$AURA_PR_BODY" --base main --head "$AURA_BRANCH"
fi
PR_URL="$(gh pr view "$AURA_BRANCH" --json url -q .url)"
echo "PR: $PR_URL"

echo ">> [5/8] Acionar manualmente workflows com workflow_dispatch"
for wf in "${AURA_DISPATCH_WORKFLOWS[@]}"; do
  if gh workflow view "$wf" >/dev/null 2>&1; then
    echo "Disparando $wf…"
    gh workflow run "$wf" --ref "$AURA_BRANCH" || true
  else
    echo "AVISO: workflow $wf não encontrado (seguindo adiante)."
  fi
done

echo ">> [6/8] Aguardar execuções relacionadas ao branch"
# Janela de observação: coleta os últimos 30 runs do branch
# Dica: gh run watch pode bloquear por ID; aqui colhemos status e agregamos.
RUNS_JSON="$(gh run list --branch "$AURA_BRANCH" --limit 30 --json databaseId,name,event,headBranch,status,conclusion,htmlUrl)"
echo "$RUNS_JSON" > /tmp/ci_validation_runs.json

echo ">> [7/8] Gerar relatório consolidado em $AURA_REPORT"
mkdir -p "$(dirname "$AURA_REPORT")"

# Descobrir workflows habilitados no repo:
WF_LIST="$(gh workflow list --limit 50 --json name,path,state -q '.[] | [.name, .path, .state] | @tsv')"

{
  echo "# Relatório de Validação CI — ${AURA_BRANCH}"
  echo
  echo "**PR:** ${PR_URL}"
  echo
  echo "Gerado em: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
  echo
  echo "## Workflows detectados"
  echo
  echo "| Workflow | Arquivo | Estado |"
  echo "|---|---|---|"
  if [ -n "$WF_LIST" ]; then
    while IFS=$'\t' read -r wname wpath wstate; do
      echo "| ${wname} | \`${wpath}\` | ${wstate} |"
    done <<< "$WF_LIST"
  else
    echo "| (nenhum) | | |"
  fi
  echo
  echo "## Execuções recentes no branch \`${AURA_BRANCH}\`"
  echo
  echo "| Workflow | Evento | Status | Conclusão | Link |"
  echo "|---|---|---|---|---|"
} > "$AURA_REPORT"

# Renderizar linhas de runs no relatório
python3 - <<'PY'
import json, os
runs = json.load(open("/tmp/ci_validation_runs.json","r"))
def row(r):
    name = r.get("name","-")
    event = r.get("event","-")
    status = r.get("status","-")
    concl = r.get("conclusion","-")
    url   = r.get("htmlUrl","-")
    return f"| {name} | {event} | {status} | {concl} | [abrir]({url}) |"
lines = [row(r) for r in runs]
with open(os.environ["AURA_REPORT"], "a", encoding="utf-8") as f:
    for L in lines:
        f.write(L+"\n")
PY

# Sinalização simples de sucesso global (verde = todos success)
ALL_GREEN="$(jq -r '[.[] | select(.headBranch=="'"$AURA_BRANCH"'")] | all(.conclusion=="success")' /tmp/ci_validation_runs.json)"
echo >> "$AURA_REPORT"
echo "## Resultado Global" >> "$AURA_REPORT"
if [ "$ALL_GREEN" = "true" ]; then
  echo "- **STATUS GLOBAL:** SUCESSO ✅" >> "$AURA_REPORT"
else
  echo "- **STATUS GLOBAL:** ATENÇÃO ❗ — há falhas ou jobs em aberto. Investigar antes de mergear." >> "$AURA_REPORT"
fi

echo ">> [8/8] Commitar relatório no branch de teste"
git add "$AURA_REPORT"
git commit -m "docs(ci): relatório de validação CI ${AURA_BRANCH}"
git push origin "$AURA_BRANCH"

echo ">> Concluído. Revise o relatório em: $AURA_REPORT"
echo "   PR: $PR_URL"
