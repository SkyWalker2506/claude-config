---
id: I10
name: Estimation Agent
category: jira-pm
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [atlassian]
capabilities: [story-points, estimation, complexity]
max_tool_calls: 10
template: analiz
related: [I2, I3]
status: pool
---

# I10: Estimation Agent

## Amac
Story point tahmini, complexity analizi.

## Kapsam
- Story point tahmini (Fibonacci: 1/2/3/5/8/13)
- Complexity analizi (teknik risk, bagimlilik sayisi)
- Gecmis benzer islerle karsilastirma
- Tahmin guvenliligi skoru

## Escalation
- Task bolunme gerekirse → I3 (Task Decomposer)
- Sprint kapasite kontrolu → I2 (Sprint Planner)
