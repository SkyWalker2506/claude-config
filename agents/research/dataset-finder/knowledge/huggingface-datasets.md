---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Hugging Face Datasets

## Quick Reference

| Kavram | Açıklama |
|--------|----------|
| Dataset card | Lisans, splits, biases |
| `load_dataset` | Streaming vs map-style |
| Config | Çoklu alt-veri kümeleri |

## Patterns & Decision Matrix

| Boyut | Öneri |
|-------|-------|
| Büyük | `streaming=True` |
| Küçük | Tam önbellek |

## Code Examples

```python
from datasets import load_dataset
ds = load_dataset("imdb", split="train[:1%]")
```

## Anti-Patterns

- Kartı okumadan üretime veri bağlama (bias / lisans).

## Deep Dive Sources

- [HF Datasets docs](https://huggingface.co/docs/datasets/)
