---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Decision Framework

## Quick Reference
| Kavram | Not |
|--------|-----|
| Temel kullanım | Bu konu decision-framework bağlamında |
| Risk | Veri/konfigürasyon doğrulanmadan prod'a taşıma |

## Patterns & Decision Matrix
| Senaryo | Öneri |
|---------|-------|
| Düşük risk | Standart desen + küçük doğrulama |
| Yüksek risk | Aşamalı rollout, geri alma planı |

## Code Examples
```text
[WAITIN] resource=example | verify=checklist
```

## Anti-Patterns
- Jenerik şablonu görev bağlamına uyarlamadan kopyalamak.
- Ölçüm ve log olmadan değişiklik yapmak.

## Deep Dive Sources
- [Official docs](https://example.com/docs) — sürüm notlarına göre güncelle
- [Reference architecture](https://example.com/ref) — bağlamsal
- [Community patterns](https://example.com/wiki) — dikkatli doğrula
