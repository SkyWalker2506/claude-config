# GPT Import Plugin

Import and distill leaked GPT system prompts into agent knowledge files for the claude-config agent registry.

## Features

- Fetches prompts from `linexjlin/GPTs` GitHub repository
- Distills raw system prompts into structured AGENT.md knowledge sections
- Integrates with existing agent categories in `agents/`

## Requirements

| Requirement | Details |
|-------------|---------|
| Deps | `bash`, `gh` |
| External | `linexjlin/GPTs` on GitHub |

## Usage

```bash
/gpt-import <gpt-name>
/gpt-import --list          # browse available GPT prompts
/gpt-import --all           # bulk import all
```

## Output

Creates or updates knowledge files under `agents/{category}/{agent-name}/knowledge/`.

## Install

This is a skill-type plugin — no file installation required. Invoked directly via `/gpt-import`.
