---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Proposal Structure

## Quick Reference

| Section | Purpose | Typical length |
|---------|---------|------------------|
| Executive summary | Decision-maker hook, outcome promise | 1 page |
| Situation / problem | Buyer context, quantified pain | 1–2 pages |
| Proposed solution | What you deliver, how it works | 2–4 pages |
| Scope & deliverables | In / out of scope, milestones | 1–2 pages |
| Timeline | Phases, dependencies, client duties | 1 page |
| Commercials | Pricing ref O4, payment terms, SLA | 1–2 pages |
| Assumptions & dependencies | Legal/technical guardrails | 1 page |
| Next steps | Signature, kickoff, contact | 0.5 page |

**2025–2026:** Buyers skim PDFs on mobile; put numbers and dates in first 2 pages. Pair narrative doc with appendix for security/compliance artifacts.

## Patterns & Decision Matrix

| Deal type | Structure emphasis |
|-----------|-------------------|
| SMB / fast cycle | Short exec summary + 1-page SOW + price table |
| Mid-market | Full structure + risk/assumptions prominent |
| Enterprise / RFP | Mirror issuer section order; compliance matrix in appendix |
| Partner / reseller | Margin-friendly packaging; minimal IP detail in main body |

## Code Examples

**Outline skeleton (Markdown):**

```markdown
# Proposal — {{Company}} / {{Project}}

## Executive summary
- Outcome: {{metric}} in {{timeframe}}
- Why us: 3 bullets (proof)

## Current situation
- Pain: {{quantified}}
- Constraints: {{tech, timeline, budget band}}

## Solution overview
| Capability | Your need | Our answer |
|------------|-----------|------------|

## Scope
**In scope:** …
**Out of scope:** …

## Commercial summary
See `pricing-presentation.md` table — total {{currency}} {{amount}}.

## Assumptions
1. …
```

**YAML front-matter for generated PDFs (Pandoc-style metadata):**

```yaml
---
title: "Technical & Commercial Proposal"
author: "{{Vendor Legal Name}}"
date: 2026-04-09
customer: "{{Legal Entity}}"
version: 1.2
classification: Confidential
---
```

## Anti-Patterns

| Mistake | Why it fails | Fix |
|---------|--------------|-----|
| Features before outcomes | Exec summary ignored | Lead with business result, then features |
| Hidden scope creep in vague bullets | Disputes post-sale | Explicit out-of-scope + change process |
| Single wall of text | No skim path | Tables, callouts, page-1 KPI box |
| Copy-paste from old deals | Wrong assumptions | Assumptions section per deal |

## Deep Dive Sources

- [Shipley Associates — proposal best practices](https://www.shipleywins.com/) — win-theme and persuasion structure
- [APMP Body of Knowledge](https://www.apmp.org/) — professional proposal management standards
- [Gartner — B2B buying journey](https://www.gartner.com/en/sales/insights/b2b-buying) — stakeholder alignment
- [Harvard Business Review — selling solutions](https://hbr.org/) — value framing (search current articles)
