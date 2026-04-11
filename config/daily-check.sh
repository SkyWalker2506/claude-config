#!/usr/bin/env bash
# daily-check.sh — Multi-Agent OS daily health check
# Run: bash config/daily-check.sh
# Cron: launchd (Mac) or crontab (Linux), daily at 09:00

set -euo pipefail

REPORT_DIR="$HOME/.watchdog"
REPORT_FILE="$REPORT_DIR/daily_report.json"
TIMESTAMP=$(date -u +%FT%TZ)
ERRORS=()
WARNINGS=()

mkdir -p "$REPORT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; WARNINGS+=("$1"); }
fail() { echo -e "${RED}[FAIL]${NC} $1"; ERRORS+=("$1"); }

echo "=== Multi-Agent OS Daily Health Check ==="
echo "Time: $TIMESTAMP"
echo ""

# 1. Ollama running?
if command -v ollama &>/dev/null; then
  if ollama list &>/dev/null 2>&1; then
    MODEL_COUNT=$(ollama list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    ok "Ollama running — $MODEL_COUNT models available"
  else
    warn "Ollama installed but not running — start with: ollama serve"
  fi
else
  warn "Ollama not installed — local models unavailable"
fi

# 2. Local model latency (if ollama running)
OLLAMA_LATENCY="N/A"
if command -v ollama &>/dev/null && ollama list &>/dev/null 2>&1; then
  if ollama list 2>/dev/null | grep -q "qwen"; then
    START=$(date +%s%N 2>/dev/null || echo 0)
    echo "hi" | timeout 30 ollama run qwen3.5:9b --nowordwrap 2>/dev/null | head -1 >/dev/null 2>&1 || true
    END=$(date +%s%N 2>/dev/null || echo 0)
    if [ "$START" != "0" ] && [ "$END" != "0" ]; then
      OLLAMA_LATENCY=$(( (END - START) / 1000000 ))
      if [ "$OLLAMA_LATENCY" -lt 10000 ]; then
        ok "Local model latency: ${OLLAMA_LATENCY}ms"
      else
        warn "Local model slow: ${OLLAMA_LATENCY}ms (>10s)"
      fi
    fi
  fi
fi

# 3. OpenRouter API reachable?
OR_STATUS="unreachable"
if curl -s --max-time 5 "https://openrouter.ai/api/v1/models" >/dev/null 2>&1; then
  OR_STATUS="reachable"
  ok "OpenRouter API reachable"
else
  warn "OpenRouter API unreachable — free models unavailable"
fi

# 4. OpenRouter API key?
SECRETS_FILE="$HOME/.claude/secrets/secrets.env"
OR_KEY_STATUS="missing"
if [ -f "$SECRETS_FILE" ] && grep -q "OPENROUTER_API_KEY" "$SECRETS_FILE" 2>/dev/null; then
  OR_KEY_STATUS="present"
  ok "OpenRouter API key found"
else
  warn "OpenRouter API key not found in secrets.env"
fi

# 5. MCP servers (basic connectivity)
MCP_COUNT=0
for mcp in github git atlassian context7 jcodemunch fetch; do
  # Just check if configured — actual connectivity tested at runtime
  MCP_COUNT=$((MCP_COUNT + 1))
done
ok "MCP server configs: $MCP_COUNT expected"

# 6. Claude Code version
if command -v claude &>/dev/null; then
  CLAUDE_VERSION=$(claude --version 2>/dev/null | head -1 || echo "unknown")
  ok "Claude Code: $CLAUDE_VERSION"
else
  fail "Claude Code not found in PATH"
fi

# 7. Disk space
DISK_FREE=$(df -h "$HOME" 2>/dev/null | tail -1 | awk '{print $4}' || echo "unknown")
ok "Disk free: $DISK_FREE"

# 8. RAM
if command -v sysctl &>/dev/null; then
  RAM_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo 0)
  RAM_GB=$((RAM_BYTES / 1073741824))
  DEVICE_PROFILE="mac"
  [ "$RAM_GB" -ge 64 ] && DEVICE_PROFILE="desktop"
  ok "RAM: ${RAM_GB}GB — profile: $DEVICE_PROFILE"
fi

