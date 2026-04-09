---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Beta Package Evaluation

## Quick Reference

| Kontrol | Soru |
|---------|------|
| experimental / preview | API stabil mi? |
| Bağımlılık | Diğer preview zinciri |
| CI | Editör sürümü sabitle |

## Patterns & Decision Matrix

| Risk | Mitigation |
|------|------------|
| Yüksek | Ayrı branch + feature flag |
| Düşük | Küçük PoC sahnesi |

## Code Examples

```text
[PREVIEW] pkg=com.unity.x@3.0.0-pre | breaking=[API_A] | rollback=previous_minor
```

## Anti-Patterns

- Preview paketi ana prod dalına doğrudan merge.

## Deep Dive Sources

- [Package lifecycle](https://docs.unity3d.com/Manual/upm-lifecycle.html)
