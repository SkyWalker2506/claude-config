#!/usr/bin/env bash
# telegram-notify.sh — Send a one-way Telegram notification (no reply wait)
# Usage: bash telegram-notify.sh "message text" [emoji]
# Reads TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID from ~/.claude/secrets/secrets.env

SECRETS_FILE="$HOME/.claude/secrets/secrets.env"

# Load secrets
if [ -f "$SECRETS_FILE" ]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" =~ ^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*= ]] && eval "export $line" 2>/dev/null || true
  done < "$SECRETS_FILE"
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="${TELEGRAM_CHAT_ID:-}"
MESSAGE="${1:-}"

if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
  echo "telegram-notify: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in secrets.env" >&2
  exit 1
fi

if [ -z "$MESSAGE" ]; then
  echo "telegram-notify: No message provided" >&2
  exit 1
fi

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  --data-urlencode "parse_mode=HTML")

if [ "$HTTP_CODE" = "200" ]; then
  exit 0
else
  echo "telegram-notify: HTTP $HTTP_CODE from Telegram API" >&2
  exit 1
fi
