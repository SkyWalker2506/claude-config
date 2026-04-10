#!/usr/bin/env bash
# Sync agent trees + agent-related JSON from claude-config clone → ~/.claude/
# Used by: install.sh (install_agents), SessionStart hook (every Claude open).
# Quiet on success; no network.
set -euo pipefail

ROOT="${1:-${CLAUDE_CONFIG_ROOT:-$HOME/Projects/claude-config}}"

if [ ! -d "$ROOT/agents" ]; then
  exit 0
fi

mkdir -p "$HOME/.claude/agents" "$HOME/.claude/config"

cp -r "$ROOT/agents/"* "$HOME/.claude/agents/" 2>/dev/null || true

for f in agent-registry.json fallback-chains.json model-tiers.json layer-contracts.json model-requirements.json openrouter-free-models.json; do
  if [ -f "$ROOT/config/$f" ]; then
    cp "$ROOT/config/$f" "$HOME/.claude/config/" 2>/dev/null || true
  fi
done

if [ -f "$ROOT/config/check-agent-deps.sh" ]; then
  cp "$ROOT/config/check-agent-deps.sh" "$HOME/.claude/config/" 2>/dev/null || true
  chmod +x "$HOME/.claude/config/check-agent-deps.sh" 2>/dev/null || true
fi

exit 0
