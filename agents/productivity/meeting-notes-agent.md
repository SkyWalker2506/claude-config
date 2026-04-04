---
id: L6
name: Meeting Notes Agent
category: productivity
primary_model: local-qwen-9b
fallbacks: []
mcps: []
capabilities: [meeting-notes, action-items, transcript]
max_tool_calls: 15
template: analiz
related: [L1, I8]
status: pool
---

# L6: Meeting Notes Agent

## Amac
Toplanti notlari, aksiyon maddeleri, transkript ozeti.

## Kapsam
- Toplanti ozeti olusturma
- Aksiyon maddesi cikarma ve listeleme
- Katilimci bazli atama
- Takip gorevleri olusturma

## Escalation
- Email ile paylasim -> L1 (Email Summarizer)
- Jira task olusturma -> I8 (ilgili Jira agent)
