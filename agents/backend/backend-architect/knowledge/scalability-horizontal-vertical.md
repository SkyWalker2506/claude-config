---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Scalability: Horizontal vs Vertical

## Quick Reference

| Scale mode | What you change | Typical trigger |
|------------|-----------------|-----------------|
| **Vertical (scale up)** | Bigger CPU/RAM/disk on one node | DB primary, license-bound workloads |
| **Horizontal (scale out)** | More instances behind LB | Stateless APIs, read replicas |
| **Functional split** | Separate service per load profile | CPU-heavy vs I/O-heavy paths |

**Throughput rough mental model:** Stateless app tier: horizontal linear-ish until DB or shared resource bottlenecks. **Strong consistency** often caps writes to single primary.

**Metrics to watch (2025–2026):** p95/p99 latency, saturation (CPU, conn pool), queue depth, error budget burn rate (SLO).

## Patterns & Decision Matrix

| Bottleneck | First lever | Second lever |
|------------|-------------|--------------|
| Stateless HTTP layer | Add replicas + autoscaling | CDN for static; connection pooling |
| Read-heavy DB | Replicas, caching, materialized views | Partition read models (CQRS) |
| Write-heavy DB | Shard/partition strategy, queue writes | Reduce hot keys, async processing |
| Session state on server | Sticky sessions (fragile) or external session store | Redis, signed cookies |
| Large payloads | Compression, pagination, field filtering | GraphQL or sparse DTOs |

**When vertical wins:** Managed DB tier where HA pair is vendor-managed; single-node analytics; strict serial workloads.

**When horizontal wins:** API workers, batch workers, stateless containers (Kubernetes HPA).

## Code Examples

**Autoscaling signal (pseudo — target CPU 60%):**

```yaml
# Kubernetes HPA sketch
metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

**Read replica routing (conceptual):**

```text
writes → primary.postgresql.internal:5432
reads  → replica.postgresql.internal:5432 (lag-aware if needed)
```

## Anti-Patterns

| Anti-pattern | Why | Better |
|--------------|-----|--------|
| Scale DB vertically forever | Cost + single point of failure | Replicas, partitioning, archive cold data |
| Cache-aside without TTL/invalidation | Stale reads, incidents | TTL + event-driven invalidation |
| Autoscale on CPU only for latency issues | CPU idle but GC/locks hurt | Golden signals + SLO-based scaling |

## Deep Dive Sources

- [Google SRE — Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/) — metrics that matter
- [AWS — Well-Architected Performance Efficiency](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html)
- [CNCF — Kubernetes Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [PostgreSQL — High Availability](https://www.postgresql.org/docs/current/high-availability.html) — replication concepts
