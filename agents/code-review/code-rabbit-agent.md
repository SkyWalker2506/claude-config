---
id: C4
name: Code Rabbit Agent
category: code-review
primary_model: free-coderabbit
fallbacks: []
mcps: []
capabilities: [deep-review, coderabbit]
max_tool_calls: 5
effort: medium
template: code-review
layer: L2
related: [C3, C5]
status: pool
---

# C4: Code Rabbit Agent

## Amac
CodeRabbit CLI ile derin kod incelemesi.

## Kapsam
- CodeRabbit CLI calistirma ve sonuc yorumlama
- Derin statik analiz
- Kod kalitesi ve guvenlik onerileri
- PR bazli otomatik review
- Review bulgularini raporlama

## Escalation
- Ek manual review gerekirse → C3 (Local AI Reviewer)
- CI review katmani gerekirse → C5 (CI Review Agent)
