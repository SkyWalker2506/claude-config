---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Hype Cycle Assessment

## Quick Reference

| Faz | Belirti | Risk |
|-----|---------|------|
| **Peak of Inflated Expectations** | Çok vaat, az ölçüm | Erken taahhüt |
| **Trough of Disillusionment** | Soğuma, kötü basın | Fırsat (değer kalanı) |
| **Slope of Enlightenment** | Gerçek kullanım örnekleri | Hâlâ kırılgan |
| **Plateau of Productivity** | Standart araç | Düşük marj fark |

```text
Not: Gartner faz isimleri tescilli; rapor ücretli — genel çerçeve olarak kullan, kaynak belirt
```

## Patterns & Decision Matrix

| Soru | Cevap kaynağı |
|------|---------------|
| Vaat mi, ürün mü? | Çalışan referans müşteri |
| Tek vendor mı? | Kilitleme riski |
| Regülasyon | Özellikle AI / biyometri |

**Karar:** “Peak” aşamasında bütçe taahhüdü için PoC çıkış kriterleri yaz.

## Code Examples

**Değerlendirme satırı:**

```text
[HYPE] topic=… | phase_guess=trough | rationale: … | evidence: [case study, benchmark]
```

## Anti-Patterns

- **Hype cycle’ı kesin faz sanmak:** Niteliksel model; sayısal değil.
- **Basın başlığına göre faz:** Medya gecikmeli tepeyi gösterir.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Gartner Hype Cycle explained (public summaries)](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle)
- Tarihsel teknoloji analizleri — akademik ve endüstri raporları
