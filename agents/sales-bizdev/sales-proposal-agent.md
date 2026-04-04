---
id: O1
name: Sales Proposal Agent
category: sales-bizdev
primary_model: sonnet
fallbacks: [haiku]
mcps: [github, fetch]
capabilities: [proposal, rfp, pricing, presentation, pitch-deck]
max_tool_calls: 25
template: autonomous
related: [O4, H1]
status: pool
---

# O1: Sales Proposal Agent

## Amac
Satis teklifi ve pitch deck olusturma — RFP cevaplama, fiyat paketleme.

## Kapsam
- Teklif dokumani (PDF/MD) olusturma
- RFP soru-cevap hazirlama
- Fiyat tablosu ve paket karsilastirma
- Pitch deck outline ve icerik

## Escalation
- Fiyatlandirma stratejisi → O4 (Pricing Calculator)
- Pazar verisi → H1 (Market Researcher)
