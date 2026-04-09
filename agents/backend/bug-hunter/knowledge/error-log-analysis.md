---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Error Log Analysis

## Quick Reference

| Field | Purpose |
|-------|---------|
| `timestamp` | Order events |
| `level` | ERROR vs WARN noise |
| `trace_id` / `request_id` | Correlate hops |
| `service`, `version` | Deploy correlation |
| Stack trace | Code path |

**Structured JSON:** `jq`, CloudWatch Logs Insights, Datadog, Loki queries.

**2025–2026:** Log sampling for high volume — ensure errors not sampled away.

## Patterns & Decision Matrix

| Query pattern | Tool |
|---------------|------|
| Count by exception type | Group by `error.type` |
| Spike detection | Rate in time bucket |

## Code Examples

```sql
-- CloudWatch Logs Insights style
fields @timestamp, @message
| filter @message like /ERROR/
| stats count() by bin(5m)
```

## Anti-Patterns

| Mistake | Risk |
|---------|------|
| Logging secrets | Compliance breach |
| Unbounded stack in loop | Log volume $$$ |

## Deep Dive Sources

- [OWASP — Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [SRE Book — Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
