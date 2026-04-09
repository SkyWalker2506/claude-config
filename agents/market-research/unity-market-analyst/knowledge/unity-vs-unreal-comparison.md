---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Unity vs Unreal Comparison

## Quick Reference

| Boyut | Unity | Unreal |
|-------|-------|--------|
| Hedef | geniş platform, mobil güçlü | AAA görsel, Nanite |
| Dil | C# | C++ / Blueprint |
| Lisans | runtime ücret modeli (sürüme bağlı) | royalty eşiği |

## Patterns & Decision Matrix

| Takım | Öneri |
|-------|-------|
| Küçük, mobil | Unity sık |
| PC konsol görsel | Unreal tartışılır |

## Code Examples

```text
[COMPARE] project=… | platforms=[mobile,pc] | team_csharp_strong=true → lean Unity
```

## Anti-Patterns

- 2018 karşılaştırma tablosunu güncel sanmak.

## Deep Dive Sources

- Resmi Unity ve Epic lisans sayfaları
