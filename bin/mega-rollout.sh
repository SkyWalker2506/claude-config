#!/usr/bin/env bash
# Mega-prompt rollout — status / verify
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS="$ROOT/agents"

cmd="${1:-status}"

count_placeholder() {
  local pat="$1"
  # Şablon klasörü gerçek agent sayımına dahil edilmez
  grep -rl "$pat" "$AGENTS" --include="AGENT.md" --exclude-dir=_template 2>/dev/null | wc -l | tr -d ' '
}

knowledge_count() {
  find "$AGENTS" -path "*/knowledge/*.md" ! -name "_index.md" 2>/dev/null | wc -l | tr -d ' '
}

case "$cmd" in
  status|verify)
    echo "=== Mega rollout status ($ROOT) ==="
    echo "Bridge placeholder (Hangi alanlarla): $(count_placeholder 'Hangi alanlarla')"
    echo "Output placeholder (Ciktinin formati):   $(count_placeholder 'Ciktinin formati')"
    echo "Identity placeholder (Cursor dolduracak): $(count_placeholder 'Cursor dolduracak')"
    echo "Knowledge files (excl _index):        $(knowledge_count)"
    qr=$(grep -rsl "## Quick Reference" "$AGENTS" --include="*.md" 2>/dev/null | grep '/knowledge/' | grep -v '_index.md' | wc -l | tr -d ' ')
    dd=$(grep -rsl "Deep Dive Sources" "$AGENTS" --include="*.md" 2>/dev/null | grep '/knowledge/' | grep -v '_index.md' | wc -l | tr -d ' ')
    echo "Knowledge with Quick Reference:     $qr"
    echo "Knowledge with Deep Dive Sources:      $dd"
    echo ""
    echo "Target (mega-prompt): first 3 placeholders = 0, knowledge >= 660"
    ;;
  list)
    echo "Batch manifest: $ROOT/cursor-prompts/MEGA_BATCH_MANIFEST.md"
    echo "Worker index:   $ROOT/cursor-prompts/mega-workers/README.md"
    echo "Worker template: $ROOT/cursor-prompts/mega-workers/WORKER_PROMPT.md"
    echo ""
    echo "Worker scope files:"
    for w in W1-orchestrator W2-code-review W3-design W4-devops W5-data-analytics \
             W6-ai-ops W7-jira-pm W8-research W9-market-research W10-marketing-engine \
             W11-productivity W12-agent-builder W13-sales-bizdev W14-3d-cad W15-unity-backend-skeleton; do
      f="$ROOT/cursor-prompts/mega-workers/${w}.md"
      if [[ -f "$f" ]]; then echo "  $f"; else echo "  (missing) $f"; fi
    done
    ;;
  *)
    echo "Usage: $0 {status|verify|list}" >&2
    exit 1
    ;;
esac
