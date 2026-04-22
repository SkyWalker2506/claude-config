# Sync Agents Plugin

Synchronizes agent definitions from `claude-config` to all downstream repos — `claude-agent-catalog`, `~/.claude/agents/`, and any project-local agent mirrors.

## Features

- Push updated AGENT.md files to `claude-agent-catalog`
- Mirror agents to `~/.claude/agents/` for local activation
- Detect and report agent definition drift between source and mirrors
- Dry-run mode to preview changes before syncing

## Requirements

| Requirement | Details |
|-------------|---------|
| Deps | `bash`, `gh`, `git` |
| External | `claude-agent-catalog` repo checked out locally |

## Usage

```bash
/sync-agents                  # sync all agents
/sync-agents --dry-run        # preview changes
/sync-agents --agent <name>   # sync a specific agent
/sync-agents --catalog-only   # push to catalog only
/sync-agents --local-only     # mirror to ~/.claude/agents/ only
```

## Sync Flow

1. Read source from `~/Projects/claude-config/agents/**/*.md`
2. Compare against `claude-agent-catalog` repo and `~/.claude/agents/`
3. Push diffs, commit to catalog, copy to local mirror
4. Report summary of synced / up-to-date / failed agents

## Install

Installed as part of full claude-config setup via `./install.sh`.
