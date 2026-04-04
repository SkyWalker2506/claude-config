---
id: I9
name: Retrospective Agent
category: jira-pm
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [atlassian]
capabilities: [retrospective, lessons-learned]
max_tool_calls: 15
template: analiz
related: [I2, A7]
status: pool
---

# I9: Retrospective Agent

## Amac
Sprint retrospective analizi — iyi giden/kotu giden/aksiyon.

## Kapsam
- Sprint metrikleri ozeti (velocity, tamamlanma orani)
- Iyi giden (keep doing) listesi
- Kotu giden (stop doing) listesi
- Aksiyon maddeleri onerisi

## Escalation
- Sprint planlama iyilestirmesi → I2 (Sprint Planner)
- Surec degisikligi → A7 (Process Improvement Agent)
