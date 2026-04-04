---
id: C6
name: Human Review Coordinator
category: code-review
primary_model: haiku
fallbacks: []
mcps: [github]
capabilities: [review-routing, human-handoff]
max_tool_calls: 5
effort: low
template: code-review
layer: L4
related: [C3, C5]
status: pool
---

# C6: Human Review Coordinator

## Amac
Human review atama ve takip.

## Kapsam
- Uygun reviewer belirleme ve atama
- Review durumu takip
- Review hatirlatma ve eskalasyon
- Review sonuclarini toplama
- Approval/rejection akisi yonetimi

## Escalation
- AI review yeterliyse → C3 (Local AI Reviewer)
- CI review katmani ile koordinasyon → C5 (CI Review Agent)
