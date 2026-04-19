#!/usr/bin/env bash
# SessionStart hook: emit concise summary from .claude/graph-cache.json if present.
# Claude-Code SessionStart hooks read JSON input on stdin; we only need cwd heuristics
# so we just ignore stdin. Output goes to stdout — becomes part of session context.
set -euo pipefail

# Best-effort: pick project root from env, else PWD.
ROOT="${CLAUDE_PROJECT_DIR:-${PWD}}"
CACHE="$ROOT/.claude/graph-cache.json"
[[ -f "$CACHE" ]] || exit 0

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
stale = g.get("stale", False)
built = g.get("built_at", "?")

def deg(n):
    try:
        return int(n.get("degree") or 0)
    except Exception:
        return 0

top = sorted(nodes, key=deg, reverse=True)[:10]
top_names = [str(n.get("name") or n.get("id") or "?") for n in top]

docs = [n for n in nodes if n.get("type") == "doc"]

print(f"GRAPH_CACHE: {len(nodes)} nodes, {len(edges)} edges, {len(communities)} communities")
if top_names:
    print("Top hubs: " + ", ".join(top_names))
if docs:
    print(f"Docs indexed: {len(docs)}")
print(f"Built: {built}" + (" (STALE — run 'hq graph build')" if stale else ""))
PY
