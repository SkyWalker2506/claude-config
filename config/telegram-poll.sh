#!/bin/bash
# telegram-poll.sh — Telegram → Claude Code köprüsü
# Kullanım: bash config/telegram-poll.sh [proje_dizini]

PROJECT_DIR="${1:-$HOME/Projects/claude-config}"
LOG_FILE="$HOME/.watchdog/telegram.log"
OFFSET_FILE="$HOME/.watchdog/telegram_offset"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKDIR=$(mktemp -d)
trap "rm -rf $WORKDIR" EXIT

set -a
SECRETS_FILE="$HOME/Projects/claude-config/claude-secrets/secrets.env"
[ -f "$SECRETS_FILE" ] && source "$SECRETS_FILE"
[ -z "$TELEGRAM_BOT_TOKEN" ] && source "$HOME/.claude/secrets/secrets.env" 2>/dev/null
set +a

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
  echo "❌ Token/Chat ID eksik" >&2; exit 1
fi

API="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}"
mkdir -p "$(dirname "$LOG_FILE")"
OFFSET=$(cat "$OFFSET_FILE" 2>/dev/null || echo "0")

log() { echo "$(date '+%H:%M:%S'): $*" | tee -a "$LOG_FILE"; }

send() {
  python3 "$SCRIPT_DIR/tg_send.py" "$TELEGRAM_BOT_TOKEN" "$TELEGRAM_CHAT_ID" "$1" "${2:-}"
}

send_file() {
  curl -s -X POST "$API/sendDocument" \
    -F chat_id="$TELEGRAM_CHAT_ID" \
    -F document=@"$1" \
    -F caption="${2:-Çıktı}" -o /dev/null
}

typing() {
  curl -s -X POST "$API/sendChatAction" \
    -d chat_id="$TELEGRAM_CHAT_ID" -d action="typing" -o /dev/null &
}

run_claude() {
  local task="$1"
  local out="$WORKDIR/out.txt"
  typing
  send "⚙️ _Çalışıyor..._"
  (cd "$PROJECT_DIR" && timeout 120 claude -p "$task" --output-format text 2>&1) > "$out"
  local result; result=$(cat "$out")
  if [ ${#result} -gt 3500 ]; then
    send_file "$out" "Çıktı ($(wc -l < "$out" | tr -d ' ') satır)"
  else
    send "✅ *Tamamlandı*

\`\`\`
${result}
\`\`\`" "$MAIN_KB"
  fi
}

MAIN_KB='{"keyboard":[[{"text":"📊 Durum"},{"text":"📁 Projeler"}],[{"text":"📋 Log"},{"text":"⏹ Durdur"}]],"resize_keyboard":true,"persistent":true}'

# Eski mesajları atla
LATEST=$(curl -s "$API/getUpdates?offset=-1" | python3 -c "
import json,sys
r=json.load(sys.stdin).get('result',[])
print(r[-1]['update_id']+1 if r else 0)
" 2>/dev/null)
[ -n "$LATEST" ] && [ "$LATEST" -gt 0 ] && OFFSET="$LATEST" && echo "$OFFSET" > "$OFFSET_FILE"

log "Polling başladı → $PROJECT_DIR (offset=$OFFSET)"
send "🟢 *Claude Code bağlandı*
Proje: \`$(basename "$PROJECT_DIR")\`
Komut ver veya mesaj yaz." "$MAIN_KB"

while true; do
  RESPONSE=$(curl -s --max-time 8 "$API/getUpdates?offset=$OFFSET&timeout=3&allowed_updates=message,callback_query" 2>/dev/null)
  [ -z "$RESPONSE" ] && sleep 2 && continue

  UPDATES="$WORKDIR/updates.txt"
  echo "$RESPONSE" | python3 "$SCRIPT_DIR/tg_parse.py" "$TELEGRAM_CHAT_ID" > "$UPDATES" 2>/dev/null
  [ ! -s "$UPDATES" ] && sleep 1 && continue

  while IFS=$'\t' read -r TYPE UID FIELD1 FIELD2; do
    [ -z "$TYPE" ] && continue
    OFFSET=$((UID + 1))
    echo "$OFFSET" > "$OFFSET_FILE"

    if [ "$TYPE" = "CB" ]; then
      curl -s -X POST "$API/answerCallbackQuery" -d callback_query_id="$FIELD1" -o /dev/null
      TEXT="$FIELD2"
    else
      TEXT="$FIELD1"
    fi

    [ -z "$TEXT" ] && continue
    log "[$TYPE] $TEXT"

    # Normalize: emoji'li buton metinlerini komuta çevir
    case "$TEXT" in
      *"Durum"*)  TEXT="/status" ;;
      *"Projeler"*) TEXT="/projects" ;;
      *"Durdur"*)  TEXT="/stop" ;;
      *"Log"*)     TEXT="/log" ;;
    esac

    case "$TEXT" in
      /stop)
        send "🔴 Durduruldu."
        exit 0 ;;
      /status)
        send "🟢 *Durum*
Proje: \`$(basename "$PROJECT_DIR")\`
Saat: \`$(date '+%H:%M:%S')\`" "$MAIN_KB" ;;
      /projects)
        PLIST=$(ls -d ~/Projects/*/ 2>/dev/null | xargs -I{} basename {} | head -10)
        send "📁 *Projeler*
\`\`\`
$PLIST
\`\`\`" "$MAIN_KB" ;;
      /cd\ *)
        NEW="${TEXT#/cd }"
        FULL="$HOME/Projects/$NEW"
        if [ -d "$FULL" ]; then
          PROJECT_DIR="$FULL"
          send "📁 Proje: \`$NEW\`" "$MAIN_KB"
        else
          send "❌ Bulunamadı: \`$NEW\`" "$MAIN_KB"
        fi ;;
      /log)
        TMPF="$WORKDIR/log.txt"
        tail -100 "$LOG_FILE" > "$TMPF"
        send_file "$TMPF" "Son 100 satır" ;;
      /run\ *|/r\ *)
        TASK="${TEXT#/run }"; TASK="${TASK#/r }"
        run_claude "$TASK" ;;
      /help|/start)
        send "🤖 *Claude Code Bot*

\`/run <görev>\` — Claude'a görev ver
\`/status\` — Durum
\`/projects\` — Projeler
\`/cd <proje>\` — Proje değiştir
\`/log\` — Loglar
\`/stop\` — Durdur

Serbest metin → Claude'a iletilir." "$MAIN_KB" ;;
      *)
        run_claude "$TEXT" ;;
    esac

  done < "$UPDATES"
done
