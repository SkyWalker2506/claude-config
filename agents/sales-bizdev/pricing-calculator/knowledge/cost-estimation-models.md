---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Cost Estimation Models

## Quick Reference

**Internal cost** drives floor price before margin (see `margin-calculation.md`). Common models:

| Model | Formula idea | Best for |
|-------|--------------|----------|
| T&M | Σ(hours × blended rate) | Custom services |
| Unit / seat | units × cost-to-serve | SaaS |
| Activity-based | drivers (tickets, GB, API calls) | Usage products |
| Milestone | % weight per deliverable | Projects |

**Burden:** Add overhead % (tools, management, bench) consistently — do not cherry-pick per deal.

## Patterns & Decision Matrix

| Uncertainty | Approach |
|-------------|----------|
| Low | Fixed internal hours from past projects |
| Medium | Range (P50/P90) + risk buffer line |
| High | T&M not-to-exceed or phased discovery |

## Code Examples

**T&M build (spreadsheet logic):**

```text
Role          Hours   Blended $/h   Subtotal
PM            40      120           4800
Senior Dev    120     150           18000
QA            24      90            2160
────────────────────────────────────────────
Direct labor                      24960
Overhead 18%                      4493
Risk reserve 10% (of subtotal)    2945
Total internal cost               32398
```

**Seat cost-to-serve (annual, illustrative):**

```text
Infra + support per seat:  180
CSM alloc per enterprise:  4000 / 50 seats = 80
────────────────────────────────────────────
Cost to serve per seat:    260/year
```

**Driver-based API cost:**

```text
Cost per 1M calls = (lambda_compute + egress + logging) / 1M
Floor price per call = cost_per_call × (1 + target_margin)
```

## Anti-Patterns

| Mistake | Risk |
|---------|------|
| Sales hours not in estimate | Margin death post-sale |
| Ignore support load | Churn cost |
| One hero dev forever | Unrealistic repeatability |

## Deep Dive Sources

- [Activity-based costing — CIMA](https://www.cimaglobal.com/) — management accounting foundation
- [AWS Pricing Calculator](https://calculator.aws/) — infra cost modeling
- [TCO frameworks — Gartner](https://www.gartner.com/) — enterprise comparisons
- [IFRS 15](https://www.ifrs.org/) — revenue/cost alignment awareness
