---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Data Protection Patterns

## Quick Reference

| Pattern | Ne işe yarar |
|---------|--------------|
| Pseudonymization | Kimlik anahtarını ayır |
| Encryption at rest | Disk / DB şifreleme |
| TLS in transit | Tüm API ve kullanıcı yüzeyi |
| RBAC + ABAC | Erişim modeli |
| Audit log | Kim neye erişti |

## Patterns & Decision Matrix

| Risk | Minimum |
|------|---------|
| Düşük | TLS + temel RBAC |
| Orta | Şifreli kolon + audit |
| Yüksek | HSM / tokenization + DLP |

## Code Examples

```sql
-- Pseudonym: ayrı tablo, join sadece yetkili rol
SELECT p.order_id, map.real_id FROM orders p
JOIN id_map map ON … WHERE current_user_has('pii_read');
```

## Anti-Patterns

- PII’yi log’da düz metin.
- “Şifreli yedek” yok sayılan restore testi.

## Deep Dive Sources

- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) — V2 Storage, V8 Data protection
