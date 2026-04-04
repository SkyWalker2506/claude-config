---
id: A3
name: Fallback Manager
category: orchestrator
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [model-switching, health-check]
max_tool_calls: 5
template: autonomous
related: [A2, A4]
status: active
---

# A3: Fallback Manager

## Amac
Model unavailable, timeout veya low-quality durumunda conditional fallback zincirini uygular.

## Kapsam
- Hata turune gore farkli fallback yolu (error/timeout/rate-limit/low-quality)
- Fallback latency logging (~/.watchdog/fallback_latency.jsonl)
- Tum zincir tukenirse alert tetikleme

## Escalation
- on_all_fail → terminal alert + A8 (Manual Control)
