#!/bin/bash
# telegram-poll.sh — Telegram'dan gelen mesajları Claude Code'a iletir
# Kullanım: bash config/telegram-poll.sh [proje_dizini]
# Arka planda: nohup bash config/telegram-poll.sh ~/Projects/myapp > ~/.watchdog/telegram.log 2>&1 &

PROJECT_DIR="${1:-$HOME/Projects/claude-config}"
POLL_INTERVAL=3
OFFSET_FILE="$HOME/.watchdog/telegram_offset"
LOG_FILE="$HOME/.watchdog/telegram.log"

# Secrets yükle
SECRETS_FILE="$HOME/Projects/claude-config/claude-secrets/secrets.env"
[ -f "$SECRETS_FILE" ] && source "$SECRETS_FILE"
[ -z "$TELEGRAM_BOT_TOKEN" ] && source "$HOME/.claude/secrets/secrets.env" 2>/dev/null

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
  echo "❌ TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik" >&2
  exit 1
fi

API="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}"
mkdir -p "$(dirname "$OFFSET_FILE")" "$(dirname "$LOG_FILE")"
OFFSET=$(cat "$OFFSET_FILE" 2>/dev/null || echo "0")

send_msg() {
  local text="$1"
  curl -s -X POST "$API/sendMessage" \
    -d chat_id="$TELEGRAM_CHAT_ID" \
    -d parse_mode="Markdown" \
    -d text="$text" -o /dev/null
}

echo "$(date): Telegram polling başladı → proje: $PROJECT_DIR" | tee -a "$LOG_FILE"
send_msg "🟢 *Claude Code bağlandı*
Proje: \`$(basename "$PROJECT_DIR")\`
Mesaj at, çalıştırayım."

while true; do
  RESPONSE=$(curl -s "$API/getUpdates?offset=$OFFSET&timeout=30&allowed_updates=message")

  UPDATES=$(echo "$RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for u in data.get('result', []):
    msg = u.get('message', {})
    chat_id = str(msg.get('chat', {}).get('id', ''))
    text = msg.get('text', '')
    update_id = u.get('update_id', 0)
    print(f'{update_id}|||{chat_id}|||{text}')
" 2>/dev/null)

  while IFS= read -r line; do
    [ -z "$line" ] && continue
    UPDATE_ID=$(echo "$line" | cut -d'|||' -f1)
    CHAT_ID=$(echo "$line" | cut -d'|||' -f2)
    TEXT=$(echo "$line" | cut -d'|||' -f3)

    # Sadece yetkili chat ID'den gelen mesajları işle
    if [ "$CHAT_ID" != "$TELEGRAM_CHAT_ID" ]; then
      OFFSET=$((UPDATE_ID + 1))
      echo "$OFFSET" > "$OFFSET_FILE"
      continue
    fi

    echo "$(date): Mesaj alındı: $TEXT" | tee -a "$LOG_FILE"

    # Özel komutlar
    case "$TEXT" in
      /stop|/dur)
        send_msg "🔴 Polling durduruluyor."
        echo "$(date): /stop komutu alındı" >> "$LOG_FILE"
        OFFSET=$((UPDATE_ID + 1))
        echo "$OFFSET" > "$OFFSET_FILE"
        exit 0
        ;;
      /status|/durum)
        send_msg "🟢 Çalışıyor — proje: \`$(basename "$PROJECT_DIR")\`
\`$(date '+%H:%M:%S')\`"
        OFFSET=$((UPDATE_ID + 1))
        echo "$OFFSET" > "$OFFSET_FILE"
        continue
        ;;
    esac

    # Claude'a gönder
    send_msg "⚙️ Çalışıyor: _${TEXT}_"

    RESULT=$(cd "$PROJECT_DIR" && claude -p "$TEXT" --output-format text 2>&1 | tail -50)

    # Sonucu Telegram'a gönder (max 4000 karakter)
    if [ ${#RESULT} -gt 4000 ]; then
      RESULT="${RESULT:0:3900}
..._(kesildi)_"
    fi

    send_msg "✅ *Tamamlandı*

\`\`\`
${RESULT}
\`\`\`"

    OFFSET=$((UPDATE_ID + 1))
    echo "$OFFSET" > "$OFFSET_FILE"
  done <<< "$UPDATES"

  sleep "$POLL_INTERVAL"
done
