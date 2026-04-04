#!/bin/bash
# telegram-poll.sh — Telegram → Claude Code köprüsü
# Kullanım: bash config/telegram-poll.sh [proje_dizini]
# Arka plan: nohup bash config/telegram-poll.sh ~/Projects/myapp > ~/.watchdog/telegram.log 2>&1 &

PROJECT_DIR="${1:-$HOME/Projects/claude-config}"
LOG_FILE="$HOME/.watchdog/telegram.log"
OFFSET_FILE="$HOME/.watchdog/telegram_offset"

SECRETS_FILE="$HOME/Projects/claude-config/claude-secrets/secrets.env"
[ -f "$SECRETS_FILE" ] && source "$SECRETS_FILE"
[ -z "$TELEGRAM_BOT_TOKEN" ] && source "$HOME/.claude/secrets/secrets.env" 2>/dev/null

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
  echo "❌ TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik" >&2; exit 1
fi

API="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}"
mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$OFFSET_FILE")"
OFFSET=$(cat "$OFFSET_FILE" 2>/dev/null || echo "0")

# ── Yardımcı fonksiyonlar ──

send_msg() {
  local text="$1"
  local markup="${2:-}"
  local payload
  payload=$(python3 -c "
import json, sys
d = {'chat_id': '$TELEGRAM_CHAT_ID', 'parse_mode': 'Markdown', 'text': sys.argv[1]}
if sys.argv[2]:
    d['reply_markup'] = json.loads(sys.argv[2])
print(json.dumps(d))
" "$text" "$markup" 2>/dev/null)
  curl -s -X POST "$API/sendMessage" -H "Content-Type: application/json" -d "$payload" -o /dev/null
}

send_file() {
  local filepath="$1"
  local caption="${2:-Çıktı}"
  curl -s -X POST "$API/sendDocument" \
    -F chat_id="$TELEGRAM_CHAT_ID" \
    -F document=@"$filepath" \
    -F caption="$caption" -o /dev/null
}

typing() {
  curl -s -X POST "$API/sendChatAction" \
    -d chat_id="$TELEGRAM_CHAT_ID" \
    -d action="typing" -o /dev/null
}

answer_callback() {
  local callback_id="$1"
  curl -s -X POST "$API/answerCallbackQuery" \
    -d callback_query_id="$callback_id" -o /dev/null
}

projects_list() {
  ls -d ~/Projects/*/  2>/dev/null | xargs -I{} basename {} | head -10 | tr '\n' '\n'
}

# Başlangıçta eski mesajları atla
LATEST=$(curl -s "$API/getUpdates?offset=-1" | python3 -c "
import json,sys
r=json.load(sys.stdin).get('result',[])
print(r[-1]['update_id']+1 if r else 0)
" 2>/dev/null)
[ -n "$LATEST" ] && [ "$LATEST" -gt "$OFFSET" ] && OFFSET="$LATEST" && echo "$OFFSET" > "$OFFSET_FILE"

echo "$(date): Polling başladı → $PROJECT_DIR" | tee -a "$LOG_FILE"

# Ana keyboard
MAIN_KB='{"keyboard":[[{"text":"📊 Durum"},{"text":"📁 Projeler"}],[{"text":"📋 Log"},{"text":"⏹ Durdur"}]],"resize_keyboard":true,"persistent":true}'

send_msg "🟢 *Claude Code bağlandı*
Proje: \`$(basename "$PROJECT_DIR")\`
Komut yaz veya görev ver." "$MAIN_KB"

# ── Ana döngü ──
while true; do
  RESPONSE=$(curl -s "$API/getUpdates?offset=$OFFSET&timeout=20&allowed_updates=message,callback_query")

  echo "$RESPONSE" | python3 -c "
import json, sys, os

data = json.load(sys.stdin)
chat_id = os.environ.get('TELEGRAM_CHAT_ID','')

for u in data.get('result', []):
    uid = u['update_id']

    # Callback query (inline button tıklaması)
    if 'callback_query' in u:
        cq = u['callback_query']
        if str(cq['message']['chat']['id']) == chat_id:
            print(f'CB|||{uid}|||{cq[\"id\"]}|||{cq[\"data\"]}')
        continue

    msg = u.get('message', {})
    if str(msg.get('chat', {}).get('id', '')) == chat_id:
        text = msg.get('text', '')
        print(f'MSG|||{uid}|||{text}')
" 2>/dev/null | while IFS= read -r line; do
    [ -z "$line" ] && continue

    TYPE=$(echo "$line" | python3 -c "import sys; print(sys.stdin.read().strip().split('|||')[0])")
    UID=$(echo "$line"  | python3 -c "import sys; print(sys.stdin.read().strip().split('|||')[1])")
    REST=$(echo "$line" | python3 -c "import sys; p=sys.stdin.read().strip().split('|||'); print('|||'.join(p[2:]))")

    OFFSET=$((UID + 1))
    echo "$OFFSET" > "$OFFSET_FILE"

    if [ "$TYPE" = "CB" ]; then
      CB_ID=$(echo "$REST" | python3 -c "import sys; print(sys.stdin.read().strip().split('|||')[0])")
      DATA=$(echo "$REST"  | python3 -c "import sys; p=sys.stdin.read().strip().split('|||'); print('|||'.join(p[1:]))")
      answer_callback "$CB_ID"
      TEXT="$DATA"
    else
      TEXT="$REST"
    fi

    echo "$(date): [$TYPE] $TEXT" >> "$LOG_FILE"

    case "$TEXT" in
      /stop|"⏹ Durdur")
        send_msg "🔴 Durduruldu." ""
        exit 0 ;;

      /status|"📊 Durum")
        send_msg "🟢 *Durum*
Proje: \`$(basename "$PROJECT_DIR")\`
Uptime: \`$(uptime | awk '{print $3}' | tr -d ',')\`
Saat: \`$(date '+%H:%M:%S')\`" "$MAIN_KB" ;;

      /projects|"📁 Projeler")
        PLIST=$(projects_list)
        send_msg "📁 *Projeler*
\`\`\`
$PLIST
\`\`\`
Geçmek için: \`/cd <proje_adı>\`" "$MAIN_KB" ;;

      /cd\ *)
        NEW_PROJ="${TEXT#/cd }"
        FULL_PATH="$HOME/Projects/$NEW_PROJ"
        if [ -d "$FULL_PATH" ]; then
          PROJECT_DIR="$FULL_PATH"
          send_msg "📁 Proje değişti: \`$NEW_PROJ\`" "$MAIN_KB"
        else
          send_msg "❌ Bulunamadı: \`$FULL_PATH\`" "$MAIN_KB"
        fi ;;

      /log|"📋 Log")
        LOG_OUT=$(tail -20 "$LOG_FILE" 2>/dev/null)
        TMPF=$(mktemp /tmp/claude-log-XXXX.txt)
        tail -100 "$LOG_FILE" > "$TMPF" 2>/dev/null
        send_file "$TMPF" "Son 100 satır log"
        rm -f "$TMPF" ;;

      /run\ *|/r\ *)
        TASK="${TEXT#/run }"
        TASK="${TASK#/r }"
        typing
        send_msg "⚙️ _Çalışıyor..._" ""
        TMPOUT=$(mktemp /tmp/claude-out-XXXX.txt)
        (cd "$PROJECT_DIR" && timeout 120 claude -p "$TASK" --output-format text 2>&1) > "$TMPOUT"
        RESULT=$(cat "$TMPOUT")
        if [ ${#RESULT} -gt 3800 ]; then
          send_file "$TMPOUT" "Çıktı ($(wc -l < "$TMPOUT") satır)"
        else
          send_msg "✅ *Tamamlandı*

\`\`\`
$RESULT
\`\`\`" "$MAIN_KB"
        fi
        rm -f "$TMPOUT" ;;

      /help|/start)
        send_msg "🤖 *Claude Code Bot*

*Komutlar:*
\`/run <görev>\` — Claude'a görev ver
\`/status\` — Durum
\`/projects\` — Proje listesi
\`/cd <proje>\` — Proje değiştir
\`/log\` — Son loglar
\`/stop\` — Durdur

Veya direkt mesaj yaz → Claude çalıştırır." "$MAIN_KB" ;;

      *)
        # Serbest metin → Claude'a ilet
        typing
        send_msg "⚙️ _Çalışıyor..._" ""
        TMPOUT=$(mktemp /tmp/claude-out-XXXX.txt)
        (cd "$PROJECT_DIR" && timeout 120 claude -p "$TEXT" --output-format text 2>&1) > "$TMPOUT"
        RESULT=$(cat "$TMPOUT")
        if [ ${#RESULT} -gt 3800 ]; then
          send_file "$TMPOUT" "Çıktı"
        else
          send_msg "✅ *Tamamlandı*

\`\`\`
$RESULT
\`\`\`" "$MAIN_KB"
        fi
        rm -f "$TMPOUT" ;;
    esac

    OFFSET=$((UID + 1))
    echo "$OFFSET" > "$OFFSET_FILE"
  done

  sleep 1
done
