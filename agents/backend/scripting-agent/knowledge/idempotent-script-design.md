---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Idempotent Script Design

## Quick Reference

| Principle | Meaning |
|-----------|---------|
| **Idempotent** | Second run = same end state |
| **Keys** | Natural id or idempotency key store |
| **Locks** | `flock` or DB advisory lock for concurrent runs |

**2025–2026:** Terraform-style apply; migrations already idempotent with `IF NOT EXISTS`.

## Patterns & Decision Matrix

| Operation | Pattern |
|-----------|---------|
| Insert row | `INSERT ... ON CONFLICT DO NOTHING` |
| File copy | Check hash or mtime |

## Code Examples

```bash
flock -n /var/lock/myjob.lock -c '/usr/local/bin/myjob.sh'
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Append-only log without rotation | Disk full |

## Deep Dive Sources

- [Martin Fowler — Idempotent Receiver](https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html)
