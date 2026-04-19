#!/usr/bin/env bash
# Git post-commit hook: mark .claude/graph-cache.json as stale if it exists.
# Runs inside the repo; full rebuild is deferred to 'hq graph build'.
set -euo pipefail

TOP="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[[ -z "$TOP" ]] && exit 0
CACHE="$TOP/.claude/graph-cache.json"
[[ -f "$CACHE" ]] || exit 0

CHANGED="$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null || true)"
[[ -z "$CHANGED" ]] && exit 0

python3 - "$CACHE" <<'PY' || true
import json, sys
from datetime import datetime, timezone
p = sys.argv[1]
try:
    with open(p) as f:
        g = json.load(f)
    g["stale"] = True
    g["last_commit_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    with open(p, "w") as f:
        json.dump(g, f, indent=2)
except Exception as e:
    print(f"graph cache update failed: {e}", file=sys.stderr)
PY

echo "[graph] cache marked stale — run 'hq graph build' to refresh"
