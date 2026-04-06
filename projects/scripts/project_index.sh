#!/usr/bin/env bash
# L0 Project Index Hook — outputs terse PROJECT_INDEX signal if .claude/index.md exists
# Silent when no index found (no noise for unindexed projects)

find_index() {
  local dir="$PWD"
  for _ in 1 2 3 4 5; do
    if [ -f "$dir/.claude/index.md" ]; then
      echo "$dir/.claude/index.md"
      return 0
    fi
    [ "$dir" = "/" ] && break
    dir="$(dirname "$dir")"
  done
  return 1
}

INDEX_FILE=$(find_index) || exit 0

# Parse frontmatter fields (---...--- block)
get_field() {
  local field="$1"
  sed -n '/^---$/,/^---$/p' "$INDEX_FILE" | grep "^${field}:" | head -1 | sed "s/^${field}:[[:space:]]*//"
}

PROJECT=$(get_field "project")
STACK=$(get_field "stack")
JIRA=$(get_field "jira")
FOCUS=$(get_field "focus")

# First non-empty, non-frontmatter body line
SUMMARY=$(awk '/^---$/{f=!f;next} f{next} NF{print;exit}' "$INDEX_FILE")

# Build signal
OUT="PROJECT_INDEX:"
[ -n "$PROJECT" ] && OUT="$OUT $PROJECT"
[ -n "$JIRA" ]    && OUT="$OUT ($JIRA)"
[ -n "$STACK" ]   && OUT="$OUT | $STACK"
[ -n "$SUMMARY" ] && OUT="$OUT | $SUMMARY"
[ -n "$FOCUS" ]   && OUT="$OUT | Focus: $FOCUS"

echo "$OUT"
