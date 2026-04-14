#!/bin/bash
# quota-check.sh — Pre-dispatch quota check for all backends
# Usage: ./scripts/quota-check.sh [backend]
#   backend: "codex" | "gemini" | "all" (default: all)
# Commands:
#   ./scripts/quota-check.sh increment <backend>  — increment call counter
#   ./scripts/quota-check.sh block <backend> [duration_seconds]  — mark backend as blocked
# Output: JSON with status per backend
# Exit codes: 0 = all OK, 1 = at least one backend over quota

set -euo pipefail

QUOTA_STATE="$HOME/.watchdog/quota-state.json"
mkdir -p "$HOME/.watchdog"

# Initialize state file if missing
if [ ! -f "$QUOTA_STATE" ]; then
  echo '{"codex":{"calls_5h":0,"calls_weekly":0,"last_reset_5h":0,"last_reset_weekly":0,"blocked_until":0},"gemini":{"calls_daily":0,"calls_minute":0,"last_reset_daily":"","last_minute":"","blocked_until":0}}' > "$QUOTA_STATE"
fi

now=$(date +%s)
today=$(date +%Y-%m-%d)
this_minute=$(date +%Y-%m-%d-%H-%M)

# --- Codex (GPT) quota check ---
check_codex() {
  local state=$(python3 -c "
import json
with open('$QUOTA_STATE') as f:
    d = json.load(f)
c = d.get('codex', {})
import time
now = int(time.time())
# Reset 5h window (18000 seconds)
if now - c.get('last_reset_5h', 0) > 18000:
    c['calls_5h'] = 0
    c['last_reset_5h'] = now
# Reset weekly window (604800 seconds)
if now - c.get('last_reset_weekly', 0) > 604800:
    c['calls_weekly'] = 0
    c['last_reset_weekly'] = now
d['codex'] = c
with open('$QUOTA_STATE', 'w') as f:
    json.dump(d, f, indent=2)
# Limits (ChatGPT Pro estimates)
limit_5h = 80  # ~80 codex exec calls per 5h window
limit_weekly = 500
remaining_5h = max(0, limit_5h - c['calls_5h'])
remaining_weekly = max(0, limit_weekly - c['calls_weekly'])
blocked = c.get('blocked_until', 0) > now
print(json.dumps({
    'backend': 'codex',
    'available': not blocked and remaining_5h > 0 and remaining_weekly > 0,
    'remaining_5h': remaining_5h,
    'remaining_weekly': remaining_weekly,
    'used_5h': c['calls_5h'],
    'used_weekly': c['calls_weekly'],
    'blocked': blocked
}))
")
  echo "$state"
}

# --- Gemini API quota check ---
check_gemini() {
  local state=$(python3 -c "
import json
with open('$QUOTA_STATE') as f:
    d = json.load(f)
g = d.get('gemini', {})
today = '$today'
this_minute = '$this_minute'
# Reset daily counter
if g.get('last_reset_daily', '') != today:
    g['calls_daily'] = 0
    g['last_reset_daily'] = today
# Reset per-minute counter
if g.get('last_minute', '') != this_minute:
    g['calls_minute'] = 0
    g['last_minute'] = this_minute
d['gemini'] = g
with open('$QUOTA_STATE', 'w') as f:
    json.dump(d, f, indent=2)
# Limits (free tier: Flash 1500/day 15/min, Pro 50/day 2/min)
# Use conservative combined limits
limit_daily = 1000
limit_minute = 10
remaining_daily = max(0, limit_daily - g['calls_daily'])
remaining_minute = max(0, limit_minute - g['calls_minute'])
print(json.dumps({
    'backend': 'gemini',
    'available': remaining_daily > 0 and remaining_minute > 0,
    'remaining_daily': remaining_daily,
    'remaining_minute': remaining_minute,
    'used_daily': g['calls_daily'],
    'blocked': remaining_daily <= 0 or remaining_minute <= 0
}))
")
  echo "$state"
}

# --- Claude (always available) ---
check_claude() {
  echo '{"backend":"claude","available":true,"remaining":"unlimited","blocked":false}'
}

# --- Increment call counter (called AFTER successful dispatch) ---
if [ "${1:-}" = "increment" ]; then
  backend="${2:-}"
  python3 -c "
import json
with open('$QUOTA_STATE') as f:
    d = json.load(f)
if '$backend' == 'codex':
    d.setdefault('codex',{})
    d['codex']['calls_5h'] = d['codex'].get('calls_5h',0) + 1
    d['codex']['calls_weekly'] = d['codex'].get('calls_weekly',0) + 1
elif '$backend' == 'gemini':
    d.setdefault('gemini',{})
    d['gemini']['calls_daily'] = d['gemini'].get('calls_daily',0) + 1
    d['gemini']['calls_minute'] = d['gemini'].get('calls_minute',0) + 1
with open('$QUOTA_STATE','w') as f:
    json.dump(d,f,indent=2)
print('OK: incremented $backend')
"
  exit 0
fi

# --- Mark backend as blocked (called when rate limit error detected) ---
if [ "${1:-}" = "block" ]; then
  backend="${2:-}"
  duration="${3:-3600}"  # default 1 hour block
  python3 -c "
import json,time
with open('$QUOTA_STATE') as f:
    d = json.load(f)
d.setdefault('$backend',{})
d['$backend']['blocked_until'] = int(time.time()) + int('$duration')
with open('$QUOTA_STATE','w') as f:
    json.dump(d,f,indent=2)
print('BLOCKED: $backend for ${duration}s')
"
  exit 0
fi

# --- Main check ---
backend="${1:-all}"
any_blocked=0

if [ "$backend" = "all" ] || [ "$backend" = "codex" ]; then
  result=$(check_codex)
  echo "$result"
  echo "$result" | python3 -c "import json,sys;d=json.load(sys.stdin);exit(0 if d['available'] else 1)" || any_blocked=1
fi

if [ "$backend" = "all" ] || [ "$backend" = "gemini" ]; then
  result=$(check_gemini)
  echo "$result"
  echo "$result" | python3 -c "import json,sys;d=json.load(sys.stdin);exit(0 if d['available'] else 1)" || any_blocked=1
fi

if [ "$backend" = "all" ] || [ "$backend" = "claude" ]; then
  check_claude
fi

exit $any_blocked
