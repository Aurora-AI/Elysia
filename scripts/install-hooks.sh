#!/usr/bin/env bash
set -euo pipefail

mkdir -p .git/hooks
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
# Fast EXEMPLO blocker (staged-only)
if [[ "${SKIP_EXEMPLO:-0}" == "1" ]]; then exit 0; fi
MSG_FILE=".git/COMMIT_EDITMSG"
if [[ -f "$MSG_FILE" ]] && grep -qi "\[skip-exemplo-check\]" "$MSG_FILE"; then exit 0; fi
mapfile -t FILES < <(git diff --cached --name-only --diff-filter=ACM \
  | grep -E '\.(md|markdown|txt|py|yml|yaml|json|ts|tsx|js|jsx)$' \
  | grep -Ev '^(docs/|doc/|tests?/fixtures?/|node_modules/|dist/|build/|artifacts?/)' || true)
(( ${#FILES[@]} == 0 )) && exit 0
MAX_BYTES=$((2*1024*1024)); RG=$(command -v rg || true); PATTERN='(<<<EXEMPLO_INICIO>>>|<<<EXEMPLO_FIM>>>|\bEXEMPLO\b)'
viol=()
for f in "${FILES[@]}"; do
  content=$(git show ":$f") || continue
  (( $(printf "%s" "$content" | wc -c) > MAX_BYTES )) && continue
  if [[ -n "$RG" ]]; then
    printf "%s" "$content" | rg -n -E "$PATTERN" --pcre2 >/dev/null && viol+=("$f") || true
  else
    printf "%s" "$content" | grep -nE "$PATTERN" >/dev/null && viol+=("$f") || true
  fi
done
if (( ${#viol[@]} )); then
  echo -e "\n❌ EXEMPLO encontrado (staged):"; for f in "${viol[@]}"; do echo "  - $f"; done
  echo -e "\nRemova os blocos ou bypass consciente: export SKIP_EXEMPLO=1 ou [skip-exemplo-check] no commit.\n"; exit 1
fi
exit 0
EOF

chmod +x .git/hooks/pre-commit
echo "[hooks] pre-commit instalado."
