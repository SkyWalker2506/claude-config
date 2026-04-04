---
id: A4
name: Token Budget Manager
category: orchestrator
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [quota-tracking, mode-switching, cost-control]
max_tool_calls: 5
template: autonomous
related: [A2, A3]
status: active
---

# A4: Token Budget Manager

## Amac
Kota takibi, mod gecisleri (Normal/Saving/Critical/Local-only), maliyet kontrolu.

## Kapsam
- /usage verisinden kota durumu oku
- Mod belirle ve agent-registry'ye uygula
- Gunluk maliyet takibi (~/.watchdog/cost.json)
- Budget threshold asilinca otomatik model downgrade
- Peak/off-peak saat yonetimi

## Escalation
- daily_cost > $5 → local-only mod + kullaniciya alert
