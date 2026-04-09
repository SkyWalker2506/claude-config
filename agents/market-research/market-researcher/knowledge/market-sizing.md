---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Market Sizing

## Quick Reference

| Yaklaşım | Formül mantığı | Güven |
|----------|------------------|-------|
| **Top-down** | Endüstri raporu TAM × pay varsayımı | Hızlı; kaynak kalitesine bağlı |
| **Bottom-up** | Satılabilir birim × ortalama fiyat | Operasyonel olarak savunulabilir |
| **Value pool** | Müşteri bütçesinden pay | B2B enterprise için uygun |

**Tutarlılık testi:** Bottom-up SOM ≤ SAM ≤ TAM; en az iki yöntem farkı %50’yi geçmemeli (geçerse varsayımları aç.

## Patterns & Decision Matrix

| Segment | Birim tanımı örneği |
|---------|---------------------|
| SaaS | Lisanslı koltuk veya MRR |
| Marketplace | GMV veya komisyon geliri (net vs. brüt netleştir) |
| Donanım | Sevkiyat adedi × ASP |
| Reklam | DAU × gösterim × CPM / fill |

### Varsayımlar tablosu (şeffaflık)

| # | Varsayım | Kaynak | Hassasiyet (±%) |
|---|----------|--------|-----------------|
| 1 | CAGR | Statista / şirket raporu | |
| 2 | Penetrasyon yıl 5 | Karşılaştırmalı kategori | |

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| “Servis edilebilir” tanımı geniş | SAM şişkin |
| Kur dövizini karıştırmak | Yanlış USD toplamı |
| Churn’ü büyümeden düşmek | SOM fazla iyimser |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Statista — Market outlook](https://www.statista.com/outlook/) — endüstri büyüklükleri (lisanslı veri; metod notlarına bak)
- [IBISWorld — methodology](https://www.ibisworld.com/) — sektör tanımları
- [World Bank — GDP / exchange](https://data.worldbank.org/) — makro ve kur
- [US Census — business data](https://www.census.gov/programs-surveys/cbp.html) — ABD işletme sayıları (B2B alt sınır)
- [Eurostat — Structural business](https://ec.europa.eu/eurostat) — AB işletme istatistikleri
