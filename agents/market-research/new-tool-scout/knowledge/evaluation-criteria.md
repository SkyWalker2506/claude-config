---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Evaluation Criteria

## Quick Reference

| Boyut | Örnek metrik |
|-------|--------------|
| Performans | latency p95 |
| Maliyet | $/1M token |
| Güvenilirlik | uptime SLA |
| Destek | dokümantasyon |

## Patterns & Decision Matrix

| Ağırlık | Bağlam |
|---------|--------|
| Regülasyon | veri rezidansı öncelik |
| Startup | hız + fiyat |

## Code Examples

```text
[SCORECARD] tool=… | weights={perf:0.3,cost:0.3,support:0.2,license:0.2} | winner=A
```

## Anti-Patterns

- Tek demo günü ile karar.

## Deep Dive Sources

- Gartner / Forrester metodolojileri (özet)
