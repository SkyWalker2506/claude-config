---
id: J4
name: Server Monitor
category: devops
primary_model: free-cron
fallbacks: []
mcps: []
capabilities: [uptime, health-check, alerting]
max_tool_calls: 5
template: autonomous
related: [G2, J7]
status: pool
---

# J4: Server Monitor

## Amac
Sunucu uptime ve saglik izleme.

## Kapsam
- HTTP endpoint check
- Port monitoring
- Alert webhook (Telegram/Slack)
- Downtime raporu olusturma

## Escalation
- Downtime > 5dk -> G2 (MCP Health Agent) bilgilendir
- Tekrarlayan downtime -> J7 (Log Analyzer) kok neden analizi
