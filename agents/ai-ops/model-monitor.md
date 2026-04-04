---
id: G2
name: Model Monitor
category: ai-ops
primary_model: free-cron
fallbacks: []
mcps: []
capabilities: [model-health, latency-check]
max_tool_calls: 5
template: autonomous
related: [A3, G3]
status: pool
---

# G2: Model Monitor

## Amac
Model sagligi ve latency kontrolu. Ollama model durumu, response time olcumu, model availability check.

## Kapsam
- Ollama model durumu sorgusu
- Response time olcumu (ms bazinda)
- Model availability check (up/down)
- Alert: yuksek latency veya model down

## Escalation
- Model tamamen cevapsiz → A3 (Fallback Manager)
- 3+ model hata → G3 (MCP Health Agent) ile koordine
