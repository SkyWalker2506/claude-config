#!/bin/bash
# notify.sh — Claude Code hook bildirimi
# Kullanım: notify.sh "mesaj" [emoji] [buttons_json]
# Ses aç/kapa: touch ~/.claude/notifications-mute / rm ~/.claude/notifications-mute

MSG="${1:-Bildirim}"
EMOJI="${2:-🤖}"
BUTTONS="${3:-}"

# ccplugin-notifications mevcutsa ona delege et
PLUGIN_NOTIFY="$HOME/.claude/plugins/notifications/notify.sh"
if [ -f "$PLUGIN_NOTIFY" ]; then
  bash "$PLUGIN_NOTIFY" --message "$MSG" --emoji "$EMOJI" ${BUTTONS:+--buttons "$BUTTONS"}
  exit $?
fi

# Fallback: sadece ses + macOS bildirim
if [ ! -f "$HOME/.claude/notifications-mute" ] && command -v afplay &>/dev/null; then
  afplay /System/Library/Sounds/Glass.aiff &
fi

command -v osascript &>/dev/null && \
  osascript -e "display notification \"$MSG\" with title \"Claude Code\"" 2>/dev/null

exit 0
