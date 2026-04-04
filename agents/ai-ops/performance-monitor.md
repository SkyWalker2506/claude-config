---
id: G9
name: Performance Monitor
category: ai-ops
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [token-tracking, response-time]
max_tool_calls: 5
template: autonomous
related: [A4, G2]
status: pool
---

# G9: Performance Monitor

## Amac
Token kullanimi ve response time takibi.

## Kapsam
- Gunluk token raporu (model bazli)
- Model bazli maliyet hesaplama
- Agent performans metrigi (tool call/basari orani)
- Response time trend analizi

## Escalation
- Token limiti yaklasirsa → A4 (Token Budget Manager) alert
- Performans dususu → G2 (Model Monitor) ile koordine
