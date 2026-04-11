#!/usr/bin/env bash
# Sync core prompt + skills + agent trees + agent-related JSON from claude-config clone → ~/.claude/
# Used by: install.sh (install_agents), SessionStart hook (every Claude open).
# Quiet on success; no network.
set -euo pipefail

ROOT="${1:-${CLAUDE_CONFIG_ROOT:-$HOME/Projects/claude-config}}"

if [ ! -d "$ROOT/agents" ]; then
  exit 0
fi

mkdir -p "$HOME/.claude/agents" "$HOME/.claude/config" "$HOME/.claude/skills"

if [ -f "$ROOT/global/CLAUDE.md" ]; then
  cp "$ROOT/global/CLAUDE.md" "$HOME/.claude/CLAUDE.md" 2>/dev/null || true
fi

if [ -d "$ROOT/global/skills" ]; then
  for skill_dir in "$ROOT"/global/skills/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    mkdir -p "$HOME/.claude/skills/$skill_name"
    cp -r "$skill_dir"* "$HOME/.claude/skills/$skill_name/" 2>/dev/null || true
  done
fi

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

if command -v python3 >/dev/null 2>&1 && [ -f "$ROOT/scripts/generate_runtime_agent_mirrors.py" ]; then
  python3 "$ROOT/scripts/generate_runtime_agent_mirrors.py" --root "$ROOT" --runtime-agents "$HOME/.claude/agents" >/dev/null 2>&1 || true
fi

exit 0
