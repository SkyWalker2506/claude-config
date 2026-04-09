---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Load Testing Methodology

## Quick Reference

| Tool | Type |
|------|------|
| **k6** | Scriptable, JS |
| **Locust** | Python |
| **JMeter** | GUI + CLI |
| **Gatling** | Scala DSL |

**Steps:** Baseline → ramp → soak → stress. Define **SLO** (e.g. p95 < 300ms).

**2025–2026:** Run against staging with prod-like data volume; never DDoS production without approval.

## Patterns & Decision Matrix

| Goal | Test |
|------|------|
| Capacity | Find breaking point in staging |
| Regression | Same script each release |

## Code Examples

```javascript
import http from 'k6/http';
export default function () { http.get('https://staging.example.com/health'); }
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| No think time | Unrealistic RPS |

## Deep Dive Sources

- [k6 — Documentation](https://k6.io/docs/)
- [Google SRE — Load testing](https://sre.google/sre-book/load-testing/)
