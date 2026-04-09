---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Pipeline Management

## Quick Reference

**Healthy pipeline:** Enough **coverage** (pipeline $ / quota) and **velocity** (avg days per stage). **Stage definitions** must be binary testable — not “nice conversation had.”

| Metric | Typical signal |
|--------|----------------|
| Win rate | Quality of top-of-funnel |
| Average deal size | Packaging / discount discipline |
| Sales cycle length | Friction in evaluation |
| Stage conversion % | Where deals die |

**Forecast categories:** Commit / Best case / Pipeline — align with finance definitions, not rep optimism.

## Patterns & Decision Matrix

| Maturity | Pipeline design |
|----------|-----------------|
| Startup | Few stages; weekly review; founder-led |
| Scale-up | Segment pipelines; MEDICC or similar qualification |
| Enterprise | Separate renewal/expansion; legal stage explicit |

## Code Examples

**Stage exit criteria (documentation snippet):**

```markdown
### Stage: Discovery complete → Evaluation
- [ ] Champion identified (contact record + role)
- [ ] Problem quantified (numeric field filled)
- [ ] Budget band confirmed or procurement path known
- [ ] Next meeting scheduled < 14 days
```

**Coverage math (spreadsheet):**

```text
Quarter quota:        500,000
Target coverage 3x:   1,500,000
Open pipeline:        1,200,000  → gap 300,000 → accelerate top of funnel
```

**Weekly pipeline review agenda (30 min):**

```text
1. New (7d) — qualify in/out
2. Slipped close dates — root cause
3. Stalled in stage > median+1σ — action
4. Next week commits — evidence check
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Backdating stages for forecast | Audit trail + manager criteria |
| Everything in “Proposal” | Split negotiation vs sent |
| Ignoring leakage at one stage | Funnel analysis by cohort |

## Deep Dive Sources

- [Salesforce — pipeline inspection](https://www.salesforce.com/resources/articles/sales-pipeline/) — concepts transfer across CRMs
- [MEDDICC / MEDDPICC](https://www.meddicc.com/) — qualification frameworks
- [SaaS Metrics — David Skok](https://www.forentrepreneurs.com/saas-metrics-2/) — unit economics link to pipeline
- [Gartner — sales analytics](https://www.gartner.com/en/sales) — forecasting hygiene
