---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# AI Visibility Optimization

## Quick Reference

| Boyut | Eylem |
|-------|--------|
| **Doğruluk** | Ürün adı, fiyat, desteklenen entegrasyonlar — tek doğruluk kaynağı (docs) |
| **Tazelik** | Changelog ve “Last updated” tarihi |
| **Otorite** | Uzman içerik, müşteri kanıtı, üçüncü taraf inceleme (şeffaf) |
| **Erişilebilirlik** | robots ile engellenmemiş public dokümantasyon |

**Hedef:** Model yanıtlarında **yanlış marka bilgisi** ve **halüsinasyon** riskini azaltmak — sıralama oyunundan farklı metrikler.

## Patterns & Decision Matrix

| İçerik tipi | AI için ipucu |
|-------------|----------------|
| FAQ | Soru başına kısa doğrudan cevap (40–80 kelime) |
| Karşılaştırma | Tablo + “hangi durumda hangisi” |
| Yasal | Net sorumluluk reddi ve bölge farkları |

### İzleme (pratik)

- Haftalık örnek prompt seti — marka, ürün, rakip karşılaştırma
- Yanıtları ekran görüntüsü / log ile arşivle (iç kullanım)

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Çelişen alt domain’ler | Model hangisini seçeceğini bilmez |
| PDF-only doküman | Metin çıkarımı kötü |
| Abartılı süperlative | Güven kaybı |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [OpenAI — GPT bot / crawling](https://platform.openai.com/docs) — bot ve kullanım politikaları (güncel)
- [Anthropic — Claude](https://www.anthropic.com/) — marka ve içerik politikaları
- [Common Crawl](https://commoncrawl.org/) — web korpus bağlamı
- [Google — AI disclosures](https://ai.google/responsibility/) — şeffaflık çerçevesi
