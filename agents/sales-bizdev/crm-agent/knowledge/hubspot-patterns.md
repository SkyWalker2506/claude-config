---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# HubSpot Patterns

## Quick Reference

**Core objects:** Contacts, Companies, Deals, Tickets (service). **Associations** link records; **pipelines** are per object (e.g. deal stages). **Properties** = fields; prefer custom groups over cluttering default groups.

| Pattern | Use when |
|---------|----------|
| Deal pipeline per segment | Different stages/SKUs (SMB vs ENT) |
| Required properties on stage move | Data quality at handoffs |
| Workflows (automation) | SLA-based tasks, not complex branching logic |
| Lists (active vs static) | Campaigns vs one-time audits |

**2025–2026:** HubSpot AI features surface next actions — keep properties clean or suggestions degrade.

## Patterns & Decision Matrix

| Need | HubSpot tool |
|------|----------------|
| Lead routing | Workflow + if/then branches or Operations Hub routing |
| Duplicate control | Duplicate management + merge rules |
| Quote → Deal | Quotes tied to deal; products in product library |
| Reporting | Single-object reports first; datasets for cross-object |

## Code Examples

**Deal property naming (consistent prefix):**

```text
deal_segment__c          (picklist: SMB | MM | ENT)
primary_use_case__c      (multi-select)
competitor_named__c      (text)
next_step_date__c        (date)
```

**Workflow pseudo-logic (documentation for admins):**

```text
TRIGGER: Deal stage changes to "Proposal Sent"
ACTIONS:
  - Set property proposal_sent_date = today
  - Create task for owner: "Follow up in 3 business days" due +3 days
  - Internal notification to #sales-deals if amount > 50000
```

**Association labels (conceptual):**

```text
Contact → Company: "Employee" (default)
Contact → Deal: "Primary contact" | "Economic buyer"
```

## Anti-Patterns

| Mistake | Impact |
|---------|--------|
| 200 custom fields unused | Low adoption, bad AI |
| One catch-all pipeline | Wrong forecasting |
| Workflows fighting manual edits | Duplicate emails, trust loss |
| Storing PII in open text without purpose | Compliance risk |

## Deep Dive Sources

- [HubSpot Knowledge Base](https://knowledge.hubspot.com/) — official how-tos
- [HubSpot Developers — CRM APIs](https://developers.hubspot.com/docs/api/crm/understanding-the-crm) — object model
- [HubSpot Academy](https://academy.hubspot.com/) — free certifications
- [SOC 2 / HubSpot trust](https://www.hubspot.com/security) — security posture for enterprise buyers
