---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Integration Complexity

## Quick Reference

| Seviye | İşaret |
|--------|--------|
| Düşük | Drop-in prefab, örnek sahne |
| Orta | Namespace + API wiring |
| Yüksek | Mevcut mimariyle çakışma |

## Patterns & Decision Matrix

| Süre | Aksiyon |
|------|---------|
| <4h | Genelde kabul |
| >2 gün | Spike + POC |

## Code Examples

```text
[INTEGRATION] effort_h=8 | deps=[input,addressables] | conflicts=none|render_pipeline
```

## Anti-Patterns

- Entegrasyonu sprint son gününe bırakmak.

## Deep Dive Sources

- Unity forums / asset reviews
