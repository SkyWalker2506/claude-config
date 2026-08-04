#!/usr/bin/env bash
# SessionStart hook: emit a concise summary from .claude/graph-cache.json.
# Rebuilds the cache in place when it is stale (the rebuild takes ~0.1s, so
# nagging the user to run it by hand was pure per-session noise).
# Claude-Code SessionStart hooks read JSON on stdin; we ignore it and use cwd.
set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-${PWD}}"
CACHE="$ROOT/.claude/graph-cache.json"
[[ -f "$CACHE" ]] || exit 0

# Auto-refresh when older than 7 days, if this project ships an hq CLI.
MAX_AGE_DAYS=7
mtime=$(stat -f %m "$CACHE" 2>/dev/null || stat -c %Y "$CACHE" 2>/dev/null || echo "")
if [[ -n "$mtime" ]]; then
    age=$(( ( $(date +%s) - mtime ) / 86400 ))
    if (( age > MAX_AGE_DAYS )) && [[ -x "$ROOT/scripts/hq" ]]; then
        "$ROOT/scripts/hq" graph build "$(basename "$ROOT")" >/dev/null 2>&1 || true
    fi
fi

python3 - "$CACHE" <<'PY'
import json, sys

p = sys.argv[1]
try:
    with open(p) as f:
        g = json.load(f)
except Exception as e:
    print(f"GRAPH_CACHE: unreadable ({e})", file=sys.stderr)
    sys.exit(0)

nodes = g.get("nodes", []) or []
edges = g.get("edges", []) or []
communities = g.get("communities", []) or []


def deg(n):
    try:
        return int(n.get("degree") or 0)
    except Exception:
        return 0


hubs, seen = [], set()
for n in sorted(nodes, key=deg, reverse=True):
    name = str(n.get("name") or n.get("id") or "?")
    if name in seen:
        continue
    seen.add(name)
    hubs.append(name)
    if len(hubs) == 5:
        break

line = f"GRAPH_CACHE: {len(nodes)} nodes, {len(edges)} edges, {len(communities)} communities"
if g.get("stale"):
    line += " (STALE)"
print(line)
if hubs:
    print("Top hubs: " + ", ".join(hubs))
PY
