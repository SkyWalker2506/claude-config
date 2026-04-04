#!/bin/bash
# notify.sh — Telegram bildirimi gönder
# Kullanım: notify.sh "mesaj" [emoji]
# Örnek:    notify.sh "Ultraplan hazır" "🔵"

MSG="${1:-Bildirim}"
EMOJI="${2:-🤖}"

# Secrets yükle
SECRETS_FILE="$HOME/Projects/claude-config/claude-secrets/secrets.env"
[ -f "$SECRETS_FILE" ] && source "$SECRETS_FILE"
[ -z "$TELEGRAM_BOT_TOKEN" ] && SECRETS_FILE="$HOME/.claude/secrets/secrets.env" && [ -f "$SECRETS_FILE" ] && source "$SECRETS_FILE"

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
  echo "⚠️  notify.sh: TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik" >&2
  exit 1
fi

FULL_MSG="$EMOJI *Claude Code*
$MSG

\`$(date '+%H:%M')\` · \`$(basename "$PWD")\`"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id="$TELEGRAM_CHAT_ID" \
  -d parse_mode="Markdown" \
  -d text="$FULL_MSG" \
  -o /dev/null

exit 0
