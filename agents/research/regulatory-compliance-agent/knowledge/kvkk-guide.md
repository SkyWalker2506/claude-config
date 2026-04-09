---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# KVKK Guide

## Quick Reference

| Kavram | Not |
|--------|-----|
| Veri sorumlusu / işleyen | Rol ayrımı yazılı |
| Açık rıza | Belirli konu, bilgilendirilmiş, özgür irade |
| AYDINLATMA | 6698 m.10 — kim, neden, süre |
| VERBİS | Şartları kontrol et |
| Yurt dışı | Yeterlilik kararı veya TBK m.9 şartları |

## Patterns & Decision Matrix

| Aktarım | Adım |
|---------|------|
| AB | Yeterlilik |
| ABD | SCC + TIA gerekebilir |
| Diğer | İzin + güvence |

## Code Examples

```text
[KVKK] purpose=… | retention_days=… | abroad=false | verbis=exempt|registered
```

## Anti-Patterns

- GDPR metnini Türkiye’ye kopyala-yapıştır (hukuk farklı).
- İmza toplama ile “rıza” karıştırma.

## Deep Dive Sources

- [KVKK metni](https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6699) — resmi
- [KVKK Aydınlatma örneği](https://www.kvkk.gov.tr/) — KVkk rehberleri
