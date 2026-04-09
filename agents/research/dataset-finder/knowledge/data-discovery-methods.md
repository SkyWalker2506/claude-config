---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Data Discovery Methods

## Quick Reference

| Yöntem | Ne zaman |
|--------|----------|
| Keyword + metadata | İlk tarama |
| Schema similarity | Benzer tablo arama |
| Lineage graph | Downstream etki |
| Profiling | Dağılım ve eksik değer |

## Patterns & Decision Matrix

| Soru | Araç |
|------|------|
| “Bu metrik nereden geliyor?” | Lineage |
| “Hangi kolonlar PII?” | Profiler + sözlük |

## Code Examples

```text
[DISCOVER] domain=sales | sensitivity=high | sources=[warehouse, lake] | owner_tag required
```

## Anti-Patterns

- Shadow IT veri setlerini kayıt dışı kullanma.

## Deep Dive Sources

- [Open Lineage](https://openlineage.io/)
- [Amundsen / DataHub](https://datahubproject.io/) — katalog
