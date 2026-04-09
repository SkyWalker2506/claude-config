---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Variant Design

## Quick Reference

- **Variant = one coherent change set** tied to a hypothesis—not random pixel tweaks unless exploratory.
- **Naming:** `control`, `treatment_headline_v2`, `treatment_social_proof`—stable IDs in code and analytics.
- **Parity:** Same tracking, same legal disclaimers, same product behind CTA—only the test lever differs.
- **Bridge to M2:** **M2 Landing Page Agent** delivers Figma/HTML per variant with `data-copy-id` alignment to experiment sheet.
- **Bridge to M1:** Tool embed tests require **M1** to expose feature flags or query `?variant=` for iframe consumers.

| Layer | Examples |
|-------|----------|
| Copy | H1, CTA, form labels |
| Layout | Column order, form position |
| Creative | Image, video thumbnail |
| Offer | Trial length, bonus module |

## Patterns & Decision Matrix

| Hypothesis class | Design tip |
|------------------|------------|
| Motivation | Reframe outcome in H1 |
| Friction | Remove fields / add progress |
| Anxiety | Add security / refund near CTA |
| Value clarity | Comparison table, ROI |

**Multivariate vs A/B**

| Approach | When |
|----------|------|
| Classic A/B | Learning speed priority |
| MVT | Enough traffic + factorial interest |
| Bandits | Continuous optimization, not one-shot read |

## Code Examples

**1) Variant spec JSON**

```json
{
  "experiment_id": "EXP-2026-041",
  "variants": {
    "control": { "hero_h1": "Automate AP in Slack", "cta": "Start trial" },
    "b": { "hero_h1": "Close books 3× faster", "cta": "Try free for 14 days" }
  },
  "frozen": { "pricing": "2026-q1-list", "m1_tool_version": "roi-calculator-v2" }
}
```

**2) CSS isolation per variant**

```html
<body class="exp-041" data-variant="b">
  <!-- variant-specific theme tokens -->
</body>
```

## Anti-Patterns

- **Confounded changes:** New headline + new pricing in same cell.
- **Invisible variants:** Same pixels, different only in dev tools—debug nightmare.
- **Accessibility regression** in winning variant—ship blocker.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Baymard — UX benchmarks](https://baymard.com/) — evidence-backed patterns
- [GOV.UK Design System](https://design-system.service.gov.uk/) — component discipline
- [W3C — Accessibility](https://www.w3.org/WAI/standards-guidelines/wcag/) — variant QA checklist
- [CXL — Testing ideas](https://cxl.com/blog/) — hypothesis backlog inspiration
