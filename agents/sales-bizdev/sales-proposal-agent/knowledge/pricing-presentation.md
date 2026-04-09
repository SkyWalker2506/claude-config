---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Pricing Presentation

## Quick Reference

**Proposal-facing pricing** = transparent line items + one total + terms. **Never** bury material limits in footnotes without a summary box.

| Element | Buyer need |
|---------|------------|
| Line items | What they pay for (SKU/phase) |
| Unit | Seat, month, project, TB |
| Quantity | Volume, duration |
| Subtotal | Before tax/discount |
| Discounts | Named (e.g. annual prepay) with expiry |
| Total | Currency, tax note, validity date |

**Sync with O4:** All numbers originate from `pricing-calculator` models; proposal only presents approved scenarios.

## Patterns & Decision Matrix

| Scenario | Presentation |
|----------|----------------|
| Good/Better/Best | Comparison table + recommended column |
| Consumption / usage | Tier table + overage row |
| T&M + cap | Rate card + not-to-exceed + change order rule |
| Fixed fee milestone | % at signature, UAT, go-live |

## Code Examples

**Markdown table for proposal body:**

```markdown
| Package | Includes | Monthly (USD) | Annual (USD) |
|---------|----------|---------------|--------------|
| Core | Up to 25 users, standard SLA | 2,400 | 24,000 |
| Plus | 100 users, premium SLA, SSO | 4,900 | 49,000 |

*Annual prepay: 15% discount through {{date}}. Prices exclude VAT.*
```

**Simple ROI bridge (align with value narrative):**

```text
Baseline cost today: {{annual}} (labor + tools)
Projected Year-1 with {{Product}}: {{annual_new}}
Payback: {{months}} months (per O4 model v{{version}})
```

**Footnote discipline (appendix-safe):**

```markdown
^1 Assumes client provides UAT environment by {{date}}.
^2 Overage: $0.12 per API call above 5M/month.
```

## Anti-Patterns

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Price without validity | Stale quotes | “Valid 30 days from {{date}}” |
| Mixing net and gross | Accounting disputes | One tax treatment per table |
| “Contact us” for core SKU | Friction | At least list list price or range |

## Deep Dive Sources

- [HubSpot — how to present pricing](https://www.hubspot.com/sales/pricing-strategy) — packaging narrative
- [McKinsey — pricing strategy fundamentals](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/how-we-help-clients/pricing) — value communication
- [Gartner — technology contract negotiation](https://www.gartner.com/) — enterprise buyer expectations
- [IFRS 15 / ASC 606 overview](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/) — revenue recognition awareness for complex deals
