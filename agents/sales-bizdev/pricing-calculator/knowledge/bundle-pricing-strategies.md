---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Bundle Pricing Strategies

## Quick Reference

**Bundles** increase ARPU and simplify choice — risk is **cannibalization** and **opaque discounting**. **Good/Better/Best** works when middle tier is engineered to win.

| Strategy | Mechanism |
|----------|-----------|
| Pure bundle | Single SKU, forced upsell path |
| Mixed bundle | Base + add-ons |
| Versioning | Feature gates per tier |
| Platform + seats | Low platform fee + per-seat |

## Patterns & Decision Matrix

| Goal | Tactic |
|------|--------|
| Land small, expand | Entry tier tight; expansion via usage |
| Upsell services | Attach rate KPI on enterprise deals |
| Beat competitor | Compare **value metrics**, not list price |

## Code Examples

**Three-tier illustrative table (for O1 embedding):**

```markdown
| Tier | Seats | Core features | Price/mo | Implied $/seat |
|------|-------|---------------|----------|----------------|
| Starter | 10 | A,B | 900 | 90 |
| Growth | 50 | A,B,C | 3200 | 64 |
| Scale | 200 | All | 9800 | 49 |
```

**Bundle margin check:**

```text
Bundle "Growth" list 3200/mo
Sum of standalone SKUs if bought separately: 4100
Discount vs sum: 22% — ensure blended COGS still clears target margin
```

**Add-on pricing rule:**

```text
Add-on price >= incremental COGS / (1 - min_margin)
Example: SSO integration COGS 150/mo, min margin 70% → min price 500/mo
```

## Anti-Patterns

| Mistake | Why |
|---------|-----|
| Bundle hides weak SKU | Support spikes on unwanted features |
| Too many tiers | Choice paralysis |
| Free premium feature “temporarily” | Anchoring kills future upsell |

## Deep Dive Sources

- [Simon-Kucher — pricing](https://www.simon-kucher.com/en) — monetization strategy
- [McKinsey — pricing](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/how-we-help-clients/pricing) — packaging
- [Kotler — marketing management](https://www.pearson.com/) — product line pricing theory
- [Stripe — usage-based billing patterns](https://stripe.com/billing) — modern SaaS mechanics
