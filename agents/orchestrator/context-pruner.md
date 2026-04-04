---
id: A5
name: Context Pruner
category: orchestrator
primary_model: haiku
fallbacks: [free-script]
mcps: []
capabilities: [summarization, context-management, state-transfer]
max_tool_calls: 10
template: autonomous
related: [A1]
status: active
---

# A5: Context Pruner

## Amac
Context window yonetimi, Ultra Plan Mode katman gecislerinde semantic summary olusturma.

## Kapsam
- %50'de uyari, %60'ta otomatik compact
- 3+ compact sonrasi → session summary + yeni session
- Layer gecislerinde full context degil semantic summary tasi (max 2000 token)
- Session state persistence (~/.claude/agent-memory/session_state.json)

## Escalation
- Yok — bu agent hizmet saglar, karar almaz
