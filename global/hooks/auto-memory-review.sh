#!/usr/bin/env bash
# auto-memory-review.sh
# Runs at session end (Stop hook) in the background.
# Spawns a headless Claude to review the transcript and update auto-memory.
# Never blocks session exit; skips if transcript is trivial or another instance is running.

set -u

LOG_DIR="$HOME/.claude/logs"
LOG_FILE="$LOG_DIR/auto-memory-review.log"
LOCK_FILE="$HOME/.claude/logs/auto-memory-review.pid"
MEMORY_DIR="/Users/musabkara/.claude/projects/-Users-musabkara-Projects-ClaudeHQ/memory"

mkdir -p "$LOG_DIR" 2>/dev/null || exit 0

ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(ts)] $*" >> "$LOG_FILE" 2>/dev/null || true; }

# ── PID lock (skip if another instance running) ──
if [ -f "$LOCK_FILE" ]; then
  other_pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
  if [ -n "$other_pid" ] && kill -0 "$other_pid" 2>/dev/null; then
    log "skip: already running (pid=$other_pid)"
    exit 0
  fi
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# ── Locate transcript ──
# Claude Code provides CLAUDE_TRANSCRIPT_PATH; fall back to newest transcript.
TRANSCRIPT="${CLAUDE_TRANSCRIPT_PATH:-}"
if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  TRANSCRIPT=$(ls -t "$HOME/.claude/projects/"*/*.jsonl 2>/dev/null | head -1)
fi

if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
  log "skip: no transcript found"
  exit 0
fi

# ── Gate on size (> 20KB ≈ ~10+ substantive turns) ──
size=$(wc -c < "$TRANSCRIPT" 2>/dev/null | tr -d ' ')
if [ -z "$size" ] || [ "$size" -lt 20480 ]; then
  log "skip: transcript too small ($size bytes) — $TRANSCRIPT"
  exit 0
fi

# ── Prefer user-turn count if jq available ──
if command -v jq >/dev/null 2>&1; then
  user_turns=$(jq -r 'select(.type=="user") | .uuid' "$TRANSCRIPT" 2>/dev/null | wc -l | tr -d ' ')
  if [ -n "$user_turns" ] && [ "$user_turns" -lt 10 ]; then
    log "skip: only $user_turns user turns — $TRANSCRIPT"
    exit 0
  fi
fi

# ── Ensure claude binary exists ──
if ! command -v claude >/dev/null 2>&1; then
  log "skip: claude CLI not on PATH"
  exit 0
fi

log "start: transcript=$TRANSCRIPT size=$size"

PROMPT="Review this session transcript at path: $TRANSCRIPT

Scan for new/updated facts matching types (user, feedback, project, reference) per the auto-memory rules in ~/.claude/CLAUDE.md. For each finding, write/update a file in $MEMORY_DIR/ and update MEMORY.md index.

Rules:
- Read $MEMORY_DIR/MEMORY.md FIRST — do NOT duplicate existing entries.
- Be conservative: only save surprising/non-obvious info that will matter in future sessions.
- Never save secret values, API keys, or credentials.
- Keep each memory file short (under 40 lines).
- Update MEMORY.md index with a one-line pointer for any new file."

# Run headless, detached. Log output.
(
  claude -p --model sonnet "$PROMPT" >> "$LOG_FILE" 2>&1
  rc=$?
  log "end: exit=$rc"
) &

disown 2>/dev/null || true
exit 0
