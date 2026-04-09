---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# A/B Test Methodology

## Quick Reference

**Definition:** Randomized controlled experiment comparing *variants* on the same traffic with a pre-registered **primary metric** and **guardrails**.

- **Unit of diversion:** User, session, or cookie—must match how users *experience* consistency (sticky assignment).
- **Minimum detectable effect (MDE):** Smallest lift you care to detect—drives sample size.
- **Bridge to M2:** **M2 Landing Page Agent** supplies DOM anchors, copy IDs, and creative assets per variant.
- **Bridge to M4:** **M4 Analytics Agent** implements `exposure` + conversion events with identical firing rules across variants.

| Phase | Deliverable |
|-------|-------------|
| Design | Hypothesis, metrics, power |
| Run | QA, monitor SRM |
| Analyze | Stats, segment sanity |
| Ship | Rollout + doc |

## Patterns & Decision Matrix

| Question | Options | Pick when |
|----------|---------|-----------|
| One vs two-sided test | One-sided (lift only) vs two-sided | Default two-sided unless strong directional prior |
| Frequentist vs Bayesian | p-value vs probability of best | Org maturity; Bayesian needs priors discipline |
| Sequential vs fixed-horizon | Peeking allowed vs not | Use proper sequential methods if peeking |

**Hypothesis template**

> Because `{insight}`, we expect `{change}` to increase `{metric}` for `{segment}`. We measure guardrails `{list}`.

## Code Examples

**1) Experiment brief (Markdown)**

```markdown
## EXP-2026-041
- **Owner:** M3
- **Primary:** `trial_start` rate
- **Guardrails:** bounce_rate, refund_7d
- **Diversion:** user_id hash
- **Variants:** control, b_headline, b_cta
- **Runtime:** 14d min OR 100k exposures (whichever later)
- **M2 assets:** hero_h1_a/b, cta_primary_a/b
- **M4 events:** `exp_exposure`, `trial_start`
```

**2) SRM check (concept)**

```sql
-- Expect ~equal assignments per variant
SELECT variant, COUNT(*) FROM exp_assignments
WHERE exp_id = 'EXP-2026-041' GROUP BY variant;
```

## Anti-Patterns

- **Changing traffic allocation** mid-test without accounting—breaks comparability.
- **Optional stopping** without correction—inflates false positives.
- **HARKing** (hypothesis after results)—invalidates p-values.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google — Foundational A/B testing](https://developers.google.com/machine-learning/crash-course/fairness/evaluating-models) — evaluation mindset (related: fairness splits)
- [Microsoft — Controlled experiments](https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/) — industrial practice
- [Evan Miller — Sequential](https://www.evanmiller.org/sequential-ab-testing.html) — peeking-aware overview
- [IMPROVED — Guideline for reporting experiments](https://arxiv.org/abs/2003.07602) — transparent reporting checklist
