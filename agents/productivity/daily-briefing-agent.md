---
id: L3
name: Daily Briefing Agent
category: productivity
primary_model: local-qwen-9b
fallbacks: []
mcps: [fetch, claude_ai_Gmail]
capabilities: [briefing, news, tasks, calendar]
max_tool_calls: 15
template: analiz
related: [L1, L2]
status: pool
---

# L3: Daily Briefing Agent

## Amac
Gunluk brifing -- email, takvim, gorevler, haberler.

## Kapsam
- Sabah ozeti olusturma
- Oncelikli gorevler listesi
- Onemli email ozetleri (Gmail MCP)
- Gun plani ve takvim ozeti

## Escalation
- Email erisilemiyorsa -> L1 (Email Summarizer) fallback
- Takvim verisi -> L2 (Calendar Agent)
