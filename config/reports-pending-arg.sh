#!/bin/bash
# reports-pending-arg.sh — Check for pending reports and echo the initial prompt arg
# Usage: initial_arg="$(bash ~/Projects/claude-config/config/reports-pending-arg.sh)"
#        [ -n "$initial_arg" ] && exec real_claude "$initial_arg" || exec real_claude
# Outputs the initial prompt string if pending reports exist, empty string otherwise.

REPORTS_DIR="$HOME/Projects/claude-config/Reports"

for f in "$REPORTS_DIR"/*.md; do
  [ -f "$f" ] || continue
  case "$(basename "$f")" in
    REPORTS_SUMMARY.md|TEMPLATE.md) continue ;;
  esac
  status=""
  while IFS= read -r line; do
    stripped="${line#> }"
    if [[ "$stripped" =~ ^[Ss]tatus:[[:space:]]*(.*) ]]; then
      status="$(echo "${BASH_REMATCH[1]}" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')"
      break
    fi
  done < <(head -n 10 "$f" 2>/dev/null)
  case "$status" in
    DONE) continue ;;
    IN_PROGRESS)
      if [[ "$(uname)" == "Darwin" ]]; then
        mtime=$(stat -f '%m' "$f" 2>/dev/null || echo 0)
      else
        mtime=$(stat -c '%Y' "$f" 2>/dev/null || echo 0)
      fi
      age=$(( $(date +%s) - mtime ))
      [ "$age" -lt 1800 ] && continue ;;
  esac
  fname="$(basename "$f")"
  echo "REPORTS_PENDING: $fname bekliyor. Raporu oku, Required Actions'ları özetle, uygulayayım mı diye sor."
  exit 0
done
exit 0
