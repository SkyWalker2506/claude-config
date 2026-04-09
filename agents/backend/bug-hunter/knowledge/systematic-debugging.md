---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Systematic Debugging

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Reproduce — minimal, deterministic |
| 2 | Hypothesis — what could cause this |
| 3 | Instrument — logs, breakpoints, trace id |
| 4 | Binary search — bisect versions/commits |
| 5 | Fix + regression test |

**Divide and conquer:** Isolate layer (client, API, DB, queue).

**2025–2026:** OpenTelemetry trace id across services; feature flags for safe reproduction.

## Patterns & Decision Matrix

| Symptom | First check |
|---------|-------------|
| Intermittent | Race, timeout, resource exhaustion |
| After deploy | Diff, migration, config |
| Only prod | Data shape, load, feature flag |

## Code Examples

```text
trace_id=abc → logs: gateway → service-a → db
Compare spans: latency jump at hop 2
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| Random changes | One hypothesis per experiment |
| No repro | Staging fixture |

## Deep Dive Sources

- [David Agans — Debugging](https://www.amazon.com/Debugging-Indispensable-Software-Hardware-Problems/dp/0814474578)
- [OpenTelemetry — Tracing](https://opentelemetry.io/docs/concepts/signals/traces/)
