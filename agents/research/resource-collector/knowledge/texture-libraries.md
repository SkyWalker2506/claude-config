---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Texture Libraries

## Quick Reference

| Tür | Not |
|-----|-----|
| PBR set | Albedo, NRM, AO, roughness |
| Tileable | Seam test |
| Resolution | 1K / 2K / 4K bütçe |

## Patterns & Decision Matrix

| Stil | Seçim |
|------|-------|
| Realistic | Photo scan |
| Stylized | Hand-painted pack |

## Code Examples

```text
[PACK] name=… | maps=[albedo,normal,orm] | tile=true | license=CC0
```

## Anti-Patterns

- Farklı projelerden karışık PBR albedo tonu.

## Deep Dive Sources

- [Poly Haven](https://polyhaven.com/textures) — CC0
