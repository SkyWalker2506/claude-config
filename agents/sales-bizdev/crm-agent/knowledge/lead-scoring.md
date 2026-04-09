---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Lead Scoring

## Quick Reference

**Goal:** Prioritize SDR/AE time; route MQLs to nurture vs sales. **Hybrid model** (2025–2026): explicit rules + behavioral signals + (optional) predictive from CRM/MAP.

| Signal type | Examples |
|-------------|----------|
| Fit (firmographic) | Industry, size, geo, tech stack |
| Intent (behavioral) | Pricing page, demo request, repeat visits |
| Engagement | Email clicks, webinar attendance |
| Negative | Competitor domain, job title “student”, bad fit geo |

**Calibration:** Review monthly — scores should correlate with **SQO→win**, not just volume.

## Patterns & Decision Matrix

| Stack | Approach |
|-------|----------|
| HubSpot only | HubSpot score properties + workflows |
| HubSpot + data enrichment | Clearbit/Apollo fields → fit points |
| Full MAP (Marketo, etc.) | Scoring programs with recency decay |

## Code Examples

**Linear point model (spreadsheet-ready):**

```text
FIT (max 40)
  +10  Employee count 200–2000
  +10  Industry in {FinTech, HealthIT}
  +10  Country in ICP list
  +10  Uses complementary stack (e.g. Salesforce)

BEHAVIOR (max 40)
  +15  Demo requested
  +10  Visited pricing 2+ times in 14d
  +8   Attended live webinar
  +7   Opened last 3 emails

NEGATIVE (floor 0)
  -20  Competitor email domain
  -15  Employee count < 20 (for ENT product)

MQL threshold: 60 → route to AE
SAL threshold: 70 + AE acceptance
```

**Decay rule (document for revops):**

```text
Behavior points decay 25% every 30 days without meaningful activity
(meaningful = pricing, demo, high-intent page)
```

**SQL handoff payload (what O2 sends to O3/O1):**

```yaml
lead_id: HS-88291
score: 68
top_signals:
  - pricing_page_views: 4
  - industry_match: true
recommended_action: "Book discovery — template B"
```

## Anti-Patterns

| Mistake | Why |
|---------|-----|
| Static scores forever | Stale priority, angry AEs |
| Only email opens | Bots inflate score |
| Same model for all products | ICP differs by SKU |

## Deep Dive Sources

- [HubSpot — lead scoring](https://knowledge.hubspot.com/lead-scoring) — native tooling
- [Forrester — B2B buying groups](https://www.forrester.com/) — account-level scoring context
- [Gartner — intent data](https://www.gartner.com/en/marketing/insights/intent-data) — third-party intent caveats
- [PECR / ePrivacy (EU)](https://ico.org.uk/for-organisations/guide-to-pecr/what-are-pecr/) — tracking consent for behavioral scoring
