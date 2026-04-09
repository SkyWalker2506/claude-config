---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Onboarding Checklist Design

## Quick Reference

**Checklist** = ordered tasks with **owner**, **due**, **dependency**, **artifact**. Split **customer-facing** vs **internal**. **Time-to-value (TTV)** metric: first meaningful outcome — define explicitly.

| Phase | Typical focus |
|-------|----------------|
| Kickoff | Goals, stakeholders, comms |
| Access | SSO, VPN, API keys, sandbox |
| Integration | Data mapping, test loads |
| Training | Role-based sessions |
| Go-live | Cutover, hypercare window |

## Patterns & Decision Matrix

| Segment | Checklist depth |
|---------|-----------------|
| SMB | 1-page checklist + self-serve links |
| Mid-market | RACI + weekly milestones |
| Enterprise | Workstream per domain (sec, data, app) |

## Code Examples

**Markdown checklist template:**

```markdown
## Onboarding — {{Customer}} — {{Project}}

### Week 0–1
- [ ] Kickoff scheduled — Owner: CSM — Due: {{date}}
- [ ] Success criteria doc signed — Owner: Customer PM
- [ ] Technical discovery questionnaire — Link: {{url}}

### Week 2–4
- [ ] UAT environment provisioned — Owner: Ops
- [ ] SSO tested (SAML) — Owner: IT + Vendor Sec
```

**RACI fragment:**

```text
Task: Initial data load
R: Vendor Solutions Eng
A: Customer Data Lead
C: Security officer
I: Exec sponsor
```

**TTV definition (single sentence for kickoff slide):**

```text
TTV = First production workflow completing {{named_use_case}} with {{success_metric}} met.
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| 200 tasks with no grouping | Phases + milestones |
| All tasks “CSM” | Clear customer duties |
| No exit criteria per phase | Gate reviews |

## Deep Dive Sources

- [Atlassian — RACI](https://www.atlassian.com/work-management/project-management/raci-chart) — responsibility model
- [TSIA — onboarding frameworks](https://www.tsia.com/) — services research
- [Gainsight — customer onboarding](https://www.gainsight.com/) — CS platform patterns
- [ISO 21500 — project management](https://www.iso.org/standard/50003.html) — structured delivery
