---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# FastAPI Project Structure

## Quick Reference

| Layer | Folder |
|-------|--------|
| **Routers** | `api/routes/` — `APIRouter` per domain |
| **Services** | business logic |
| **Schemas** | Pydantic v2 models |
| **Deps** | `Depends()` DB session |

**2025–2026:** Pydantic v2 (`model_validate`); lifespan context for startup/shutdown.

## Code Examples

```python
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/items", tags=["items"])

@router.get("/{item_id}")
def read_item(item_id: int, db=Depends(get_db)):
    ...
```

## Deep Dive Sources

- [FastAPI — Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Pydantic V2 Migration](https://docs.pydantic.dev/latest/migration/)
