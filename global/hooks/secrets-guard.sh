#!/usr/bin/env bash
# PreToolUse on Edit|Write. Refuses to write a secrets file.
#
# This replaces an inline version that read $CLAUDE_TOOL_INPUT. Claude Code does not set that
# variable - it sends the hook payload on stdin as {"tool_name":..,"tool_input":{...}} - so the
# path was always empty and the guard NEVER blocked anything. Measured 2026-10-27: with the
# payload on stdin the old command exits 0 on ~/.claude/secrets/keys.env.
# Same bug as agent-routing-guard.sh had; found by the PC session.
IN=$(cat 2>/dev/null)
[ -z "$IN" ] && IN="$CLAUDE_TOOL_INPUT"
if command -v jq >/dev/null 2>&1; then
  F=$(printf '%s' "$IN" | jq -r '(.tool_input.file_path // .file_path // "")' 2>/dev/null)
else
  F=$(printf '%s' "$IN" | python3 -c \
    "import sys,json
try:
  d=json.load(sys.stdin); print((d.get('tool_input') or d).get('file_path',''))
except Exception: print('')" 2>/dev/null)
fi

# Never block because our own parsing failed.
[ -z "$F" ] && exit 0

case "$F" in
  *.env|*.env.*|*/.env*|*/secrets/*|*/claude-secrets/*|*id_rsa*|*.pem|*.p12|*.keystore)
    echo "BLOCKED: $F is a secrets file - edit ~/.claude/secrets/ directly, never through a tool" >&2
    exit 2 ;;
esac
exit 0
