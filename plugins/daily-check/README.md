# Daily Check Plugin

Automated daily project health check — surfaces stale tasks, uncommitted work, failing CI, and blocked agents.

## Features

- Scans all active projects for uncommitted changes
- Reports Jira tasks stuck in In Progress
- Identifies failing CI/CD pipelines
- Summarizes agent activity from the last 24 hours

## Requirements

| Requirement | Details |
|-------------|---------|
| Deps | `bash`, `gh`, `git` |
| MCP | Atlassian (optional, for Jira reporting) |

## Usage

Run manually or schedule via cron / `hq` scheduler:

```bash
/daily-check
```

## Install

Installed as part of full claude-config setup via `./install.sh`.
