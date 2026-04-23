#!/usr/bin/env bash
# hive-append.sh — Append a task record to the shared hive log.
#
# Usage:
#   hive-append.sh --agent <name> --status <done|failed|started> --summary "<text>"
#
# Appends one JSONL line to ~/.claude/hive/tasks.jsonl with a UTC timestamp.
# Creates the directory if missing. Voluntary call from agent workflows.

set -euo pipefail

AGENT=""
STATUS=""
SUMMARY=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent)   AGENT="${2:-}"; shift 2 ;;
        --status)  STATUS="${2:-}"; shift 2 ;;
        --summary) SUMMARY="${2:-}"; shift 2 ;;
        -h|--help)
            grep '^#' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo "hive-append: unknown arg: $1" >&2
            exit 2
            ;;
    esac
done

if [[ -z "$AGENT" || -z "$STATUS" || -z "$SUMMARY" ]]; then
    echo "Usage: hive-append.sh --agent <name> --status <done|failed|started> --summary \"<text>\"" >&2
    exit 2
fi

case "$STATUS" in
    done|failed|started) ;;
    *) echo "hive-append: status must be one of: done, failed, started" >&2; exit 2 ;;
esac

HIVE_DIR="${HIVE_DIR:-$HOME/.claude/hive}"
HIVE_LOG="$HIVE_DIR/tasks.jsonl"
mkdir -p "$HIVE_DIR"

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if command -v jq >/dev/null 2>&1; then
    jq -cn \
        --arg ts "$TS" \
        --arg agent "$AGENT" \
        --arg status "$STATUS" \
        --arg summary "$SUMMARY" \
        '{ts:$ts, agent:$agent, status:$status, summary:$summary}' \
        >> "$HIVE_LOG"
else
    # Fallback: manual JSON with minimal escaping (quotes + backslashes)
    esc() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }
    printf '{"ts":"%s","agent":"%s","status":"%s","summary":"%s"}\n' \
        "$(esc "$TS")" "$(esc "$AGENT")" "$(esc "$STATUS")" "$(esc "$SUMMARY")" \
        >> "$HIVE_LOG"
fi

echo "hive-append: recorded $AGENT/$STATUS @ $TS"
