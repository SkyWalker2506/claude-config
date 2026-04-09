#!/bin/bash
# sync-mcp.sh — Sync MCP servers from settings.json → .claude.json
# Resolves ${VAR} env templates from secrets.env
# Run after install.sh or whenever MCP config changes

set -euo pipefail

SETTINGS="$HOME/.claude/settings.json"
CLAUDE_JSON="$HOME/.claude.json"
SECRETS="$HOME/.claude/secrets/secrets.env"

if [ ! -f "$SETTINGS" ]; then
  echo "ERROR: $SETTINGS not found"
  exit 1
fi

if [ ! -f "$CLAUDE_JSON" ]; then
  echo "SKIP: $CLAUDE_JSON not found (fresh install?)"
  exit 0
fi

python3 -c "
import json, sys, os, re

# Load secrets
secrets = {}
secrets_path = '$SECRETS'
if os.path.exists(secrets_path):
    with open(secrets_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                secrets[k.strip()] = v.strip()

with open('$SETTINGS') as f:
    settings = json.load(f)

with open('$CLAUDE_JSON') as f:
    claude = json.load(f)

src_mcps = settings.get('mcpServers', {})
dst_mcps = claude.get('mcpServers', {})

def resolve_env(val):
    \"\"\"Resolve \${VAR} from secrets.env\"\"\"
    m = re.match(r'^\\\$\{(.+)\}$', val)
    if m:
        key = m.group(1)
        if key in secrets:
            return secrets[key]
        else:
            print(f'  WARNING: {key} not in secrets.env — left as template')
    return val

# Sync: settings.json is source of truth
synced = {}
for k, v in src_mcps.items():
    entry = {'type': 'stdio', 'command': v['command'], 'args': v['args']}
    env = v.get('env', {})
    if env:
        resolved = {}
        for ek, ev in env.items():
            resolved[ek] = resolve_env(ev)
        entry['env'] = resolved
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
