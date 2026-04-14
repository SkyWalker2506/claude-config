#!/bin/bash
# gemini-call.sh — Google Gemini API doğrudan çağrısı
# Kullanım: ./scripts/gemini-call.sh "prompt metni"
# Bağımlılık: $GOOGLE_API_KEY env değişkeni veya secrets.env

set -euo pipefail

# --- Secrets yükle (yoksa env'den al) ---
SECRETS_FILE="$HOME/.claude/secrets/secrets.env"
if [ -f "$SECRETS_FILE" ]; then
  # shellcheck disable=SC1090
  source "$SECRETS_FILE"
fi

if [ -z "${GOOGLE_API_KEY:-}" ]; then
  echo "HATA: GOOGLE_API_KEY tanımlı değil." >&2
  echo "~/.claude/secrets/secrets.env dosyasına ekle: GOOGLE_API_KEY=..." >&2
  exit 1
fi

PROMPT="${1:-}"
if [ -z "$PROMPT" ]; then
  echo "Kullanım: $0 \"prompt metni\"" >&2
  exit 1
fi

MODEL="${GEMINI_MODEL:-gemini-2.0-flash}"
MAX_TOKENS="${GEMINI_MAX_TOKENS:-4096}"

response=$(curl -s \
  -X POST "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{\"parts\": [{\"text\": $(echo "$PROMPT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}]}],
    \"generationConfig\": {\"maxOutputTokens\": $MAX_TOKENS}
  }")

if echo "$response" | python3 -c "import json,sys; d=json.load(sys.stdin); exit(0 if 'candidates' in d else 1)" 2>/dev/null; then
  echo "$response" | python3 -c "import json,sys; print(json.load(sys.stdin)['candidates'][0]['content']['parts'][0]['text'])"
else
  echo "HATA: Gemini yanıtı beklenmedik format:" >&2
  echo "$response" >&2
  exit 1
fi
