---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Mixpanel Patterns

## Quick Reference

- **Identity merge:** `distinct_id` + `$identify` to stitch anonymous → authenticated—critical for B2B funnels.
- **Super properties:** Persist across events (plan tier)—use sparingly; prefer group profiles for B2B accounts.
- **Bridge to M3:** Cohort of users in experiment via `experiment_id` property—compare conversion in Insights.
- **Bridge to M2:** Page or `utm` properties on `Page View` or custom `lp_view`—tie **M2** campaigns to downstream events.

| Object | Mixpanel concept |
|--------|------------------|
| User | Profile |
| Company | Group (if enabled) |
| Funnel step | Event sequence |

## Patterns & Decision Matrix

| Analysis | Mixpanel tool |
|----------|----------------|
| Funnel time-to-convert | Funnels with conversion window |
| Retention of activated users | Retention report |
| Feature adoption | Insights + breakdown by `feature_name` |

**Implementation choice**

| SDK | When |
|-----|------|
| Browser JS | Marketing site |
| Server | Authoritative revenue |
| Mobile | Native apps |

## Code Examples

**1) track + people set (browser, conceptual)**

```javascript
mixpanel.track('Trial Started', {
  plan: 'pro',
  experiment_id: 'EXP-2026-041',
  variant_id: 'b'
});
mixpanel.identify(user.id);
mixpanel.people.set({ $email: user.email, plan: 'pro' });
```

**2) Group analytics (B2B)**

```javascript
mixpanel.set_group('company', 'acme_inc');
mixpanel.get_group('company', 'acme_inc').set('employee_count', 500);
```

## Anti-Patterns

- **Tracking without identify**—double counts users across devices incorrectly.
- **High-cardinality properties** on every event—slow queries, cost.
- **Mismatch** with GA4 event names—document mapping table.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Mixpanel — JavaScript SDK](https://developer.mixpanel.com/docs/javascript) — implementation
- [Mixpanel — Identity management](https://developer.mixpanel.com/docs/identifying-users) — merge rules
- [Mixpanel — Group Analytics](https://developer.mixpanel.com/docs/group-analytics) — B2B
- [Mixpanel — Lexicon](https://help.mixpanel.com/hc/en-us/articles/360001307806) — data governance
