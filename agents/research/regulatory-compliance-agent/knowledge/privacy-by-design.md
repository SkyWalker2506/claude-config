---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Privacy by Design

## Quick Reference

| İlke | Uygulama |
|------|----------|
| Proactive | Varsayılan: toplama yok |
| Privacy as default | Opt-in gerçekten seçmeli |
| Full lifecycle | Silme + anonimleştirme tasarımda |
| Visibility | Veri akış diyagramı |
| Respect for user | Açık UX, düşük sürtünme |

## Patterns & Decision Matrix

| Özellik | Soru |
|---------|------|
| Yeni alan | Gerçekten gerekli mi? |
| Analytics | Aggregate yeter mi? |

## Code Examples

```text
[DESIGN_REVIEW] feature=x | data_collected=[] | lawful=… | retention=… | user_controls=[export,delete]
```

## Anti-Patterns

- “Sonra ekleriz” anonimleştirme.
- Karanlık desenler (dark patterns) ile rıza.

## Deep Dive Sources

- [PbD 7 Principles — Ann Cavoukian](https://www.ipc.on.ca/wp-content/uploads/resources/7foundationalprinciples.pdf)
- [ICO PbD](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-by-design-and-default/)
