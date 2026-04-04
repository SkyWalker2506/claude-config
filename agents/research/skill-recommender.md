---
id: K8
name: Skill Recommender
category: research
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: []
capabilities: [skill-gap, tool-recommendation]
max_tool_calls: 10
template: analiz
related: [K4, H10]
status: pool
---

# K8: Skill Recommender

## Amac
Yetenek acigi analizi ve arac onerisi.

## Kapsam
- Mevcut yetenekler vs hedef karsilastirmasi
- Eksik skill tespiti
- Tool ve framework onerisi
- Ogrenme yol haritasi olusturma

## Escalation
- Trend bilgisi gerektiren oneri -> K4 (Trend Analyzer)
- Arac entegrasyonu -> H10 (ilgili entegrasyon agent)
