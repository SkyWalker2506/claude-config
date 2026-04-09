---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Output Format Guide

## Quick Reference
| Kavram | Not |
|--------|-----|
| Temel kullanım | Bu konu output-format-guide bağlamında |
| Risk | Doğrulanmadan prod/build'e taşıma |

## Patterns & Decision Matrix
| Senaryo | Öneri |
|---------|-------|
| Düşük risk | Standart desen + küçük doğrulama |
| Yüksek risk | Aşamalı rollout, geri alma planı |

## Code Examples
```text
[RENDER] resource=example | verify=checklist
```

## Anti-Patterns
- Jenerik şablonu görev bağlamına uyarlamadan kopyalamak.
- Ölçüm ve log olmadan değişiklik yapmak.

## Deep Dive Sources
- [Official docs](https://example.com/docs) — sürüm notlarına göre güncelle
- [Reference](https://example.com/ref) — bağlamsal
- [Community](https://example.com/wiki) — doğrula
