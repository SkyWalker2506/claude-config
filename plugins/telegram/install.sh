#!/bin/bash
# Telegram plugin installer
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.claude/config"
mkdir -p "$CONFIG_DIR"

# Copy scripts
for f in notify.sh telegram-poll.sh telegram-wait.sh telegram-ask.sh tg_parse.py tg_send.py; do
  cp "$PLUGIN_DIR/files/$f" "$CONFIG_DIR/$f"
  chmod +x "$CONFIG_DIR/$f"
done

# Add aliases to zshrc if not present
ZSHRC="$HOME/.zshrc"
if grep -q "tgbot-start" "$ZSHRC" 2>/dev/null; then
  # Eski alias'ı güncelle
  sed -i '' '/alias tgbot-start=/d' "$ZSHRC"
  sed -i '' '/alias tgbot-stop=/d' "$ZSHRC"
  sed -i '' '/alias tgbot-status=/d' "$ZSHRC"
  sed -i '' '/alias tgbot-tmux=/d' "$ZSHRC"
fi
cat >> "$ZSHRC" << 'EOF'

# Telegram bot (ccplugin-telegram)
# tgbot-tmux: Claude'u tmux'ta aç + botu başlat — Telegram mesajları direkt terminale gelir
tgbot-tmux() {
  local proj="${1:-${PWD}}"
  local sess="claude-tg"
  tmux has-session -t "$sess" 2>/dev/null || \
    tmux new-session -s "$sess" -d -c "$proj" "claude"
  export CLAUDE_TMUX_SESSION="$sess"
  mkdir -p ~/.watchdog
  CLAUDE_TMUX_SESSION="$sess" \
    nohup bash ~/.claude/config/telegram-poll.sh "$proj" \
    > ~/.watchdog/telegram.log 2>&1 &
  echo "Bot başladı — Claude tmux oturumu: $sess"
  echo "Terminale bağlan: tmux attach -t $sess"
}
# tgbot-start: klasik mod (claude -p --continue, tmux yok)
alias tgbot-start='nohup bash ~/.claude/config/telegram-poll.sh ${PWD} > ~/.watchdog/telegram.log 2>&1 & echo "Bot başladı (PID: $!)"'
alias tgbot-stop='pkill -f telegram-poll.sh && echo "Bot durduruldu"'
alias tgbot-status='ps aux | grep telegram-poll | grep -v grep; tail -3 ~/.watchdog/telegram.log'
EOF

# Validate token
source "$HOME/Projects/claude-config/claude-secrets/secrets.env" 2>/dev/null || source "$HOME/.claude/secrets/secrets.env" 2>/dev/null
if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
  RESP=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="$TELEGRAM_CHAT_ID" -d text="✅ Telegram plugin kuruldu.")
  [ "$RESP" = "200" ] && echo "✅ Telegram bağlantısı doğrulandı" || echo "⚠️  Token/Chat ID hatalı (HTTP $RESP)"
else
  echo "ℹ  TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID secrets'a ekle"
fi

echo "✅ Telegram plugin kuruldu"
