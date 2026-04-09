---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# GA4 Setup Guide

## Quick Reference

- **Data model:** Events + parameters + user properties—not pageviews-only (though `page_view` is an event).
- **Streams:** Web + iOS + Android per property; use one **Measurement ID** (`G-XXXX`) per site/app pair.
- **Bridge to M3:** Register `experiment_id` / `variant_id` as **event-scoped** or **user-scoped** custom dimensions (Admin → Custom definitions) for **M3** reporting.
- **Bridge to M1:** `tool_*` events from **M1** map to GA4 recommended events where possible (`generate_lead`, `sign_up`) or custom names with a naming convention doc.

| Task | Where |
|------|-------|
| Mark conversions | Admin → Events → Mark as conversion |
| Exclude internal IP | Data streams → Configure tag settings |
| BigQuery export | Admin → BigQuery links (360 or eligible) |

## Patterns & Decision Matrix

| Need | GA4 feature |
|------|-------------|
| Funnel with drop-off | Explorations → Funnel |
| Cohort retention | Explorations → Cohort |
| Raw SQL | BigQuery export |
| Ads ROI | Link Google Ads + import conversions |

**Event naming**

| Style | Example |
|-------|---------|
| snake_case | `trial_start` |
| Consistent entity | `tool_open`, `tool_submit` |

## Code Examples

**1) gtag recommended event**

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXX');
  gtag('event', 'sign_up', { method: 'google' });
</script>
```

**2) GTM dataLayer push (common pattern)**

```javascript
dataLayer.push({
  event: 'trial_start',
  plan_tier: 'pro',
  experiment_id: 'EXP-2026-041',
  variant_id: 'b'
});
```

## Anti-Patterns

- **PII in parameters** (email, name)—violates GA terms; hash or omit.
- **Duplicate page_view** from double tags—inflate sessions.
- **Changing event names** monthly—breaks YoY reports.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [GA4 — Set up Analytics](https://support.google.com/analytics/answer/9304153) — official setup
- [GA4 — Recommended events](https://support.google.com/analytics/answer/9267735) — naming alignment
- [GA4 — BigQuery export](https://support.google.com/analytics/answer/9358801) — schema
- [Google Tag Manager — Web container](https://developers.google.com/tag-platform/tag-manager) — deployment layer
