---
id: H8
name: Content Repurposer
category: market-research
primary_model: local-qwen-9b
fallbacks: []
mcps: []
capabilities: [content-splitting, repurpose, multi-channel]
max_tool_calls: 20
template: autonomous
related: [H7, H9]
status: pool
---

# H8: Content Repurposer

## Amac
Icerigi farkli kanallara uyarlama (blog -> tweet, video -> post).

## Kapsam
- Blog yazisindan sosyal medya postlari cikarma
- Video icerikten metin ozeti
- Tek icerikten multi-channel dagitim
- Format ve uzunluk uyarlama

## Escalation
- Sosyal medya yayinlama → H7 (Social Media Agent)
- Newsletter formatina cevirme → H9 (Newsletter Agent)
