---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# A/B Testing on Landing Pages

## Quick Reference

- **One primary metric per test:** e.g. `signup_submit` or `trial_start`—align with **M4 Analytics Agent** event name.
- **Isolation:** Change one *layer* per experiment when possible (headline OR image, not both) unless factorial design is intentional.
- **Stable URLs:** Same LP URL + server-side or client-side assignment—avoid `/page-a` vs `/page-b` for SEO dilution unless `canonical` set.
- **Bridge to M3:** **M3 A/B Test Agent** owns power analysis, stopping rules, and doc—M2 supplies DOM `data-variant` hooks and copy tables.
- **Bridge to M1:** If test includes embedded tool, **M1** freezes `logic_version` for duration.

| Test type | Tooling examples | Notes |
|-----------|------------------|-------|
| Visual editor | Optimizely, VWO, Google Optimize successors | Fast; watch flicker |
| Feature flag | LaunchDarkly, Split | Good for SPA |
| Redirect | CDN split | SEO care |

## Patterns & Decision Matrix

| When to test | When to wait |
|--------------|--------------|
| High traffic, low conversion | <5k weekly visitors—may need sequential or multi-week |
| Clear hypothesis | “Try stuff” without model |
| Instrumentation ready | Events missing in GA4/Mixpanel |

**What to test first (typical ROI)**

| Area | Impact |
|------|--------|
| H1 + subhead | High |
| CTA label + placement | High |
| Hero creative | Medium–high |
| Footer color | Low |

## Code Examples

**1) data-* contract for M3/M4**

```html
<section id="hero" data-exp="hero_q2_2026" data-variant="b">
  <h1 data-copy-id="hero_h1">…</h1>
  <button data-cta-id="primary" type="submit">…</button>
</section>
```

**2) GA4 experiment dimensions (conceptual)**

```javascript
gtag('event', 'page_exposure', {
  experiment_id: 'hero_q2_2026',
  variant_id: 'b',
  page_location: location.href
});
gtag('event', 'sign_up', { method: 'email' }); // primary metric
```

## Anti-Patterns

- **Peeking** at results daily and stopping early—inflate false positives (M3 mitigates).
- **Novelty effect:** Big change wins week one, reverts—run full calendar cycles.
- **Mismatch** between visual winner and revenue—guardrail metrics in M3 doc.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google — Tag Assistant / GA4 DebugView](https://support.google.com/analytics/answer/7201382) — validate events
- [Optimizely — Experiment design](https://docs.developers.optimizely.com/) — platform patterns
- [Evan Miller — Sample size](https://www.evanmiller.org/ab-testing/sample-size.html) — quick calculator reference
- [Microsoft ExP platform — ethics](https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/) — trustworthy experimentation culture
