---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Attribution Models

## Quick Reference

**Attribution** assigns credit for conversions to touchpoints (ads, organic, email).

- **GA4 defaults:** Data-driven (when eligible), last click non-direct, paid organic last click—varies by report and Ads linking.
- **Lookback window:** 30 vs 90 days changes credit for long B2B cycles.
- **Bridge to M3:** Experiments measure *incrementality* on randomized slices—do not confuse with platform attribution.
- **Bridge to M2:** **M2** UTM discipline on LPs (`utm_source`, `utm_medium`, `utm_campaign`) feeds clean channel reports.

| Model | Behavior | Bias |
|-------|----------|------|
| Last click | 100% to last touch | Undervalues awareness |
| First click | 100% to first | Undervalues closing channels |
| Linear | Equal split | Ignores impact differences |
| Data-driven / Markov | Learned from paths | Needs volume, black box |

## Patterns & Decision Matrix

| Question | Approach |
|----------|----------|
| Budget allocation | MMM + platform ROAS + incrementality tests |
| Creative performance | Ad platform + UTMs |
| Content ROI | Assisted conversions + path length |

**B2B vs B2C**

| | B2B | B2C |
|---|-----|-----|
| Cycle | Long, many touches | Short, fewer |
| Identity | CRM is source of truth | Often anonymous |

## Code Examples

**1) UTM standard**

```
https://example.com/lp/ap?utm_source=linkedin&utm_medium=paid_social&utm_campaign=q2_finance&utm_content=carousel_a
```

**2) BigQuery path sketch (GA4 export concept)**

```sql
-- Pseudocode: sessions with campaign grouped per user
SELECT user_pseudo_id, ARRAY_AGG(campaign ORDER BY event_timestamp) AS path
FROM `project.analytics_events_*`
GROUP BY user_pseudo_id;
```

## Anti-Patterns

- **Single source of truth** from ad platform alone—double-counts vs analytics.
- **Changing UTMs** mid-quarter—breaks continuity.
- **Ignoring dark social**—complement with surveys and branded search.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [GA4 — Attribution settings](https://support.google.com/analytics/answer/10596866) — reporting attribution
- [Google Ads — Attribution models](https://support.google.com/google-ads/answer/6259715) — ads-specific
- [IAB — MMT guidance](https://www.iab.com/) — marketing mix modeling industry context
- [Think with Google — Measurement](https://www.thinkwithgoogle.com/intl/en-emea/future-of-marketing/measurement/) — strategic framing
