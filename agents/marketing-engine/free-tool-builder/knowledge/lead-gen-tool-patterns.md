---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Lead-Gen Tool Patterns

## Quick Reference

| Pattern | Best for | Primary conversion |
|---------|----------|-------------------|
| **Calculator** | SaaS pricing, ROI, savings | Email gate after result OR soft gate |
| **Grader / audit** | SEO, performance, maturity | Score + PDF lead magnet |
| **Interactive quiz** | Persona, fit, assessment | Segmented nurture |
| **Template / generator** | Copy, code snippet, checklist | Sign-up to save |

- **One job:** Tool solves one measurable pain; avoid Swiss-army UX.
- **Time-to-value:** User sees *something* useful in < 30s before heavy form friction.
- **Bridge to M2:** Output blocks (embed URL, headline, CTA) must match landing sections the **M2 Landing Page Agent** owns—coordinate UTM and hero copy.
- **Bridge to M4:** Fire `tool_open`, `calc_submit`, `lead_submit` events for **M4 Analytics Agent** funnel steps (names mirror GA4/Mixpanel conventions).

| Stage | User sees | You measure |
|-------|-----------|-------------|
| Land | Problem + CTA to start | `tool_open` |
| Input | Minimal fields | `step_complete` |
| Result | Shareable outcome | `result_view` |
| Gate | Email / book demo | `lead_submit` |

## Patterns & Decision Matrix

| When | Pattern | Trade-off |
|------|---------|-----------|
| B2B, long sales cycle | Grader + report | Higher build cost; strong SQL quality |
| PLG / self-serve | Calculator + compare tiers | Needs accurate pricing logic |
| Content / top of funnel | Quiz + segment | Nurture complexity |
| Dev audience | CLI-style or API preview | Low fluff; must be technically honest |

**Gating decision**

| Gate type | Conversion | Lead quality | Use when |
|-----------|------------|--------------|----------|
| None | High traffic, low intent | Variable | Awareness campaigns |
| Soft (email for PDF/save) | Balanced | Good default | Most B2B tools |
| Hard (email before result) | Lower volume | Higher intent | Premium audits |

## Code Examples

**1) Event contract (GTM dataLayer + GA4)—align with M4 naming**

```html
<script>
window.dataLayer = window.dataLayer || [];
function pushToolEvent(name, params) {
  dataLayer.push({
    event: name,
    tool_id: 'roi-calculator-v2',
    ...params
  });
}
pushToolEvent('tool_open', { surface: 'embed', referrer: document.referrer });
pushToolEvent('calc_submit', { inputs_hash: 'v1', step: 3 });
pushToolEvent('lead_submit', { method: 'email', variant: 'soft_gate' });
</script>
```

**2) Minimal tool spec (YAML) for handoff to M2**

```yaml
tool:
  id: roi-calculator-v2
  primary_job: "Estimate annual savings vs status quo"
  inputs:
    - { id: seats, type: int, min: 1, max: 10000 }
    - { id: arpu, type: currency, currency: USD }
  outputs:
    - { id: annual_savings, format: currency }
  lead_gate:
    type: soft
    trigger: after_result
    offer: "Email PDF breakdown"
  embed_paths:
    - /tools/roi-calculator
    - landing_section: hero_cta_secondary
```

## Anti-Patterns

- **Fake precision:** Showing 7 decimal places on estimates—erodes trust; round sensibly.
- **Bait-and-switch:** Hiding that results require sales call—spikes bounce and hurts brand.
- **Unbounded inputs:** Free-text that breaks logic—use constrained fields and validation.
- **Orphan tool:** No UTM discipline, no events—**M4** cannot attribute; **M2** cannot reuse blocks.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Tag Manager — data layer](https://developers.google.com/tag-platform/tag-manager/datalayer) — event structure for GA4
- [HubSpot — Lead generation tools](https://www.hubspot.com/lead-generation) — playbook framing (2025–2026 positioning)
- [CXL — Interactive content](https://cxl.com/blog/) — conversion-focused tool UX research
- [Refactoring UI — hierarchy and density](https://www.refactoringui.com/) — layout for result screens
