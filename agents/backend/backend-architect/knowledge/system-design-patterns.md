---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# System Design Patterns

## Quick Reference

| Pattern | Problem | Typical building blocks |
|---------|---------|-------------------------|
| **Layered (n-tier)** | Separation of concerns | API → service → repository → DB |
| **CQRS** | Read/write scale & model divergence | Command bus + read models + events |
| **Event sourcing** | Full audit + time travel | Event store + projections |
| **Saga** | Distributed transactions | Choreography vs orchestration |
| **API Gateway** | Single entry, auth, routing | Kong, Envoy, AWS API Gateway |
| **BFF (Backend for Frontend)** | Per-client API shape | One BFF per app (web/mobile) |
| **Strangler fig** | Legacy replacement | Proxy new routes incrementally |

**2025–2026 validity:** Core patterns are stable; managed services (API GW, event buses) vendor-specific — verify quotas and limits in target cloud.

## Patterns & Decision Matrix

| If you need… | Prefer | Avoid when… |
|--------------|--------|-------------|
| Simple CRUD + one team | Layered monolith | You already have 5+ deployable services with tight coupling |
| High read traffic, rare writes | CQRS (+ cache on read side) | Team cannot maintain dual models and sync |
| Audit/compliance for all state changes | Event sourcing | Reporting is ad-hoc SQL-only and team lacks event skills |
| Long-running business process across services | Saga (orchestrated often clearer) | Single DB transaction suffices |
| Mobile + web with different payloads | BFF per channel | Duplication cost > benefit (then shared API + versioning) |

**Load / failure:** Pair patterns with explicit **SLA** (p99 latency) and **failure modes** (circuit breaker, bulkhead) — see scalability doc for scale-out.

## Code Examples

**Strangler routing (conceptual — ingress or reverse proxy):**

```nginx
# New checkout goes to new service; rest legacy
location /api/v2/checkout/ {
    proxy_pass http://checkout-service:8080;
}
location /api/ {
    proxy_pass http://legacy-monolith:8080;
}
```

**Saga orchestration (pseudo — state machine):**

```text
OrderCreated → ReserveInventory → ChargePayment → Ship
                 ↓ fail           ↓ fail
            ReleaseInventory   RefundPayment
```

## Anti-Patterns

| Anti-pattern | Why it hurts | Instead |
|--------------|--------------|---------|
| Distributed monolith | Services deployed separately but tightly coupled | Bound contexts + clear APIs or merge to monolith |
| “Microservices from day one” | Ops complexity without domain clarity | Monolith first, extract when boundaries clear |
| God service | One service owns everything | Split by bounded context |
| Chatty sync calls between services | Latency cascade | Batch, async events, or consolidate |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [AWS Well-Architected — Reliability & Operational Excellence](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — production pillars
- [Martin Fowler — Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/) — classic catalog
- [Microsoft Azure Architecture Center — Architecture styles](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/) — styles and trade-offs
- [Google Cloud — Design patterns for microservices](https://cloud.google.com/architecture/microservices) — reference patterns on GCP
