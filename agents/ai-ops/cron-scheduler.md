---
id: G8
name: Cron Scheduler
category: ai-ops
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [cron, scheduling, launchd]
max_tool_calls: 5
template: autonomous
related: [A6, G2]
status: pool
---

# G8: Cron Scheduler

## Amac
Zamanlanmis gorevleri yonetme — cron/launchd.

## Kapsam
- Cron job olusturma ve duzenleme
- macOS launchd plist yonetimi
- Zamanlama stratejisi (gunluk/haftalik/olay bazli)
- Mevcut zamanlanmis gorev listesi

## Escalation
- Zamanlanmis gorev basarisiz → A6 (Notification Agent) alert
- Cron catismasi → G2 (Model Monitor) ile koordine
