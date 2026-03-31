#!/bin/bash
set -euo pipefail

echo "=== Claude Code Config Uninstaller ==="
echo ""

# En son yedegi bul
LATEST_BACKUP=$(ls -dt "$HOME/.claude.backup."* 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
  echo "❌ Yedek bulunamadi ($HOME/.claude.backup.*)"
  echo "   Manuel geri alma gerekli."
  exit 1
fi

echo "Yedek bulundu: $LATEST_BACKUP"
read -p "Bu yedekten geri yuklensin mi? [E/h]: " CONFIRM
CONFIRM="${CONFIRM:-E}"

if [[ "$CONFIRM" =~ ^[Ee]$ ]]; then
  rm -rf "$HOME/.claude"
  cp -r "$LATEST_BACKUP" "$HOME/.claude"
  echo "✅ ~/.claude/ yedekten geri yuklendi."
  echo "   Projects dizinindeki dosyalar manuel silinebilir."
else
  echo "Iptal edildi."
fi
