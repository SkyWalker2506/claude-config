#!/bin/bash
# gpt-call.sh — GPT via Codex CLI (ChatGPT Pro subscription, no API billing)
# Kullanım: ./scripts/gpt-call.sh "prompt metni"
# Varsayılan model: gpt-5.4
# GPT_MODEL env değişkeniyle override edilebilir: GPT_MODEL=gpt-5.4-mini

set -euo pipefail

PROMPT="${1:-}"
if [ -z "$PROMPT" ]; then
  echo "Kullanım: $0 \"prompt metni\"" >&2
  exit 1
fi

MODEL="${GPT_MODEL:-gpt-5.4}"
EFFORT="${GPT_EFFORT:-high}"

if ! command -v codex &>/dev/null; then
  echo "HATA: codex CLI bulunamadı. Kurmak için: npm install -g @openai/codex" >&2
  exit 1
fi

codex exec -m "$MODEL" -c "model_reasoning_effort=\"$EFFORT\"" "$PROMPT"
