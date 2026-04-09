---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Personalization at Scale

## Quick Reference

**Tiers:** (1) **Segment** — industry/role messaging. (2) **Account** — logo, tech stack, news. (3) **1:1** — high-value only. **Cost model:** research minutes × hourly rate vs expected pipeline $.

| Tier | Data sources | Typical depth |
|------|--------------|---------------|
| Segment | CRM + firmographics | Mail merge only |
| Account | News, 10-K, job posts | 1 custom sentence |
| Strategic | Podcast, earnings call | Paragraph + custom asset |

**2025–2026:** AI drafts scale fast — add **human QA** on facts and names; hallucination = deliverability and brand risk.

## Patterns & Decision Matrix

| Volume / week | Approach |
|---------------|----------|
| < 200 | Semi-automated research + templates |
| 200–2000 | Enrichment API + conditional paragraphs |
| > 2000 | Segment-level only + sample 1:1 for whales |

## Code Examples

**Snippet library (YAML-style for generators):**

```yaml
industry_hooks:
  fintech:
    opener: "With {{regulatory}} timelines, {{pain}} usually spikes before audits."
  retail:
    opener: "Peak season prep often surfaces {{pain}} in ops teams."

triggers:
  funding:
    line: "Congrats on the {{round}} — scaling {{function}} is a common next hurdle."
  new_exec:
    line: "Saw {{name}} joined as {{role}} — often a window to revisit {{initiative}}."
```

**QA checklist before send (per batch):**

```markdown
- [ ] Company name matches domain
- [ ] Trigger fact has public URL saved in CRM note
- [ ] No competitor praised by mistake
- [ ] Unsubscribe / opt-out path present (email)
```

**Formula for rep time budget:**

```text
Accounts tier-A: 20 × 12 min research = 240 min/week
Accounts tier-B: 80 × 3 min = 240 min/week
Total cap 8h — remainder stays segment-only
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Fake personalization (“love your website”) | Cite one specific public fact |
| Wrong person after reorg | Verify title on LinkedIn same week |
| AI fabricates metrics | Human verify numbers |

## Deep Dive Sources

- [Clearbit / enrichment category](https://clearbit.com/) — firmographic APIs (compare vendors)
- [LinkedIn — Sales Insights](https://business.linkedin.com/sales-solutions) — social selling context
- [Gartner — B2B buying group](https://www.gartner.com/en/sales/insights/b2b-buying) — multi-thread personalization
- [ICO — automated decision-making](https://ico.org.uk/for-organisations/guide-to-data-protection/key-dp-themes/individual-rights/individual-rights/) — EU profiling awareness
