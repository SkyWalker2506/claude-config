---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Poetry Dependency Management

## Quick Reference

| Command | Role |
|---------|------|
| `poetry add` | Dep + lock |
| `poetry install` | From lock |
| `poetry export` | requirements.txt for legacy |

**2025–2026:** `pyproject.toml` PEP 621; Poetry 2.x lock format.

## Code Examples

```bash
poetry add httpx@^0.27
poetry install --sync
```

## Deep Dive Sources

- [Poetry — Documentation](https://python-poetry.org/docs/)
