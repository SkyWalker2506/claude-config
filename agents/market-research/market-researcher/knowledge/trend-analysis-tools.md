---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Trend Analysis Tools

## Quick Reference

| Sinyal tipi | Araç / kaynak | Okuma |
|-------------|----------------|-------|
| **Arama talebi** | Google Trends, Bing | Mevsimsellik ayır |
| **Kamu verisi** | Eurostat, BLS, FRED | Makro bağlam |
| **Sosyal dinleme** | Reddit, X/Twitter API, LinkedIn | Gürültü yüksek — örnekleme |
| **Yatırım / M&A** | Crunchbase, PitchBook özeti | Sektör ısı haritası |
| **ArXiv / papers** | cs.AI, HCI | Erken teknik sinyal |

**Trend vs. moda:** 12+ ay tekrarlanan yapı + en az iki bağımsız sinyal (ör. arama + iş ilanı).

## Patterns & Decision Matrix

| Aşama | Çıktı |
|-------|--------|
| 1. Hipotez | “X teknolojisi Y segmentinde Z nedeniyle büyüyecek” |
| 2. Ölçüm | Zaman serisi (haftalık/aylık), normalize edilmiş indeks |
| 3. Çapraz doğrulama | Farklı coğrafya veya kanal |
| 4. Senaryo | Devam / yavaşlama / tersine dönme |

### Kırmızı bayraklar

- Tek bir viral habere dayalı “sonsuz büyüme” projeksiyonu
- COVID vb. tek seferlik şokla karışmış veri seti (adjust et)

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| “AI” kelimesini tüm bağlamdan koparmak | Sahte pozitif trend |
| Sadece ABD verisiyle global iddia | Coğrafya hatası |
| Vendor whitepaper tek kaynak | Satış bias’ı |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Trends — Help](https://support.google.com/trends/) — metod ve sınırlar
- [FRED Economic Data](https://fred.stlouisfed.org/) — zaman serisi
- [Pew Research — Internet & Tech](https://www.pewresearch.org/topic/internet-technology/) — tüketici davranışı
- [WIPO — Global Innovation Index](https://www.wipo.int/global_innovation_index/) — ülke bazlı yenilik
- [Our World in Data](https://ourworldindata.org/) — uzun dönem bağlamlar
