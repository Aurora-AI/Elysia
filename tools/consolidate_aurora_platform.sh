#!/usr/bin/env bash
set -euo pipefail

# ---- Config ----
TARGET_DIR="src/aurora_platform"
MERGE_AREA="src/aurora_platform__merge_candidates"
# coleções de fontes (ajuste conforme necessidade do seu inventário real)
SOURCES=(
  "aurora-core/src/aurora_platform::aurora_core_src"
  "aurora-platform/src::aurora_platform_dash_src"
  "aurora_platform::aurora_platform_root"
  "src/aurora_platform::already_in_src"
)

DRY_RUN="${DRY_RUN:-1}"   # 1 = só mostrar; 0 = executar git mv
BRANCH_SAFE="${BRANCH_SAFE:-1}" # 1 = impede em 'main'/'master' sem override
ALLOW_ON_PROTECTED="${ALLOW_ON_PROTECTED:-0}"

# ---- Guards ----
test -f .git/config || { echo "Precisa executar na raiz do repo"; exit 1; }
current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH_SAFE" == "1" && "$ALLOW_ON_PROTECTED" == "0" ]]; then
  if [[ "$current_branch" =~ ^(main|master)$ ]]; then
    echo "Abortado: branch protegida ($current_branch). Defina ALLOW_ON_PROTECTED=1 para ignorar."
    exit 1
  fi
fi

mkdir -p "$TARGET_DIR" "$MERGE_AREA"

# ---- Funções auxiliares ----
move_preserve() {
  local origin_dir="$1"
  local label="$2"
  if [[ ! -d "$origin_dir" ]]; then
    echo "[skip] origem inexistente: $origin_dir"
    return 0
  fi
  # listar arquivos rastreados pelo git preferencialmente
  mapfile -t files < <(cd "$origin_dir" && git ls-files || find . -type f -print | sed 's|^\./||')
  if [[ "${#files[@]}" -eq 0 ]]; then
    echo "[info] sem arquivos em $origin_dir"
    return 0
  fi
  for f in "${files[@]}"; do
    src_path="$origin_dir/$f"
    tgt_path="$TARGET_DIR/$f"
    tgt_dir="$(dirname "$tgt_path")"
    if [[ ! -e "$tgt_path" ]]; then
      echo "[mv] $src_path -> $tgt_path"
      if [[ "$DRY_RUN" == "0" ]]; then
        mkdir -p "$tgt_dir"
        git mv "$src_path" "$tgt_path"
      fi
    else
      # conflito -> enviar para merge_candidates
      mc_dir="$MERGE_AREA/${label}/$(dirname "$f")"
      mc_path="$MERGE_AREA/${label}/$f"
      echo "[conflict->preserve] $src_path -> $mc_path"
      if [[ "$DRY_RUN" == "0" ]]; then
        mkdir -p "$mc_dir"
        git mv "$src_path" "$mc_path"
      fi
    fi
  done
}

# ---- Execução ----
echo "== Consolidação para $TARGET_DIR (DRY_RUN=$DRY_RUN) =="

for entry in "${SOURCES[@]}"; do
  origin="${entry%%::*}"
  label="${entry##*::}"
  # não reprocessar o próprio destino como origem útil
  if [[ "$origin" == "$TARGET_DIR" ]]; then
    echo "[info] destino já existe: $origin"
    continue
  fi
  move_preserve "$origin" "$label"
done

# Remover diretórios vazios rastreados (safe)
CANDIDATE_RM=(
  "backend/aurora_platform"
  "aurora-core/src/aurora_platform"
  "aurora-platform/src"
  "aurora_platform"
)
for p in "${CANDIDATE_RM[@]}"; do
  if [[ -d "$p" ]]; then
    # só apaga se estiver vazio (ignorando .gitkeep)
    if [[ -z "$(find "$p" -type f -not -name '.gitkeep' 2>/dev/null)" ]]; then
      echo "[rmdir] $p"
      [[ "$DRY_RUN" == "0" ]] && git rm -r --ignore-unmatch "$p" || true
    else
      echo "[keep] $p não está vazio"
    fi
  fi
done

echo "== Fim. Se estiver OK, rode novamente com DRY_RUN=0 para efetivar =="
