#!/bin/bash
# Usage: ./codex-quota-report.sh [--reset]
# Call this when codex returns a quota/rate-limit error

QUOTA_FILE="$HOME/.watchdog/codex-quota.json"
mkdir -p "$(dirname "$QUOTA_FILE")"

if [ "${1}" = "--reset" ]; then
    rm -f "$QUOTA_FILE"
    echo "✅ Codex quota durumu sıfırlandı"
    exit 0
fi

# Default: mark as exhausted, assume ~3 hour reset window (ChatGPT Pro resets hourly/daily)
RESET_AT=$(date -u -v+3H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d '+3 hours' +"%Y-%m-%dT%H:%M:%SZ")
cat > "$QUOTA_FILE" << EOF
{
  "status": "exhausted",
  "reported_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "reset_at": "$RESET_AT",
  "fallback": "claude-sonnet-4-6"
}
EOF

echo "⚠️  Codex quota exhausted. Reset bekleniyor: $RESET_AT"
echo "   Fallback: claude-sonnet-4-6"
echo "   Sıfırlamak için: $0 --reset"
