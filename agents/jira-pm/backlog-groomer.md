---
id: I6
name: Backlog Groomer
category: jira-pm
primary_model: local-qwen-9b
fallbacks: []
mcps: [atlassian]
capabilities: [backlog-cleanup, prioritization]
max_tool_calls: 15
template: autonomous
related: [I2, I3]
status: pool
---

# I6: Backlog Groomer

## Amac
Backlog temizligi, onceliklendirme, stale issue tespiti.

## Kapsam
- Stale issue tespiti (30+ gun hareketsiz)
- Duplicate issue birlesturme onerisi
- Oncelik guncelleme (MoSCoW veya WSJF)
- Backlog buyukluk raporu

## Escalation
- Sprint planlama → I2 (Sprint Planner)
- Task bolunme gerekirse → I3 (Task Decomposer)
