#!/bin/bash
# Team Build — Multi-agent autonomous development loop
# Usage: ~/Projects/claude-config/projects/scripts/team-build.sh [max_iterations]
# Run from project directory: cd ~/Projects/MyApp && ~/Projects/claude-config/projects/scripts/team-build.sh
#
# Prerequisites: jq, claude CLI, .team-build/config.json in project root

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
TB_DIR="$PROJECT_DIR/.team-build"
CONFIG_FILE="$TB_DIR/config.json"
REVIEW_NOTES="$TB_DIR/review-notes.md"
SPECS_DIR="$TB_DIR/specs"
REPORTS_DIR="$TB_DIR/reports"
CODE_PROMPT="$SCRIPT_DIR/team-build-prompt.md"
REVIEW_PROMPT="$SCRIPT_DIR/team-build-review-prompt.md"
MAX_ITERATIONS="${1:-10}"
START_TIME="$(date -u +%FT%TZ)"

# ── Dependency check ──
for cmd in jq claude; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: $cmd required."
    exit 1
  fi
done

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: $CONFIG_FILE not found."
  echo "Run: /team-build setup"
  exit 1
fi

if [ ! -f "$CODE_PROMPT" ]; then
  echo "Error: $CODE_PROMPT not found."
  echo "Run: cd ~/Projects/claude-config && ./install.sh"
  exit 1
fi

# ── Initialize ──
mkdir -p "$REPORTS_DIR"

# ── Watchdog heartbeat ──
TASK_ID="team_build_${PROJECT_NAME}_$$"
WATCHDOG_DIR="/tmp/watchdog"
mkdir -p "$WATCHDOG_DIR"

cleanup() {
  rm -f "$WATCHDOG_DIR/$TASK_ID.json"
}
trap cleanup EXIT

# ── Agent summary ──
TOTAL=$(jq '.agents | length' "$CONFIG_FILE" 2>/dev/null || echo "?")
DONE=$(jq '[.agents[] | select(.status == "done")] | length' "$CONFIG_FILE" 2>/dev/null || echo "0")
echo ""
echo "Team Build — $PROJECT_NAME"
echo "Agents: $DONE/$TOTAL complete — Max iterations: $MAX_ITERATIONS"
echo ""

