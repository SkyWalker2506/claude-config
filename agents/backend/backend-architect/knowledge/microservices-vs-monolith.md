---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Microservices vs Monolith

## Quick Reference

| Dimension | Modular monolith | Microservices |
|-----------|------------------|----------------|
| Deploy unit | One artifact | Many services |
| Boundary enforcement | Packages/modules + discipline | Network API |
| Data | Often one DB (schemas can split) | Database per service (ideal) |
| Ops complexity | Lower | CI/CD, observability, k8s/service mesh |
| Team scaling | Good for <~15 engineers on product | Fits Conway-aligned teams per service |
| Failure blast radius | Whole app can fail | Isolated if truly decoupled |

**Sam Newman / ThoughtWorks guidance (paraphrased):** Prefer **evolution** — start where delivery is fastest, extract services when friction proves boundaries.

**2025–2026:** “Monolith first” or “modular monolith” is mainstream advice; microservices when org and load justify cost.

## Patterns & Decision Matrix

| Signal for monolith / modular monolith | Signal for microservices |
|----------------------------------------|---------------------------|
| Single team, early product-market fit | Multiple teams conflicting on deploy cadence |
| Tight transactional workflows across features | Clear bounded contexts with rare cross-TX need |
| Limited DevOps capacity | Mature platform team (K8s, tracing, SLOs) |
| Low traffic | Independent scaling of hot subsystems |

**Migration path:** **Strangler** — extract highest-value or most volatile boundary first; keep data sync explicit (events, CDC).

## Code Examples

**Modular monolith (package boundaries in one repo):**

```text
src/
  billing/     # no imports from orders → except via billing.api
  orders/
  shared/kernel/
```

**Service boundary contract:**

```yaml
# openapi fragment — orders exposes to billing
paths:
  /internal/orders/{id}/total:
    get:
      summary: Read order total for invoicing
```

## Anti-Patterns

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| Microservices for 3 developers | Integration hell, slow delivery | Merge to monolith or reduce services |
| Shared database across “microservices” | Hidden coupling, migration conflicts | DB per service or schema ownership |
| Distributed big ball of mud | Every change touches 5 repos | Redraw boundaries or consolidate |

## Deep Dive Sources

- [Martin Fowler — MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html)
- [Sam Newman — Building Microservices (O’Reilly)](https://www.oreilly.com/library/view/building-microservices-2nd-edition/9781492034018/) — book overview
- [ThoughtWorks Technology Radar — Microservices](https://www.thoughtworks.com/radar) — current industry stance (check latest edition)
- [CNCF — Cloud Native Landscape](https://landscape.cncf.io/) — tooling reality check for microservices ops
