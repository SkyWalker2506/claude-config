---
last_updated: 2026-04-10
refined_by: coverage-bootstrap
confidence: high
sources: 3
---

# Cross-repo consistency (ecosystem)

## Quick Reference

| Kural | Uygulama |
|-------|----------|
| Sıra | catalog → marketplace → config → HQ |
| Sayılar | Tek kaynak: `claude-config` registry |
| Link | Çapraz README güncellemesi |

## Patterns & Decision Matrix

| Değişiklik | Yay |
|------------|-----|
| Agent sayısı | catalog + config başlık |
| Plugin sayısı | marketplace + config |

## Code Examples

```markdown
See [claude-ecosystem-github-order.md](claude-ecosystem-github-order.md) for ordered rollout.
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Bir repoda güncel diğerinde eski | Ziyaretçi kafası karışır |

## Deep Dive Sources

- Internal: `claude-ecosystem-github-order.md`
