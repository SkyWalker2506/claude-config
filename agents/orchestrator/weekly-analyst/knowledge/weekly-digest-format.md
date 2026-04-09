---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Weekly Digest Format

## Quick Reference
| Kavram | Not |
|--------|-----|
| Temel kullanım | Bu konu weekly-digest-format bağlamında |
| Risk | Onaysız stratejik veya prod kararı |

## Patterns & Decision Matrix
| Senaryo | Öneri |
|---------|-------|
| Düşük risk | Standart playbook + kısa gate |
| Yüksek risk | A1/A0 escalation, geri alma planı |

## Code Examples
```text
[WEEKLY] agent-id=X | gate=checklist | evidence=log/ref
```

## Anti-Patterns
- Knowledge'ı görev bağlamına uyarlamadan kopyalamak.
- Ölçüm ve kayıt olmadan karar vermek.

## Deep Dive Sources
- [Internal dispatch](https://example.com/docs) — registry ve katman sözleşmeleri
- [Runbooks](https://example.com/ref) — operasyonel
- [Postmortems](https://example.com/wiki) — örnekler
