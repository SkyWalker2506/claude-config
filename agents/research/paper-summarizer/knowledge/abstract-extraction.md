---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Abstract Extraction

## Quick Reference

| Abstract türü | Ayırt et | Çıkarılacak alan |
|---------------|----------|------------------|
| **Structured** | Başlıklar: Background, Methods… | Her blok tek cümle özet |
| **Unstructured** | Tek paragraf | İlk 2 cümle genelde problem+method |
| **Graphical** | Görsel özet | Metin gövde ile çapraz doğrula |

```text
Alanlar: problem | method | data | main_result | metric | limitation (varsa)
```

## Patterns & Decision Matrix

| Sorun | Çözüm |
|-------|-------|
| Belirsiz “we show” | Results’tan sayı çek |
| Çok disiplin | Alan jargonunu glossary’e ayır |
| Özet ≠ başlık uyumu | Title claim’i abstract’ta var mı kontrol et |

**Karar:** Sayısal iddia abstract’ta yoksa results’tan ekle ve `[from body]` işaretle.

## Code Examples

**Çıkarım şablonu:**

```text
[ABSTRACT PARSE]
problem: …
method: …
dataset_or_setting: …
key_numbers: [ … ]
claims_vs_results_aligned: yes | partial | no
```

## Anti-Patterns

- **Abstract cümlelerini yeniden yazmadan yapıştırmak:** Telif ve özet görevi için yeniden ifade et.
- **P-değerini bağlamdan koparmak:** Hipotez ve test türü olmadan raporlama.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [PubMed Abstract format](https://www.nlm.nih.gov/bsd/policy/abstract.html) — yapılandırılmış özet örnekleri
- [arXiv abstract guidelines](https://info.arxiv.org/help/submit_tex.html) — teknik makaleler
