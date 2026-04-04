#!/bin/bash
# telegram-ask.sh — Soru gönder, cevap bekle, stdout'a yaz
# Kullanım: CEVAP=$(bash config/telegram-ask.sh "Ne yapalım?" "🤔")

SORU="${1:-Devam edeyim mi?}"
EMOJI="${2:-🤖}"
TIMEOUT="${3:-600}"

NOTIFY="$HOME/Projects/claude-config/config/notify.sh"
WAIT="$HOME/Projects/claude-config/config/telegram-wait.sh"

bash "$NOTIFY" "$SORU" "$EMOJI"
bash "$WAIT" --timeout "$TIMEOUT"
