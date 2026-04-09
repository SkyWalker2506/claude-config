---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Conversion Copywriting

## Quick Reference

**H1 formula (pick one angle):**

- **Outcome:** `{Outcome} for {who} without {pain}`
- **Contrast:** `{Old way} vs {new way}`
- **Proof-led:** `{Metric} teams use {product} to {job}`

- **Subhead:** Expands *how* or *for whom*—never repeats H1 with synonyms only.
- **CTA verbs:** Specific (`Start 14-day trial`) beats vague (`Get started`).
- **Bridge to M1:** If hero references a calculator, repeat the *same numbers/claims* the tool can substantiate—**M1** owns formula truth.
- **Bridge to M3:** Every testable line gets a `copy_id` for **M3** variant tables (e.g. `hero_h1_a`, `hero_h1_b`).

| Element | Length guide |
|---------|----------------|
| H1 | ~6–12 words |
| Subhead | 1–2 lines |
| CTA | 2–5 words + risk reducer (`No credit card`) |

## Patterns & Decision Matrix

| Audience awareness | Lead with |
|---------------------|-----------|
| Unaware | Problem story |
| Problem-aware | Agitate + mechanism hint |
| Solution-aware | Differentiation |
| Product-aware | Offer + proof |

**Objection handling placement**

| Objection | Where to address |
|-----------|------------------|
| Price | Value stack + comparison |
| Security | Near form + FAQ |
| Effort | “Setup in 10 minutes” near CTA |

## Code Examples

**1) Variant table for M3 handoff**

```markdown
| copy_id | location | control | B |
|---------|----------|---------|---|
| hero_h1 | H1 | Cut AP time 40% | Close books 3× faster |
| cta_primary | Hero button | Start free trial | Try free for 14 days |
```

**2) Microcopy block (JSON for CMS)**

```json
{
  "hero": {
    "h1": "Automate vendor invoices in Slack",
    "sub": "Finance teams at Series B+ replace email threads with one inbox.",
    "cta": { "primary": "Book a 20-min walkthrough", "risk": "See a live sandbox" }
  }
}
```

## Anti-Patterns

- **Superlatives** without proof (“#1”, “best”)—regulatory risk and trust loss.
- **Passive voice** in CTAs (“Your trial can be started”).
- **Jargon stack** (“AI-powered synergistic orchestration”) with no plain explanation.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Apple Style Guide — clarity](https://support.apple.com/guide/applestyleguide/welcome/web) — concise corporate tone reference
- [GOV.UK — Content design](https://www.gov.uk/guidance/content-design) — plain language discipline
- [Copyhackers — Research](https://copyhackers.com/) — voice-of-customer methods
- [FTC — Endorsement guides](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) — claims and testimonials
