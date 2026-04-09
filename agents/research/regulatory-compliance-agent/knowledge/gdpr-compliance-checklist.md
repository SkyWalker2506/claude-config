---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# GDPR Compliance Checklist

## Quick Reference

| Alan | Kontrol |
|------|---------|
| Lawful basis | En az bir: consent, contract, legitimate interest dokümante |
| Data minimization | Alan listesi + retention |
| Rights | Erişim, silme, taşınabilirlik süreleri |
| DPA | İşleyen (processor) sözleşmesi |
| Breach | 72s içi bildirim prosedürü |

## Patterns & Decision Matrix

| Veri türü | Ek önlem |
|-----------|----------|
| Özel kategoriler | Açık rıza veya yasal istisna |
| Çocuk | Yaş doğrulama + ebeveyn |

## Code Examples

```text
[GDPR_REVIEW] system=crm | lawful_basis=contract | DPA_signed=true | subprocessors=[…]
```

## Anti-Patterns

- “KVKK için yeter” diyerek GDPR’ı atlama (scope farklı).
- Consent banner’ı tek başına compliance sanma.

## Deep Dive Sources

- [GDPR full text](https://gdpr-info.eu/) — Madde 5–49
- [ICO guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
