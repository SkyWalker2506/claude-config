#!/bin/bash
# auto-dream.sh — Weekly memory consolidation routine.
#
# For each ~/.claude/projects/*/memory/ directory, spawns a Sonnet session
# that reviews MEMORY.md + memory/*.md, merges duplicates, drops stale
# entries (referencing non-existent paths or contradicting current state),
# tightens descriptions, and rewrites MEMORY.md index. Conservative —
# when in doubt, keep.
#
# Single-instance via pid lock. Logs to ~/.claude/logs/auto-dream.log.

set -euo pipefail

LOG_DIR="$HOME/.claude/logs"
LOCK_FILE="$HOME/.claude/auto-dream.pid"
mkdir -p "$LOG_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

# Single-instance pid lock
if [ -f "$LOCK_FILE" ]; then
  existing_pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
  if [ -n "$existing_pid" ] && kill -0 "$existing_pid" 2>/dev/null; then
    log "auto-dream already running (pid $existing_pid) — exiting"
    exit 0
  fi
  rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# Resolve claude CLI
CLAUDE_BIN="$(command -v claude || true)"
if [ -z "$CLAUDE_BIN" ]; then
  log "claude CLI not found on PATH — aborting"
  exit 1
fi

PROJECTS_DIR="$HOME/.claude/projects"
if [ ! -d "$PROJECTS_DIR" ]; then
  log "No projects dir at $PROJECTS_DIR — nothing to consolidate"
  exit 0
fi

PROMPT='Read MEMORY.md and all memory/*.md files here. Consolidate: merge duplicates, drop stale entries (reference files/paths that no longer exist OR contradict current state), tighten descriptions. Rewrite MEMORY.md index. Be conservative — when in doubt, keep. Output only the final state of MEMORY.md index after rewrite; do not ask questions.'

log "=== auto-dream start ==="
total=0
processed=0

for memdir in "$PROJECTS_DIR"/*/memory/; do
  [ -d "$memdir" ] || continue
  total=$((total + 1))
  project_name="$(basename "$(dirname "$memdir")")"

  if [ ! -f "$memdir/MEMORY.md" ]; then
    log "skip $project_name — no MEMORY.md"
    continue
  fi

  log "consolidating: $project_name ($memdir)"

  (
    cd "$memdir" || exit 0
    if timeout 600 "$CLAUDE_BIN" -p --model sonnet "$PROMPT" >>"$LOG_DIR/auto-dream.log" 2>&1; then
      echo "[$(date '+%H:%M:%S')] ✅ $project_name consolidated" >>"$LOG_DIR/auto-dream.log"
    else
      echo "[$(date '+%H:%M:%S')] ⚠️ $project_name consolidation failed/timeout" >>"$LOG_DIR/auto-dream.log"
    fi
  )
  processed=$((processed + 1))
done

log "=== auto-dream done — $processed/$total memory dirs processed ==="
