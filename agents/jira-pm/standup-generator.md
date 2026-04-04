---
id: I8
name: Standup Generator
category: jira-pm
primary_model: local-qwen-9b
fallbacks: []
mcps: [atlassian]
capabilities: [standup, daily-summary]
max_tool_calls: 10
template: autonomous
related: [I4, I7]
status: pool
---

# I8: Standup Generator

## Amac
Gunluk standup raporu olusturma — dun/bugun/blocker.

## Kapsam
- Dun tamamlanan isler (Done gecisleri)
- Bugun planli isler (In Progress)
- Blocker ve risk listesi
- Ozet format (3 baslik)

## Escalation
- Detayli rapor → I4 (Status Reporter)
- Velocity verisi gerekirse → I7 (Burndown Tracker)
