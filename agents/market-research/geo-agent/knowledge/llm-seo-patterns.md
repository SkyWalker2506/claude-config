---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# LLM SEO Patterns

## Quick Reference

| Pattern | Açıklama |
|---------|----------|
| **Inverted pyramid** | En önemli cevap ilk paragrafta |
| **Atomic facts** | Her cümle tek iddia — kolay alıntı |
| **Disambiguation** | “X (ürün) vs x (değişken)” gibi çakışmaları çöz |
| **Citation-friendly** | Başlıklar, kalıcı URL, bölüm anchor’ları |
| **Versioning** | “v2’de değişti” notları — eski model çıktıları için |

**Not:** Ticari LLM’lerin eğitim verisi ve güncellik farklı — **tek strateji her yüzeyde işe yaramaz**.

## Patterns & Decision Matrix

| İçerik | LLM dostu yapı |
|--------|------------------|
| API dokü | Örnek istek/yanıt blokları, hata kodları tablosu |
| Fiyatlandırma | Tablo + footnote (koşullar) |
| Karşılaştırma | “Seç şu eğer…” karar ağacı |

### Risk

| Risk | Mitigasyon |
|------|------------|
| Yanlış rakip bilgisi | Birincil kaynak linki |
| Uydurma istatistik | Sadece kaynaklı rakamlar |

## Code Examples

### Örnek: citation-dostu paragraf yapısı

```markdown
## What is [X]?
One-sentence definition. [Brand] provides [Y] for [ICP] ([source year]).

### Key capabilities
- Bullet with named feature + limitation when relevant
- Link to primary doc, not login wall
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Uzun giriş paragrafları | Alıntı kesilir veya yanlış özetlenir |
| Gizli “AI için” metin (font gizleme) | Spam olarak değerlendirilebilir |
| Her cevabı 500 kelime | Gürültü — öz ve net kazanır |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Perplexity — citations model](https://www.perplexity.ai/) — alıntılı cevap UX (ürün bağlamı)
- [Microsoft — Copilot consumer](https://www.microsoft.com/en-us/microsoft-copilot) — kaynak kartları davranışı
- [Google — AI Principles](https://ai.google/responsibility/principles/) — güvenilirlik beklentisi
- [NIST — AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — risk çerçevesi (kurumsal)
- [arXiv — RAG / retrieval](https://arxiv.org/list/cs.IR/recent) — altyapı literatürü
