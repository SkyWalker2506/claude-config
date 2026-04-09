---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Margin Calculation

## Quick Reference

| Term | Meaning |
|------|---------|
| COGS / COS | Direct cost to deliver |
| Gross margin % | (Revenue − COGS) / Revenue |
| Contribution margin | Revenue − variable costs (excludes fixed alloc) |
| Markup % | (Price − Cost) / **Cost** — do not confuse with margin |

**SaaS shorthand:** Gross margin often targeted **70%+** software-only; services-heavy mixes lower blended margin.

## Patterns & Decision Matrix

| Decision | Use margin | Use markup |
|----------|------------|------------|
| Board/investor reporting | Yes | Rare |
| Partner discount from list | Sometimes | Often (reseller) |
| Internal price floor | Both — document which | |

## Code Examples

**Margin from price and cost:**

```python
def gross_margin_pct(price: float, cogs: float) -> float:
    return (price - cogs) / price * 100

# Example
price, cogs = 12000.0, 4200.0
# margin = (12000-4200)/12000 = 65%
```

**Markup to achieve target margin:**

```text
Given cost C and target gross margin M (as decimal):
Price = C / (1 - M)

Example: C = 8000, target M = 0.75
Price = 8000 / 0.25 = 32000
```

**Discount guardrail:**

```text
List price: 100
Floor margin 60% → max COGS 40
If COGS = 35, min price = 35 / (1 - 0.6) = 87.5
Max discount from list = 12.5%
```

**Multi-currency note for quotes:**

```text
FX rate source: ECB daily / OANDA — snapshot date on quote PDF
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Markup labeled “margin” | Standardize terms in O1/O4 |
| Ignore payment terms cost | NPV of cash delay |
| Variable COGS but fixed price | Price review clause or usage tier |

## Deep Dive Sources

- [Investopedia — gross margin](https://www.investopedia.com/terms/g/grossmargin.asp) — definitions
- [SaaS metrics — Bessemer](https://www.bvp.com/atlas) — industry benchmarks
- [Harvard Business Review — pricing](https://hbr.org/topic/subject/pricing) — strategy link
- [IFRS 15 — performance obligations](https://www.ifrs.org/) — multi-element deals
