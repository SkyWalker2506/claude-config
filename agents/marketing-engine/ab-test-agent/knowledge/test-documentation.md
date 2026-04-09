---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Test Documentation

## Quick Reference

**Living doc** answers: Why did we run? What did we change? How did we measure? What did we decide?

- **IDs:** `EXP-YYYY-NNN` in Jira/Notion + same in GA4 custom dimension / warehouse.
- **Handoffs:** M2 (assets) → M3 (design) → M4 (instrumentation) → M3 (analysis) → PM (ship).
- **Bridge to M2:** Archive final copy tables and screenshots—**M2** is source of visual truth.
- **Bridge to M4:** Event dictionary appendix—**M4** signs off that `exposure` fires before conversions.

| Section | Owner |
|---------|-------|
| Hypothesis & metrics | M3 |
| Creative changelog | M2 |
| Event QA log | M4 |

## Patterns & Decision Matrix

| Artifact | Purpose |
|----------|---------|
| One-pager | Stakeholder alignment |
| PR + config diff | Engineering audit trail |
| Dashboard link | Live monitoring |
| Post-mortem | Losses teach more than wins |

**Ship decision matrix**

| Outcome | Action |
|---------|--------|
| Stat sig + guardrails OK | Rollout 100% |
| Directional + underpowered | Extend or replicate |
| Sig but guardrail hurt | Iterate new test |

## Code Examples

**1) Post-experiment summary (template)**

```markdown
## EXP-2026-041 — Hero headline
- **Dates:** 2026-04-01 — 2026-04-14
- **Primary:** trial_start +4.2% rel (95% CI [0.8%, 7.9%]), p=0.02
- **Guardrails:** bounce flat, support tickets flat
- **SRM:** pass (p=0.41)
- **Decision:** Ship variant B; M2 to merge copy to main branch
- **Follow-up:** EXP-2026-048 CTA color (de-risk interaction)
```

**2) Event QA checklist**

```markdown
- [ ] `exp_exposure` once per user per experiment
- [ ] `trial_start` deduped by order id
- [ ] UTM preserved on redirect variants
- [ ] DebugView session recorded (link)
```

## Anti-Patterns

- **“We tested something in April”** with no ID—cannot reproduce.
- **Winner shipped** without removing dead code paths—tech debt.
- **Ignoring failed tests**—no learning captured.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [CONSORT — reporting trials](http://www.consort-statement.org/) — structured reporting (adapt for web)
- [Google Docs — Experiment review template](https://support.google.com/docs/) — collaborative docs (platform-neutral)
- [GitHub — PR best practices](https://docs.github.com/en/pull-requests) — code-linked experiments
- [dbt — Analytics engineering](https://docs.getdbt.com/docs/introduction) — warehouse-side experiment models
