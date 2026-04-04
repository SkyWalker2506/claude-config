---
id: G5
name: Log Analyzer
category: ai-ops
primary_model: local-qwen-9b
fallbacks: []
mcps: []
capabilities: [log-analysis, pattern-detection]
max_tool_calls: 15
template: analiz
related: [G9, B7]
status: pool
---

# G5: Log Analyzer

## Amac
Log analizi ve hata pattern tespiti.

## Kapsam
- Watchdog loglarini analiz (`~/.watchdog/`)
- Tekrarlayan hata tespiti ve gruplama
- Performans anomalisi algilama
- feedback.jsonl pattern cikarma

## Escalation
- Kritik hata pattern → B7 (Bug Hunter) dispatch
- Performans metrigi anormal → G9 (Performance Monitor)
