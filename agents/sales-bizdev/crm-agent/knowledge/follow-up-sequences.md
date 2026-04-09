---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Follow-Up Sequences

## Quick Reference

**Sequences** = timed touch pattern after trigger (demo no-show, post-event, stalled deal). **Cadence** balances persistence vs annoyance; **opt-out** and **local law** (CAN-SPAM, GDPR marketing) are non-optional.

| Trigger | Typical length | Channels |
|---------|----------------|----------|
| Inbound demo request | 5–7 touches / 14 days | Email + call task |
| Closed lost nurture | Quarterly / 6 months | Email + LinkedIn (O3) |
| Post-purchase | Onboarding (O5) | Email + CSM task |

**Task vs email:** CRM should create **tasks** for human steps, not only automated emails.

## Patterns & Decision Matrix

| Segment | Tone |
|---------|------|
| Cold | Problem-first, one CTA |
| Warm referral | Social proof + single ask |
| Existing customer expansion | Usage insight + ROI hook |

## Code Examples

**5-touch email skeleton (plain text style):**

```text
Day 0:  Problem + specific question (reply-biased)
Day 2:  Micro-case (1 metric) + soft CTA
Day 5:  Resource link (non-gated) + "useful?" check
Day 9:  Breakup / permission to close file
Day 14: Final nudge — alternate contact offer
```

**HubSpot sequence documentation template:**

```markdown
## Sequence: Outbound — MM Tech
Enrollment: Active list "MM Tech ICP" AND no open deal
Exit: Reply OR meeting booked OR unsubscribe

Touch 1 (email): Template T-MM-01 — subject A/B test A1/A2
Touch 2 (+2d, task): Call — script snippet in CRM note
Touch 3 (+3d, email): Template T-MM-02
Touch 4 (+5d, task): LinkedIn connect — O3 copy pack L-MM-01
```

**Unsubscribe footer (required pattern):**

```text
{{Company}} | {{Address}}
Unsubscribe: {{unsubscribe_link}}
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Same copy to CEO and intern | Persona splits |
| No stop on OOO | Pause enrollment + resume rule |
| 12 emails in 5 days | Cap touches / week |
| Automated calls without local rules | Check country dialer regulations |

## Deep Dive Sources

- [CAN-SPAM Act compliance](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) — US commercial email
- [ICO — direct marketing UK](https://ico.org.uk/for-organisations/direct-marketing/) — GDPR/PECR
- [HubSpot sequences](https://knowledge.hubspot.com/sequences) — product docs
- [Sales Engagement Platforms — G2 category](https://www.g2.com/categories/sales-engagement) — tool landscape
