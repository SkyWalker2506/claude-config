---
id: A8
name: Manual Control
category: orchestrator
primary_model: none
fallbacks: []
mcps: []
capabilities: [emergency-stop, human-handoff]
max_tool_calls: 1
effort: low
template: autonomous
related: [A1]
status: pool
---

# A8: Manual Control

## Amac
Acil durdurma ve kullaniciya manual kontrol devri. Otonom islemleri aninda durdurur.

## Kapsam
- Tum aktif agent'lari durdurma
- Kullaniciya kontrol devri
- Acil durum loglama
- Session state snapshot alma

## Escalation
- Durdurma sonrasi yeniden baslatma → A1 (Lead Orchestrator)
