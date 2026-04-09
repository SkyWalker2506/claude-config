---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Root Cause: 5 Whys and Fishbone

## Quick Reference

| Method | Use |
|--------|-----|
| **5 Whys** | Chain of causation — stop at process fix, not blame |
| **Fishbone (Ishikawa)** | Categories: People, Process, Tools, Data, Environment |

**Stopping rule:** When corrective action is identifiable and verifiable.

**2025–2026:** Pair with postmortem template (Google SRE style) — action items with owners.

## Patterns & Decision Matrix

| Incident scale | Depth |
|----------------|-------|
| Sev-1 | Full 5 Whys + timeline |
| Minor bug | Short RCA in ticket |

## Code Examples

```text
Why outage? Deploy failed health check.
Why? DB connection pool exhausted.
Why? New cron doubled connections.
Why? No pool limit in cron path.
Why? Missing code review checklist item.
→ Fix: pool cap + lint rule + review checklist
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Stopping at human error | No systemic fix |
| Single root for complex failure | Multiple contributing factors |

## Deep Dive Sources

- [Toyota — 5 Whys (ASQ)](https://asq.org/quality-resources/five-whys)
- [Atlassian — Postmortems](https://www.atlassian.com/incident-management/postmortem)