# ── Main loop ──
for i in $(seq 1 $MAX_ITERATIONS); do
  echo "==============================================================="
  echo "  Iteration $i / $MAX_ITERATIONS"
  echo "==============================================================="

  # Update watchdog
  echo "{\"task\":\"team-build\",\"project\":\"$PROJECT_NAME\",\"iteration\":$i,\"max\":$MAX_ITERATIONS,\"status\":\"running\",\"ts\":\"$(date -u +%FT%TZ)\"}" > "$WATCHDOG_DIR/$TASK_ID.json"

  # Find next agent to work on (priority order, not done)
  NEXT_AGENT=$(jq -r '[.agents[] | select(.status != "done")] | sort_by(.priority) | .[0].id // empty' "$CONFIG_FILE" 2>/dev/null)

  if [ -z "$NEXT_AGENT" ]; then
    echo ""
    echo "All agents completed!"
    break
  fi

  AGENT_NAME=$(jq -r ".agents[] | select(.id == \"$NEXT_AGENT\") | .name" "$CONFIG_FILE")
  AGENT_MODEL=$(jq -r ".agents[] | select(.id == \"$NEXT_AGENT\") | .model // \"sonnet\"" "$CONFIG_FILE")
  AGENT_SPEC=$(jq -r ".agents[] | select(.id == \"$NEXT_AGENT\") | .specFile" "$CONFIG_FILE")

  echo "Agent: $NEXT_AGENT — $AGENT_NAME (model: $AGENT_MODEL)"
  echo "Spec: $AGENT_SPEC"

  # ── 3a: Code iteration (Sonnet/Haiku) ──
  echo "--- Code phase ($AGENT_MODEL) ---"

  # Build context: spec + review notes + previous reports
  CONTEXT=""
  CONTEXT+="## Current Agent\n"
  CONTEXT+="ID: $NEXT_AGENT\n"
  CONTEXT+="Name: $AGENT_NAME\n"
  CONTEXT+="Spec: $AGENT_SPEC\n\n"

  if [ -f "$REVIEW_NOTES" ]; then
    CONTEXT+="## Review Notes (from Opus)\n"
    CONTEXT+="$(cat "$REVIEW_NOTES")\n\n"
  fi

  # Pipe prompt + context to claude
  {
    cat "$CODE_PROMPT"
    echo ""
    echo "---"
    echo ""
    echo -e "$CONTEXT"
  } | claude --dangerously-skip-permissions --model "claude-$AGENT_MODEL-4-6" --print 2>&1 | tee /dev/stderr || true

  # Update agent status in config
  UPDATED=$(jq "(.agents[] | select(.id == \"$NEXT_AGENT\") | .status) = \"done\" | (.agents[] | select(.id == \"$NEXT_AGENT\") | .completedAt) = \"$(date -u +%FT%TZ)\"" "$CONFIG_FILE")
  echo "$UPDATED" > "$CONFIG_FILE"

  # Progress
  DONE=$(jq '[.agents[] | select(.status == "done")] | length' "$CONFIG_FILE" 2>/dev/null || echo "?")
  echo ""
  echo "Agent $NEXT_AGENT done. Progress: $DONE/$TOTAL"

  # ── 3b: Opus review (short, cheap) ──
  echo "--- Opus review phase ---"

  REVIEW_CONTEXT=""
  REVIEW_CONTEXT+="## Config\n$(cat "$CONFIG_FILE")\n\n"

  # Gather all reports
  for report in "$REPORTS_DIR"/*.md; do
    if [ -f "$report" ]; then
      REVIEW_CONTEXT+="## Report: $(basename "$report")\n$(cat "$report")\n\n"
    fi
  done

  {
    cat "$REVIEW_PROMPT"
    echo ""
    echo "---"
    echo ""
    echo -e "$REVIEW_CONTEXT"
  } | claude --dangerously-skip-permissions --model claude-opus-4-6 --print 2>&1 | tee /dev/stderr || true

  # Check if all done
  REMAINING=$(jq '[.agents[] | select(.status != "done")] | length' "$CONFIG_FILE" 2>/dev/null || echo "?")
  if [ "$REMAINING" = "0" ]; then
    echo ""
    echo "==============================================================="
    echo "  ALL AGENTS COMPLETED!"
    echo "==============================================================="

    # Final report
    echo "--- Generating final report ---"
    {
      echo "Generate a final summary report. Read all files in .team-build/reports/ and write .team-build/final-report.md with:"
      echo "- Overall status"
      echo "- What each agent built"
      echo "- Files created/modified"
      echo "- Lessons learned"
      echo "- Suggested next steps"
    } | claude --dangerously-skip-permissions --model claude-sonnet-4-6 --print 2>&1 | tee /dev/stderr || true

    # Watchdog success
    FEEDBACK_DIR="$HOME/Projects/.watchdog"
    mkdir -p "$FEEDBACK_DIR"
    echo "{\"id\":\"$TASK_ID\",\"task\":\"team-build\",\"project\":\"$PROJECT_NAME\",\"outcome\":\"success\",\"iterations\":$i,\"max\":$MAX_ITERATIONS,\"ended\":\"$(date -u +%FT%TZ)\"}" >> "$FEEDBACK_DIR/feedback.jsonl"
    exit 0
  fi

  echo "Iteration $i done. Agents: $DONE/$TOTAL. Continuing in 2s..."
  sleep 2
done

echo ""
echo "Team Build reached max iterations ($MAX_ITERATIONS)."
echo "Progress: $DONE/$TOTAL agents done."

# Watchdog incomplete
FEEDBACK_DIR="$HOME/Projects/.watchdog"
mkdir -p "$FEEDBACK_DIR"
echo "{\"id\":\"$TASK_ID\",\"task\":\"team-build\",\"project\":\"$PROJECT_NAME\",\"outcome\":\"incomplete\",\"iterations\":$MAX_ITERATIONS,\"agents_done\":$DONE,\"agents_total\":$TOTAL,\"ended\":\"$(date -u +%FT%TZ)\"}" >> "$FEEDBACK_DIR/feedback.jsonl"
exit 1
