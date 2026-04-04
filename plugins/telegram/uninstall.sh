#!/bin/bash
pkill -f telegram-poll.sh 2>/dev/null
for f in notify.sh telegram-poll.sh telegram-wait.sh telegram-ask.sh tg_parse.py tg_send.py; do
  rm -f "$HOME/.claude/config/$f"
done
sed -i '' '/tgbot-start\|tgbot-stop\|tgbot-status\|ccplugin-telegram/d' "$HOME/.zshrc" 2>/dev/null
echo "✅ Telegram plugin kaldırıldı"
