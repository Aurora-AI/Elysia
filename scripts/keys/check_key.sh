#!/usr/bin/env bash
set -euo pipefail

PROVIDER="${1:-}"
KEY="${2:-}"
BASE="${3:-}"
INSECURE="${INSECURE:-0}"

CURL_OPTS=(-sS -D - -o /dev/null)
[[ "$INSECURE" = "1" ]] && CURL_OPTS+=(-k)

case "$PROVIDER" in
  deepseek)
    URL="https://api.deepseek.com/models"
    AUTH=(-H "Authorization: Bearer $KEY")
    ;;
  openai)
    URL="https://api.openai.com/v1/models"
    AUTH=(-H "Authorization: Bearer $KEY")
    ;;
  gemini)
    URL="https://generativelanguage.googleapis.com/v1beta/models?key=$KEY"
    AUTH=()
    ;;
  azure)
    : "${BASE:?Usage: azure requires BASE, e.g. https://<resource>.openai.azure.com}"
    URL="${BASE%/}/openai/models?api-version=2024-10-21"
    AUTH=(-H "api-key: $KEY")
    ;;
  openai_compat)
    : "${BASE:?Usage: openai_compat requires BASE, e.g. http://localhost:8000/v1}"
    URL="${BASE%/}/models"
    AUTH=(-H "Authorization: Bearer $KEY")
    ;;
  *)
    echo "Usage: $0 {deepseek|openai|gemini|azure|openai_compat} <KEY> [BASE]" >&2; exit 2;;
esac

STATUS=$(curl "${CURL_OPTS[@]}" "${AUTH[@]}" "$URL" -w "%{http_code}")
echo "PROVIDER=$PROVIDER URL=$URL STATUS=$STATUS"

case "$STATUS" in
  2??) echo "✅ Key appears VALID (HTTP $STATUS)"; exit 0;;
  401|403) echo "❌ Key INVALID or unauthorized (HTTP $STATUS)"; exit 1;;
  429) echo "⚠️ Rate limit (HTTP 429) — key may be valid"; exit 3;;
  5??) echo "⚠️ Provider/server error (HTTP $STATUS)"; exit 4;;
  *) echo "⚠️ Unexpected status (HTTP $STATUS)"; exit 5;;
esac
