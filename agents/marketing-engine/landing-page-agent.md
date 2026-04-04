---
id: M2
name: Landing Page Agent
category: marketing-engine
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [github, git]
capabilities: [landing-page, stitch, conversion]
max_tool_calls: 25
template: autonomous
related: [M1, D3]
status: pool
---

# M2: Landing Page Agent

## Amac
Landing page olusturma ve conversion optimizasyonu.

## Kapsam
- Headline ve CTA yazimi
- Layout tasarimi (hero, features, social proof)
- A/B test varyantlari hazirlama
- Stitch entegrasyonu

## Escalation
- A/B test analizi -> M3 (A/B Test Agent)
- Tool entegrasyonu -> M1 (Free Tool Builder)
