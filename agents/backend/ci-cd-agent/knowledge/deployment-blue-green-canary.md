---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Deployment: Blue-Green and Canary

## Quick Reference

| Strategy | Flow |
|----------|------|
| **Blue-green** | Two identical envs; switch traffic instantly |
| **Canary** | Small % to new version; ramp if healthy |
| **Rolling** | Replace instances in place |

**Health:** Readiness probe before receiving traffic; automated rollback on error rate.

**2025–2026:** Kubernetes Deployment + progressive delivery (Argo Rollouts, Flagger).

## Patterns & Decision Matrix

| Risk tolerance | Strategy |
|----------------|----------|
| Low risk app | Rolling |
| High impact | Canary + metrics |

## Code Examples

```yaml
# Flagger-style (conceptual)
canary:
  stepWeight: 20
  maxWeight: 100
  metrics:
    - name: request-success-rate
      threshold: 99
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Canary without metrics | Blind promotion |

## Deep Dive Sources

- [Martin Fowler — BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [CNCF — Flagger](https://flagger.app/)
