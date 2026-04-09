#!/bin/bash
# sync-mcp.sh — Sync MCP servers from settings.json → .claude.json
# Run after install.sh or whenever MCP config changes
# This ensures both config files have the same MCP servers

set -euo pipefail

SETTINGS="$HOME/.claude/settings.json"
CLAUDE_JSON="$HOME/.claude.json"

if [ ! -f "$SETTINGS" ]; then
  echo "ERROR: $SETTINGS not found"
  exit 1
fi

if [ ! -f "$CLAUDE_JSON" ]; then
  echo "SKIP: $CLAUDE_JSON not found (fresh install?)"
  exit 0
fi

python3 -c "
import json, sys

with open('$SETTINGS') as f:
    settings = json.load(f)

with open('$CLAUDE_JSON') as f:
    claude = json.load(f)

src_mcps = settings.get('mcpServers', {})
dst_mcps = claude.get('mcpServers', {})

# Sync: settings.json is source of truth
synced = {}
for k, v in src_mcps.items():
    entry = {'type': 'stdio', 'command': v['command'], 'args': v['args']}
    env = v.get('env', {})
    if env:
        entry['env'] = env
    else:
        entry['env'] = {}
    synced[k] = entry

# Report changes
added = set(synced.keys()) - set(dst_mcps.keys())
removed = set(dst_mcps.keys()) - set(synced.keys())

claude['mcpServers'] = synced

with open('$CLAUDE_JSON', 'w') as f:
    json.dump(claude, f, indent=2)

if added:
    print(f'Added: {sorted(added)}')
if removed:
    print(f'Removed: {sorted(removed)}')
print(f'Synced {len(synced)} MCP servers')
"
