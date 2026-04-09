---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Welcome Sequence

## Quick Reference

**Welcome sequence** = emails/in-app messages from **signature to first value**. **Tone:** confirm purchase, set expectations, reduce anxiety. **Cadence:** Day 0, 1, 3, 7 — adjust per product complexity.

| Message | Job |
|---------|-----|
| 0 (immediate) | Receipt + what happens next + owner contact |
| 1 | Access + first login / book kickoff |
| 3 | Quick win tutorial or checklist |
| 7 | Check-in + feedback loop |

**Align with O2:** CRM lifecycle stage “Onboarding” triggers; exit when health score / milestone met.

## Patterns & Decision Matrix

| Product | Channel mix |
|---------|-------------|
| PLG | In-app > email |
| High-touch | Email + CSM call |
| Enterprise | Executive sponsor letter + project charter |

## Code Examples

**Email 0 (plain structure):**

```text
Subject: You're in — next 3 steps for {{Product}}

Hi {{FirstName}},

Welcome aboard. Here's what happens now:
1) {{action}} — {{link}} (takes ~5 min)
2) Book kickoff: {{scheduling_link}}
3) Meet your team: {{CSM_name}}, {{email}}

Questions? Reply to this email — we read every message.

— {{CSM}}
```

**In-app checklist (copy doc for product):**

```text
Step 1 of 5: Connect {{integration}}
[Connect button]  Estimated 4 min
Tip: You'll need Admin on {{system}} — grab {{role}} first.
```

**Unsubscribe:** Transactional onboarding emails often exempt from marketing unsubscribe — still offer **preference center** for non-critical tips; legal review for jurisdiction.

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Salesy upsell in email 1 | Trust first |
| No single owner named | Anxiety + support load |
| Identical copy for all SKUs | Segment by tier |

## Deep Dive Sources

- [CAN-SPAM — transactional vs commercial](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) — US classification
- [ICO — direct marketing UK](https://ico.org.uk/for-organisations/direct-marketing/) — consent lines
- [Intercom — onboarding messages](https://www.intercom.com/) — in-app patterns
- [HubSpot — customer onboarding emails](https://knowledge.hubspot.com/) — automation tie-in
