---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Cold Email Patterns

## Quick Reference

**Goal:** Earn a reply or meeting — not deliver a pitch. **Under ~120 words** for first touch. **One CTA** (15-min call, specific question). **Personalization** = relevant hook, not flattery.

| Element | Good | Weak |
|---------|------|------|
| Subject | Specific outcome or trigger event | “Quick question” only |
| Opener | Trigger + why them | “I hope this finds you well” |
| Body | Problem → insight → proof hint | Feature list |
| CTA | Binary, low friction | “Let me know your thoughts” |

**Deliverability:** SPF/DKIM/DMARC on sending domain; warm infra; list hygiene — coordinate with ops.

## Patterns & Decision Matrix

| ICP | Pattern |
|-----|---------|
| Technical buyer | Concrete bug/constraint hypothesis |
| Economic buyer | Cost of status quo with range |
| Practitioner | Workflow observation from public content |

## Code Examples

**A/B subject lines (store in CRM):**

```text
A: "{{Company}} — cutting {{metric}} reconciliation time"
B: "Question on {{recent_initiative}} (public post)"
C: "3 teams fixed {{pain}} with {{approach}} — fit for you?"
```

**First email body (template with merge fields):**

```text
Hi {{FirstName}},

Noticed {{trigger: funding|hire|tech_change}} — teams in {{industry}}
often hit {{pain_short}} when {{context}}.

We helped {{peer_company}} get to {{result_metric}} in {{timeframe}}.

Worth a 15-min compare notes on {{specific_topic}}?

— {{Sender}}
```

**Reply classification tags for O2 CRM update:**

```text
POSITIVE — book meeting
OBJECTION — timing/budget → nurture
OOO — pause sequence
NEGATIVE — opt out + close
```

## Anti-Patterns

| Mistake | Why |
|---------|-----|
| Fake “Re:” threads | Legal/spam filter risk |
| Long PDF attachment on email 1 | Deliverability + friction |
| Same domain blast 10k/day | Blocklisting |
| Scraped emails without role fit | Spam reports |

## Deep Dive Sources

- [Google Workspace — email sender guidelines](https://support.google.com/a/answer/81126) — bulk sending
- [M3AAWG — best practices](https://www.m3aawg.org/published-documents) — anti-abuse
- [Lavender / outreach writing](https://www.lavender.ai/) — modern email coaching tools
- [CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) — US rules
