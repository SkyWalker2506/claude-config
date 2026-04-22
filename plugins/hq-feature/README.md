# HQ Feature Plugin

Cross-repo feature branch management via the ClaudeHQ `hq feature` CLI. Coordinate feature development spanning multiple repositories from a single command.

## Features

- Start feature branches across multiple repos simultaneously
- Commit, push, and open PRs across repos in one command
- Track feature status across all involved repos
- Safe abandon — cleans up branches if feature is dropped

## Requirements

| Requirement | Details |
|-------------|---------|
| Deps | `bash`, `python3` |
| External | ClaudeHQ at `~/Projects/ClaudeHQ/scripts/hq` |

## Usage

```bash
/hq-feature start <name> [--repos=A,B,C]
/hq-feature status <name>
/hq-feature commit <name> -m "message"
/hq-feature push <name>
/hq-feature pr <name> [--title "..."]
/hq-feature merge <name> [--auto]
/hq-feature abandon <name>
```

## Example

```bash
/hq-feature start gpt-integration --repos=claude-config,GptModels
/hq-feature commit gpt-integration -m "feat: add execution backends"
/hq-feature pr gpt-integration --title "feat: GPT models integration"
/hq-feature merge gpt-integration --auto
```

## Install

Installed as part of full claude-config setup via `./install.sh`. Requires ClaudeHQ to be present at `~/Projects/ClaudeHQ`.
