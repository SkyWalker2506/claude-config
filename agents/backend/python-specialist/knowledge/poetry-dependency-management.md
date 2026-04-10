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

## Patterns & Decision Matrix

| Durum | Komut / ayar |
|-------|----------------|
| Kütüphane yayını | Semver üst sınır |
| Uygulama | Lock commit + `poetry install --sync` |

## Code Examples

```bash
poetry add httpx@^0.27
poetry install --sync
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Lock dosyasını commit etmeme | Prod drift |
| Üst sınır * açık | Breaking sürpriz |

## Deep Dive Sources

- [Poetry — Documentation](https://python-poetry.org/docs/)
