---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Quote Generation

## Quick Reference

**Quote** = commercial artifact with legal weight: line items, totals, **validity**, **payment terms**, **assumptions**, signature block. **Version control:** v1.0 → v1.1 with change log when discount or scope shifts.

| Must-have | Why |
|-----------|-----|
| Legal entity names | Contract counterparty |
| Currency + tax treatment | Invoice disputes |
| Delivery / acceptance criteria | Scope arguments |
| Expiry date | Protect against stale COGS |

## Patterns & Decision Matrix

| Deal size | Quote depth |
|-----------|-------------|
| Self-serve / PLG | Automated PDF from billing portal |
| SMB | 1–2 page quote + payment link |
| Enterprise | MSA + SOW + Order Form (often O1 owns narrative, O4 owns numbers) |

## Code Examples

**Order form row schema (CSV / CPQ export):**

```csv
line_id,sku,description,qty,unit_price,term_months,subtotal
1,PLT-ENT,Platform fee,1,12000,12,12000
2,SEAT-STD,Standard seat,150,29,12,52200
,,,,,Subtotal,64200
,,,,,Discount (10%),-6420
,,,,,Total (ex VAT),57780
```

**Assumptions block (paste-safe):**

```text
ASSUMPTIONS
1. Prices valid until 2026-05-09 unless superseded by written amendment.
2. Implementation start date no later than 2026-06-15 or rescoping may apply.
3. Third-party license fees (if any) billed pass-through without markup.
```

**Approval matrix documentation (for reps):**

```markdown
| Discount off list | Approver |
|-------------------|----------|
| ≤ 10% | Manager |
| 11–20% | VP Sales |
| > 20% | CFO + CEO |
```

## Anti-Patterns

| Mistake | Risk |
|---------|------|
| Verbal price not in writing | Revenue recognition fights |
| Missing governing law / entity | Legal redo |
| Copy last quote without COGS refresh | Negative deals |

## Deep Dive Sources

- [HubSpot quotes](https://knowledge.hubspot.com/quotes) — CRM-native quoting
- [Salesforce CPQ overview](https://www.salesforce.com/products/cpq/overview/) — enterprise CPQ
- [DocuSign — agreement workflows](https://www.docusign.com/) — e-signature process
- [ASC 606 / IFRS 15 summary](https://www.pwc.com/) — revenue rules for complex quotes