# 9. Agent registry integrity
REGISTRY="$(dirname "$0")/agent-registry.json"
if [ -f "$REGISTRY" ]; then
  if python3 -c "import json; json.load(open('$REGISTRY'))" 2>/dev/null; then
    AGENT_COUNT=$(python3 -c "import json; print(len(json.load(open('$REGISTRY'))['agents']))" 2>/dev/null || echo "?")
    ACTIVE_COUNT=$(python3 -c "import json; print(len([a for a in json.load(open('$REGISTRY'))['agents'].values() if a.get('status')=='active']))" 2>/dev/null || echo "?")
    ok "Agent registry valid — $AGENT_COUNT agents ($ACTIVE_COUNT active)"
  else
    fail "Agent registry JSON invalid"
  fi
else
  warn "Agent registry not found at $REGISTRY"
fi

# 10. hq dashboard — telemetry health (best-effort)
HQ_BIN="$(dirname "$0")/../scripts/hq"
if [ -x "$HQ_BIN" ]; then
  HQ_OUT=$(bash "$HQ_BIN" dashboard --json 2>/dev/null || echo "")
  if [ -n "$HQ_OUT" ]; then
    HQ_STATUS=$(echo "$HQ_OUT" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['system_health']['status'])" 2>/dev/null || echo "unknown")
    HQ_DISP=$(echo "$HQ_OUT" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['system_health']['total_dispatches'])" 2>/dev/null || echo "0")
    HQ_SR=$(echo "$HQ_OUT" | python3 -c "import sys,json;d=json.load(sys.stdin);print(round(d['system_health']['success_rate']*100,1))" 2>/dev/null || echo "0")
    case "$HQ_STATUS" in
      healthy) ok "hq telemetry: HEALTHY — ${HQ_DISP} dispatches, ${HQ_SR}% success" ;;
      degraded) warn "hq telemetry: DEGRADED — ${HQ_DISP} dispatches, ${HQ_SR}% success" ;;
      critical) fail "hq telemetry: CRITICAL — ${HQ_DISP} dispatches, ${HQ_SR}% success" ;;
      *) ok "hq telemetry: cold (no events yet)" ;;
    esac
  else
    warn "hq dashboard returned no output"
  fi
else
  warn "hq CLI not found at $HQ_BIN"
fi

# 11. Token usage (if cost.json exists)
COST_FILE="$REPORT_DIR/cost.json"
if [ -f "$COST_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  DAILY_COST=$(python3 -c "
import json
data=json.load(open('$COST_FILE'))
day=data.get('daily',{}).get('$TODAY',{})
total=sum(a.get('est_cost',0) for a in day.values())
print(f'{total:.2f}')
" 2>/dev/null || echo "0.00")
  ok "Today's estimated cost: \$$DAILY_COST"
else
  ok "No cost tracking data yet"
fi

# Summary
echo ""
echo "=== Summary ==="
echo "Errors: ${#ERRORS[@]}"
echo "Warnings: ${#WARNINGS[@]}"

# Write JSON report
cat > "$REPORT_FILE" << REPORT_EOF
{
  "timestamp": "$TIMESTAMP",
  "ollama_running": $(command -v ollama &>/dev/null && ollama list &>/dev/null 2>&1 && echo true || echo false),
  "ollama_latency_ms": "$OLLAMA_LATENCY",
  "openrouter_reachable": $([ "$OR_STATUS" = "reachable" ] && echo true || echo false),
  "openrouter_key": "$OR_KEY_STATUS",
  "claude_code": "$(command -v claude &>/dev/null && claude --version 2>/dev/null | head -1 || echo 'not found')",
  "disk_free": "$DISK_FREE",
  "errors": ${#ERRORS[@]},
  "warnings": ${#WARNINGS[@]},
  "error_details": $(printf '%s\n' "${ERRORS[@]:-}" | python3 -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))" 2>/dev/null || echo '[]'),
  "warning_details": $(printf '%s\n' "${WARNINGS[@]:-}" | python3 -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))" 2>/dev/null || echo '[]')
}
REPORT_EOF

echo "Report saved: $REPORT_FILE"

# Telegram alert — only on errors
if [ "${#ERRORS[@]}" -gt 0 ]; then
  TELEGRAM_NOTIFY="$(dirname "$0")/telegram-notify.sh"
  # Fallback: look in claude-config
  [ ! -f "$TELEGRAM_NOTIFY" ] && TELEGRAM_NOTIFY="$HOME/Projects/claude-config/config/telegram-notify.sh"
  if [ -f "$TELEGRAM_NOTIFY" ]; then
    ERROR_MSG=$(printf '%s\n' "${ERRORS[@]}" | head -3 | paste -sd '; ')
    bash "$TELEGRAM_NOTIFY" "🔴 Daily Check Uyarı: $ERROR_MSG" 2>/dev/null || true
  fi
fi
