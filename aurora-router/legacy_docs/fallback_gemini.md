# Fallback Gemini 2.5 Pro (Delegação por Incompletude)

## Env vars

- PRIMARY_MODEL_TIMEOUT_MS=6000
- GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-latest:generateContent
- GEMINI_API_KEY=\*\*\* (injetado no deploy)
- GEMINI_MAX_TOKENS=256
- GEMINI_TEMPERATURE=0.7
- GEMINI_TOP_P=0.95

## Endpoint

POST /v1/complete
{ "prompt": "<<lacuna_semantica>>" }

Header de rastreio: `x-aurora-trace-id`
