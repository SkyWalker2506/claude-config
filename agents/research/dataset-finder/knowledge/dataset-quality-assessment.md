---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Dataset Quality Assessment

## Quick Reference

| Boyut | Metrik |
|-------|--------|
| Tamamlık | Null oranı, zorunlu alan |
| Tutarlılık | Referential integrity |
| Güncellik | Son güncelleme SLA |
| Temsil | Sınıf dengesizliği, coğrafi sapma |

## Patterns & Decision Matrix

| Kullanım | Minimum bar |
|----------|-------------|
| Prototip | Hızlı profil |
| Üretim | Great Expectations / dbt test |

## Code Examples

```yaml
expectations:
  - expect_column_values_to_not_be_null: [id]
  - expect_table_row_count_to_be_between: [1000, 1e9]
```

## Anti-Patterns

- Train/test leakage (zaman sırası bozuk).

## Deep Dive Sources

- [Great Expectations](https://greatexpectations.io/)
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
