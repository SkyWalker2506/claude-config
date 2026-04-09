---
last_updated: 2026-04-09
confidence: high
sources: 4
---

# Technology Radar Method

## Quick Reference

| Halka (ThoughtWorks tarzı) | Anlam | Örnek yerleşim |
|----------------------------|-------|----------------|
| **Adopt** | Üretimde güvenle | Postgres, React |
| **Trial** | Pilot değer kanıtı | Yeni UI kit |
| **Assess** | Öğren, PoC | Deneysel DB |
| **Hold** | Yeni yatırım yok | Eski framework |

```text
Her öğe: ad | halka | risk | son_inceleme_tarihi | sahip_takim
```

## Patterns & Decision Matrix

| Veri kaynağı | Ağırlık |
|--------------|---------|
| Ekip içi postmortem | Yüksek |
| Topluluk (GitHub issues) | Orta |
| Haber / HN | Düşük — doğrulama gerekir |

**Karar:** “Adopt” için üretim örneği veya güçlü operasyonel metrik şart.

## Code Examples

**Radar satırı:**

```text
[RADAR] item=… | ring=Trial | evidence: [link1, internal_doc2] | revisit: Q3
```

## Anti-Patterns

- **Moda göre halka:** Popülerlik tek başına adopt değil.
- **Radar’ı hiç güncellememek:** Tarih ve sahip alanları boşsa güvenilmez.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [ThoughtWorks Technology Radar methodology](https://www.thoughtworks.com/radar) — halka felsefesi
- [Gartner Hype Cycle](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle) — pazar döngüsü (ücretli raporlar — özet kullan)
