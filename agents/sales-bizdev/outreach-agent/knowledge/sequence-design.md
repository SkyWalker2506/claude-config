---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Sequence Design

## Quick Reference

**Sequence** = ordered touches with delays and branches. **Design for exit:** reply, meeting, bounce, unsubscribe. **Channel mix:** email + call tasks + LinkedIn (O3) + optional direct mail for enterprise.

| Building block | Role |
|------------------|------|
| Step | Single touch + owner |
| Delay | Business days vs calendar |
| Branch | If opened / if clicked / if no reply |
| Goal metric | Reply rate, meeting rate, not opens alone |

## Patterns & Decision Matrix

| Motion | Length | Steps |
|--------|--------|-------|
| Inbound fast response | 3–5 days | 3–4 |
| Cold outbound | 14–21 days | 5–8 |
| Nurture | 90+ days | Monthly |

## Code Examples

**Sequence map (Mermaid-compatible logic doc):**

```text
START
  → Email 1 (Day 0)
  → wait 2 business days
  → if REPLY → exit SUCCESS
  → Call task (Day 2) — owner SDR
  → wait 2 business days
  → Email 2 (value asset)
  → wait 3 business days
  → LinkedIn connect (O3 template L-04)
  → wait 5 business days
  → Email 3 (case study) — last in sequence
  → exit NURTURE or CLOSE
```

**JSON-like definition for tooling integration:**

```json
{
  "id": "seq_outbound_mm_v3",
  "steps": [
    {"type": "email", "template": "E-MM-01", "delay_days": 0},
    {"type": "task_call", "script_id": "CALL-MM-01", "delay_days": 2},
    {"type": "email", "template": "E-MM-02", "delay_days": 2}
  ],
  "exit_on": ["reply", "meeting_booked", "unsubscribe"],
  "owner_role": "SDR"
}
```

**KPI targets (illustrative — calibrate per industry):**

```text
Cold sequence: reply rate 2–6%, meeting rate 0.5–2%
Warm inbound: reply rate 15–35%
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Optimizing for opens | Optimize for replies/meetings |
| No branch on positive reply | Stop automated steps immediately |
| Identical copy across segments | At least opener rotation |

## Deep Dive Sources

- [HubSpot sequences](https://knowledge.hubspot.com/sequences) — implementation reference
- [Salesforce — cadences (High Velocity Sales)](https://help.salesforce.com/) — enterprise pattern
- [Outreach.io / Salesloft — category leaders](https://www.g2.com/) — feature parity ideas
- [DMA — responsible marketing](https://www.dma.org.uk/) — UK sequence ethics
