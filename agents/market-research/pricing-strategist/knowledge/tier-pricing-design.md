---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# Tier Pricing Design

## Quick Reference

| Tier sayısı | Ne zaman |
|-------------|----------|
| **2** | Tek ürün, basit self-serve |
| **3 (GBB)** | Çoğu SaaS — “Good / Better / Best” |
| **4+** | Enterprise, eklenti modülleri, bölge varyantı |

**Kural:** Her tier net “kim için” ve “hangi limit” ile tanımlanır; özellik listesi şişmesin.

## Patterns & Decision Matrix

| Boyut | Örnek limitler |
|-------|----------------|
| Kullanım | API çağrısı, GB, işlem |
| Rol | Admin sayısı, SSO |
| Destek | SLA, kanal |

### Good-Better-Best ipuçları

- **Better**’ı hedef marj ve hacim merkezi yap (çoğu zaman)
- **Good**: erişilebilir giriş — ama “çöp tier” değil (destek maliyeti)
- **Best / Enterprise**: “Talk to sales” — özel şartlar

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| İki tier’da aynı özellik | Tier anlamsız |
| Sınırsız her şey orta pakette | Marj ölür |
| İsimler belirsiz (“Pro” vs “Business”) | Müşteri yanlış seçer |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Price Intelligently — SaaS pricing](https://www.priceintelligently.com/) — tier ve paketleme (ProfitWell)
- [OpenView — PLG pricing](https://openviewpartners.com/) — self-serve katmanları
- [Simon-Kucher — Good-Better-Best](https://www.simon-kucher.com/en/) — danışmanlık çerçevesi
- [SaaStr — packaging](https://www.saastr.com/) — pratik örnekler
