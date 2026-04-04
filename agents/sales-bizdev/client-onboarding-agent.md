---
id: O5
name: Client Onboarding Agent
category: sales-bizdev
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [atlassian]
capabilities: [onboarding-checklist, welcome-sequence, handoff, documentation]
max_tool_calls: 15
template: autonomous
related: [O2, I2]
status: pool
---

# O5: Client Onboarding Agent

## Amac
Musteri onboarding sureci — checklist, hosgeldin emaili, dokumantasyon.

## Kapsam
- Onboarding checklist olusturma
- Hosgeldin email dizisi
- Handoff dokumantasyonu
- Jira'da onboarding task'lari

## Escalation
- Sprint planlama → I2 (Sprint Planner)
- CRM guncelleme → O2 (CRM Agent)
