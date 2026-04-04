---
id: H9
name: Newsletter Agent
category: market-research
primary_model: local-qwen-9b
fallbacks: []
mcps: []
capabilities: [newsletter, email-copy, segmentation]
max_tool_calls: 15
template: autonomous
related: [H8, L1]
status: pool
---

# H9: Newsletter Agent

## Amac
Newsletter icerik uretimi, email kopyasi yazma.

## Kapsam
- Haftalik/aylik newsletter icerik uretimi
- Email kopyasi (subject line, body, CTA)
- Hedef kitle segmentasyonu onerisi
- A/B test varyantlari

## Escalation
- Icerik kaynagi gerekirse → H8 (Content Repurposer)
- Gonderim altyapisi → L1 (Notification Agent)
