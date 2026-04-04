---
id: B8
name: Refactor Agent
category: backend
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [github, git, jcodemunch]
capabilities: [refactoring, dead-code, simplification]
max_tool_calls: 25
effort: medium
template: code
related: [B1, C3]
status: pool
---

# B8: Refactor Agent

## Amac
Kod sadelestirme, dead code temizleme, pattern iyilestirme.

## Kapsam
- Dead code tespit ve temizleme
- Kod tekrari azaltma (DRY)
- Fonksiyon/sinif sadelestirme
- Design pattern uygulama
- Dosya/modul yeniden yapilandirma

## Escalation
- Mimari degisiklik gerekirse → B1 (Backend Architect)
- Review gerekirse → C3 (Local AI Reviewer)
