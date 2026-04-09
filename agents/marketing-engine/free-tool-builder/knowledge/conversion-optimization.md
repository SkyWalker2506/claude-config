---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Conversion Optimization (Lead-Gen Tools)

## Quick Reference

**North star:** Qualified leads per thousand visits (or activated trials), not raw form fills.

- **Micro-conversions:** `start`, `step_complete`, `result_view` predict `lead_submit`—use for diagnostics when primary CVR drops.
- **Friction vs clarity:** Each extra field needs explicit value ("Why we ask").
- **Bridge to M3:** Primary CTA copy and gate timing are classic **M3 A/B Test Agent** targets—freeze `tool_id` + `logic_version` when reading experiment results.
- **Bridge to M4:** Define funnel steps in **M4 Analytics Agent** as ordered events; segment by `utm_*` and `device_category`.

| Lever | Typical lift band | Effort |
|-------|---------------------|--------|
| Headline clarity | 5–20% | Low |
| Gate after value | 10–40% | Medium |
| Social proof near form | 5–15% | Low |
| Performance (LCP) | 5–25% | Medium |

## Patterns & Decision Matrix

| Hypothesis | Experiment | Guardrail metric |
|------------|------------|------------------|
| Users fear email spam | Gate copy + privacy link | Bounce on form |
| Result not compelling | Add benchmark comparison | Time on result |
| Mobile drop-off | Fewer fields on small screens | Step completion rate |

**Segmentation before aggregate winner**

| Segment | Why split |
|---------|-----------|
| Paid vs organic | Intent differs |
| New vs returning | Familiarity with brand |
| Geo / currency | Price sensitivity |

## Code Examples

**1) Experiment assignment hook (pseudo)—hand off to M3/M4**

```javascript
const variant = window.__EXP_VARIANT__ || 'control'; // set by edge or feature flag
gtag('event', 'tool_exposure', {
  experiment_id: 'gate_timing_2026q2',
  variant,
  tool_id: 'roi-calculator-v2'
});
```

**2) Form field JSON with conversion rationale**

```json
{
  "fields": [
    { "id": "work_email", "required": true, "helper": "We send the PDF here—no spam." },
    { "id": "company_size", "required": false, "routing": "sales_qualified" }
  ],
  "primary_cta": { "label": "Email me the report", "test_id": "cta_soft_gate_v2" }
}
```

## Anti-Patterns

- **Winner on clicks only** without downstream SQL/win rate—optimizes the wrong funnel.
- **Changing tool logic mid-test**—confounds **M3** results.
- **Ignoring sample ratio mismatch** between variants—see M3 statistical docs.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Analytics 4 — Funnel exploration](https://support.google.com/analytics/answer/9327974) — funnel analysis
- [Optimizely — Stats engine overview](https://docs.developers.optimizely.com/experimentation/v4.0.0-full-stack/docs/stats-engine) — sequential testing concepts
- [CXL — Form optimization](https://cxl.com/blog/) — field-level tests
- [Nielsen Norman Group — Form design](https://www.nngroup.com/topic/forms/) — usability baseline
