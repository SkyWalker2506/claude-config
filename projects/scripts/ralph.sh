#!/bin/bash
# Ralph — Autonomous AI agent loop for Claude Code
# Usage: ~/Projects/scripts/ralph.sh [max_iterations]
# Run from project directory: cd ~/Projects/MyApp && ~/Projects/scripts/ralph.sh
#
# Prerequisites: jq (brew install jq), claude CLI, prd.json in project root
# Create prd.json: /prd → /ralph

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
PRD_FILE="$PROJECT_DIR/prd.json"
PROGRESS_FILE="$PROJECT_DIR/progress.txt"
ARCHIVE_DIR="$PROJECT_DIR/archive"
LAST_BRANCH_FILE="$PROJECT_DIR/.ralph-last-branch"
PROMPT_FILE="$SCRIPT_DIR/ralph-prompt.md"
MAX_ITERATIONS="${1:-10}"
START_TIME="$(date -u +%FT%TZ)"

# ── Dependency check ──
if ! command -v jq &>/dev/null; then
  echo "Error: jq required. Install: brew install jq"
  exit 1
fi

if ! command -v claude &>/dev/null; then
  echo "Error: claude CLI required. Install: npm install -g @anthropic-ai/claude-code"
  exit 1
fi

if [ ! -f "$PRD_FILE" ]; then
  echo "Error: $PRD_FILE not found."
  echo "Create one: /prd → /ralph"
  exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "Error: $PROMPT_FILE not found."
  echo "Run: cd ~/Projects/claude-config && ./install.sh"
  exit 1
fi

# ── Archive previous run if branch changed ──
if [ -f "$LAST_BRANCH_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  LAST_BRANCH=$(cat "$LAST_BRANCH_FILE" 2>/dev/null || echo "")

  if [ -n "$CURRENT_BRANCH" ] && [ -n "$LAST_BRANCH" ] && [ "$CURRENT_BRANCH" != "$LAST_BRANCH" ]; then
    DATE=$(date +%Y-%m-%d)
    FOLDER_NAME=$(echo "$LAST_BRANCH" | sed 's|^ralph/||')
    ARCHIVE_FOLDER="$ARCHIVE_DIR/$DATE-$FOLDER_NAME"

    echo "Archiving previous run: $LAST_BRANCH → $ARCHIVE_FOLDER"
    mkdir -p "$ARCHIVE_FOLDER"
    [ -f "$PRD_FILE" ] && cp "$PRD_FILE" "$ARCHIVE_FOLDER/"
    [ -f "$PROGRESS_FILE" ] && cp "$PROGRESS_FILE" "$ARCHIVE_FOLDER/"

    # Reset progress for new feature
    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Project: $PROJECT_NAME" >> "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
  fi
fi

# ── Track current branch ──
CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
if [ -n "$CURRENT_BRANCH" ]; then
  echo "$CURRENT_BRANCH" > "$LAST_BRANCH_FILE"
fi

# ── Initialize progress file ──
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Ralph Progress Log" > "$PROGRESS_FILE"
  echo "Project: $PROJECT_NAME" >> "$PROGRESS_FILE"
  echo "Started: $(date)" >> "$PROGRESS_FILE"
  echo "---" >> "$PROGRESS_FILE"
fi

# ── Watchdog heartbeat ──
TASK_ID="ralph_${PROJECT_NAME}_$$"
WATCHDOG_DIR="/tmp/watchdog"
mkdir -p "$WATCHDOG_DIR"

cleanup() {
  rm -f "$WATCHDOG_DIR/$TASK_ID.json"
}
trap cleanup EXIT

# ── Story summary ──
TOTAL=$(jq '.userStories | length' "$PRD_FILE" 2>/dev/null || echo "?")
DONE=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE" 2>/dev/null || echo "?")
echo ""
echo "Ralph — $PROJECT_NAME"
echo "Stories: $DONE/$TOTAL complete — Max iterations: $MAX_ITERATIONS"
echo ""

# ── Main loop ──
for i in $(seq 1 $MAX_ITERATIONS); do
  echo "==============================================================="
  echo "  Iteration $i / $MAX_ITERATIONS"
  echo "==============================================================="

  # Update watchdog
  echo "{\"task\":\"ralph\",\"project\":\"$PROJECT_NAME\",\"iteration\":$i,\"max\":$MAX_ITERATIONS,\"status\":\"running\",\"ts\":\"$(date -u +%FT%TZ)\"}" > "$WATCHDOG_DIR/$TASK_ID.json"

  # Run Claude Code with ralph prompt
  OUTPUT=$(claude --dangerously-skip-permissions --print < "$PROMPT_FILE" 2>&1 | tee /dev/stderr) || true

  # Check for completion
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "Ralph completed all stories!"
    echo "Finished at iteration $i / $MAX_ITERATIONS"

    # Watchdog success feedback
    FEEDBACK_DIR="$HOME/Projects/.watchdog"
    mkdir -p "$FEEDBACK_DIR"
    echo "{\"id\":\"$TASK_ID\",\"task\":\"ralph\",\"project\":\"$PROJECT_NAME\",\"outcome\":\"success\",\"iterations\":$i,\"max\":$MAX_ITERATIONS,\"ended\":\"$(date -u +%FT%TZ)\"}" >> "$FEEDBACK_DIR/feedback.jsonl"
    exit 0
  fi

  # Progress update
  DONE=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE" 2>/dev/null || echo "?")
  echo "Iteration $i done. Stories: $DONE/$TOTAL. Continuing in 2s..."
  sleep 2  # Rate limit — fresh context icin kisa bekleme
done

echo ""
echo "Ralph reached max iterations ($MAX_ITERATIONS) without completing all stories."
echo "Progress: $DONE/$TOTAL stories done."
echo "Check: $PROGRESS_FILE"

# Watchdog incomplete feedback
FEEDBACK_DIR="$HOME/Projects/.watchdog"
mkdir -p "$FEEDBACK_DIR"
echo "{\"id\":\"$TASK_ID\",\"task\":\"ralph\",\"project\":\"$PROJECT_NAME\",\"outcome\":\"incomplete\",\"iterations\":$MAX_ITERATIONS,\"stories_done\":$DONE,\"stories_total\":$TOTAL,\"ended\":\"$(date -u +%FT%TZ)\"}" >> "$FEEDBACK_DIR/feedback.jsonl"
exit 1
