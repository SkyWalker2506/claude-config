---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Event Tracking Design

## Quick Reference

**Taxonomy:** `{object}_{action}` e.g. `subscription_started`, `invoice_paid`.

- **Event:** Verb phrase; **properties:** nouns with context (`amount`, `currency`, `experiment_id`).
- **Required vs optional:** Schema doc lists required params per environment (staging blocks if missing).
- **Bridge to M1:** **M1** tools emit `tool_*` events—same schema in GA4 and Mixpanel via GTM/server.
- **Bridge to M3:** `exp_exposure` must precede outcome events in logical time for **M3** causal reads.

| Property type | Storage |
|---------------|---------|
| High cardinality IDs | Event param |
| User segment | User property (updated) |
| Experiment | Event param on all in-session events |

## Patterns & Decision Matrix

| Problem | Pattern |
|---------|---------|
| Duplicate purchase | `transaction_id` dedupe |
| Anonymous browsing | anonymous id until login |
| Offline conversions | Server-side upload / sGTM |

**Server vs client**

| Client | Server |
|--------|--------|
| Fast to ship | Trustworthy for revenue |
| Ad blockers | No DOM |

## Code Examples

**1) Event schema (YAML)**

```yaml
events:
  trial_start:
    description: User completes signup for trial
    required: [plan_tier, experiment_id, variant_id]
    optional: [utm_source, referrer]
  tool_submit:
    description: Lead-gen tool calculation submitted
    required: [tool_id, logic_version]
```

**2) Stape / sGTM purchase (concept)**

```json
{
  "event_name": "purchase",
  "client_id": "abc123",
  "transaction_id": "ord_9981",
  "value": 120.0,
  "currency": "USD"
}
```

## Anti-Patterns

- **God event** with 40 parameters—split lifecycle.
- **Boolean soup** (`is_test`, `is_fake`)—use environment separation.
- **No versioning** on breaking changes—use `schema_version` param.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [GA4 — Event parameters](https://support.google.com/analytics/answer/9267737) — limits and scope
- [Segment — Spec](https://segment.com/docs/connections/spec/) — industry event taxonomy reference
- [Snowplow — Event modeling](https://docs.snowplow.io/docs/) — rigorous analytics engineering
- [Avo — Tracking plan](https://www.avo.app/) — governance tooling (concept reference)
