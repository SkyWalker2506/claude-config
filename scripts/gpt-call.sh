#!/bin/bash
# gpt-call.sh — OpenRouter üzerinden GPT çağrısı
# Kullanım: ./scripts/gpt-call.sh "prompt metni"
# Varsayılan model: openai/gpt-4o-mini (ücretsiz tier'da çalışır)
# GPT_MODEL env değişkeniyle override edilebilir

set -euo pipefail

SECRETS_FILE="$HOME/.claude/secrets/secrets.env"
if [ -f "$SECRETS_FILE" ]; then
  # shellcheck disable=SC1090
  source "$SECRETS_FILE" 2>/dev/null || true
fi

if [ -z "${OPENROUTER_API_KEY:-}" ]; then
  echo "HATA: OPENROUTER_API_KEY tanımlı değil." >&2
  exit 1
fi

PROMPT="${1:-}"
if [ -z "$PROMPT" ]; then
  echo "Kullanım: $0 \"prompt metni\"" >&2
  exit 1
fi

MODEL="${GPT_MODEL:-openai/gpt-4o-mini}"
MAX_TOKENS="${GPT_MAX_TOKENS:-4096}"

response=$(curl -s \
  -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"max_tokens\": $MAX_TOKENS,
    \"messages\": [{\"role\": \"user\", \"content\": $(echo "$PROMPT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}]
  }")

if echo "$response" | python3 -c "import json,sys; d=json.load(sys.stdin); exit(0 if 'choices' in d else 1)" 2>/dev/null; then
  echo "$response" | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
else
  echo "HATA: OpenRouter yanıtı beklenmedik format:" >&2
  echo "$response" >&2
  exit 1
fi
