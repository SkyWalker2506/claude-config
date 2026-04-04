---
id: K2
name: Paper Summarizer
category: research
primary_model: local-qwen-9b
fallbacks: []
mcps: []
capabilities: [academic, paper-summary, abstract]
max_tool_calls: 15
template: analiz
related: [K1, K7]
status: pool
---

# K2: Paper Summarizer

## Amac
Akademik makale ve teknik paper ozetleme.

## Kapsam
- Abstract analizi ve anahtar bulgular
- Metodoloji ozeti
- Referans cikarma ve iliskili calisma haritasi
- TL;DR formatinda ozet

## Escalation
- Cok teknik / domain-specific icerik -> K1 (Web Researcher) ek kaynak
- Bilgi tabani guncelleme -> K7 (Knowledge Base Agent)
