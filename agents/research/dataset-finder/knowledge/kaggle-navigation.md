---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Kaggle Navigation

## Quick Reference

| Alan | İpucu |
|------|-------|
| Datasets arama | Etiket + lisans filtresi |
| Notebook | Veri keşfi için fork |
| Discussions | bilinen sorunlar |
| API | `kaggle datasets download` |

## Patterns & Decision Matrix

| Hedef | Yol |
|-------|-----|
| Tabular | Competitions + Datasets |
| CV | örnek boyut + etiket formatı kontrolü |

## Code Examples

```bash
kaggle datasets download -d user/dataset-name
```

## Anti-Patterns

- Yarış verisini üretim eğitiminde lisans izni olmadan kullanma.

## Deep Dive Sources

- [Kaggle API docs](https://github.com/Kaggle/kaggle-api/wiki)
