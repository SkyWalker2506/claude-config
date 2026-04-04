---
id: M3
name: A/B Test Agent
category: marketing-engine
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [ab-test, variant, analytics]
max_tool_calls: 10
template: autonomous
related: [M2, M4]
status: pool
---

# M3: A/B Test Agent

## Amac
A/B test planlama ve sonuc analizi.

## Kapsam
- Test hipotezi olusturma
- Varyant tanimlama ve setup
- Istatistiksel anlam hesaplama
- Kazanan varyant secimi ve rapor

## Escalation
- Traffic analizi gerektiren test -> M4 (Analytics Agent)
- Landing page varyantlari -> M2 (Landing Page Agent)
