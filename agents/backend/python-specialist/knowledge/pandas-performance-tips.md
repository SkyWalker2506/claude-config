---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Pandas Performance Tips

## Quick Reference

| Technique | Benefit |
|-----------|---------|
| **Vectorization** | Avoid Python loops |
| **Categorical dtypes** | Memory + speed |
| **`eval/query`** | Some expr faster |
| **Chunked read** | `read_csv(chunksize=)` |

**2025–2026:** PyArrow backend (`dtype_backend="pyarrow"`) where supported.

## Patterns & Decision Matrix

| Teknik | Ne zaman |
|--------|----------|
| `category` | Düşük kardinalite string |
| `observed=True` | Seyrek kategoriler |
| Chunked read | RAM sınırı |

## Code Examples

```python
df["cat"] = df["cat"].astype("category")
df.groupby("region", observed=True)["sales"].sum()
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| `iterrows()` for big DF | Slow |

## Deep Dive Sources

- [Pandas — Performance](https://pandas.pydata.org/docs/user_guide/enhancingperf.html)
