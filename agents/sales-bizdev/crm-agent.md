---
id: O2
name: CRM Agent
category: sales-bizdev
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [fetch]
capabilities: [hubspot, pipedrive, lead-management, pipeline, follow-up]
max_tool_calls: 15
template: autonomous
related: [O1, O3]
status: pool
---

# O2: CRM Agent

## Amac
CRM veri yonetimi — lead takip, pipeline, follow-up hatirlatma.

## Kapsam
- Lead kayit ve siniflandirma
- Pipeline durum takibi
- Follow-up email taslaklari
- Musteri aktivite ozeti

## Escalation
- Satis teklifi → O1 (Sales Proposal)
- Outreach → O3 (Outreach Agent)
