---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Handoff Protocol

## Quick Reference

**Sales → CS/Implementation** handoff needs **single artifact** + **meeting**. Minimum payload:

| Field | Content |
|-------|---------|
| Customer goals | Why they bought (verbatim quotes) |
| Scope | What was sold — SKU, limits, dates |
| Risks | Technical, political, competitive |
| Stakeholders | RACI, champions, blockers |
| Commercial | Contract highlights, renewal date |

**O5 owns** the template; **O2** stores on company/deal; **O1** validates scope language matches SOW.

## Patterns & Decision Matrix

| Deal complexity | Handoff |
|-----------------|---------|
| Simple | Async form + 30-min call |
| Complex | Formal handoff workshop + solution architect |

## Code Examples

**Internal handoff doc skeleton:**

```markdown
# Handoff — {{Account}} — Closed {{date}}

## Snapshot
- ARR / TCV: {{amount}}
- Go-live target: {{date}}
- CSM: {{name}} | SA: {{name}}

## What was promised (from order form §)
1. …
2. …

## Discovery notes (sales)
- Pain: …
- Success metric: …

## Risks / flags
- [ ] Data residency requirement: {{Y/N}}
- [ ] Custom dev sold: {{list}}

## Open threads
- Legal: …
- Security review: …
```

**CRM task bundle (conceptual):**

```text
On Deal = Closed Won:
  Create task "Internal handoff" — Owner: CSM — Due +2 business days
  Copy properties: deal_amount, products, primary_use_case
  Notify #customer-success Slack with template H01
```

**Sign-off line:**

```text
Sales AE confirms accuracy of commercial snapshot: _________________ Date: _____
CSM accepts handoff: _________________ Date: _____
```

## Anti-Patterns

| Mistake | Consequence |
|---------|-------------|
| “They know what they bought” | Scope creep fights |
| No written risks | Surprises at kickoff |
| Handoff after go-live | Churn |

## Deep Dive Sources

- [TSIA — sales to services handoff](https://www.tsia.com/) — research-backed workflows
- [Gainsight — handoff templates](https://www.gainsight.com/) — CS tooling
- [PRINCE2 / project handover](https://www.axelos.com/) — formal transition concepts
- [Atlassian Jira — CS projects](https://www.atlassian.com/software/jira/service-management) — ticket linkage
