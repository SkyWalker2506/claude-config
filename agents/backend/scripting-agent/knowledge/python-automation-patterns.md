---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Python Automation Patterns

## Quick Reference

| Topic | Practice |
|-------|----------|
| **CLI** | `argparse` or `typer` |
| **HTTP** | `httpx` / `requests` with timeouts |
| **Config** | Env + `pydantic-settings` |
| **Deps** | `pyproject.toml` + lock |

**2025–2026:** Type hints + `uv` for fast env; `ruff` for lint.

## Patterns & Decision Matrix

| Script | Structure |
|--------|-----------|
| Reusable | `if __name__ == "__main__"` + testable functions |

## Code Examples

```python
import httpx

def fetch(url: str, timeout: float = 30.0) -> str:
    with httpx.Client(timeout=timeout) as c:
        r = c.get(url)
        r.raise_for_status()
        return r.text
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| No timeout | Hangs forever |

## Deep Dive Sources

- [Python Packaging User Guide](https://packaging.python.org/)
- [Twelve-Factor — Config](https://12factor.net/config)
