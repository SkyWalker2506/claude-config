---
last_updated: 2026-04-09
confidence: high
sources: 4
---

# Web Search Strategies

## Quick Reference

| Tactic | Ne zaman | Sinyal / operatör |
|--------|----------|-------------------|
| **Exact phrase** | Özel terim, hata mesajı | `"quoted phrase"` |
| **Site filter** | Resmi doküman | `site:docs.example.com` |
| **Exclude noise** | Forum spam | `-site:pinterest.com` |
| **File type** | PDF, rapor | `filetype:pdf` |
| **Date window** | Breaking news / eski sürüm | Araç çubuğunda “Past year” veya `after:2024-01-01` (destekleyen motorlarda) |

```text
Query şablonu: [entity] + [action/problem] + (site:official OR filetype:pdf) -tutorial spam
```

## Patterns & Decision Matrix

| Yaklaşım | Artı | Eksi | Kullan |
|----------|------|------|--------|
| Geniş anahtar kelime | Çok sonuç | Gürültü | Keşif aşaması |
| Çoklu varyant sorgu | Kaçırılan eş anlamlılar | Zaman | Teknik terim belirsizse |
| İki dilli arama (EN+TR) | Yerel düzenlemeler | Çift doğrulama gerekir | KVKK, yerel hukuk |
| RSS / newsletter arşivi | Zaman serisi | Kurulum | Takip edilen proje |

**Karar:** Önce resmi kaynak + bir bağımsız ikincil kaynak; sonuç <5 ise sorguyu gevşet, >50 ise `site:` veya tırnak sıkılaştır.

## Code Examples

**Arama sonuçlarını yapılandırılmış özet (agent çıktı şablonu):**

```text
[SEARCH] topic=<kısa> | engine=… | queries_tried=3
Q1: "…" → top_domains: a.com, b.org (n=8)
Q2: site:docs… → hit=yes | snippet_match=high
Gap: … → next_query: …
```

**Programatik (örnek: arama API pseudo):**

```http
GET /search?q=urlencode("rust async cancellation")&limit=10&freshness=30d
```

## Anti-Patterns

- **Tek sorguya bağlı kalmak:** Aynı sonucu tekrar eden motorlar; en az iki query varyantı kullan.
- **İlk sayfada takılı kalmak:** Sayfa 2–3 ve “People also ask” ilişkili terimleri tara.
- **Clickbait başlığa güvenmek:** Snippet ≠ makale özeti; kaynağa git veya cache kontrol et.
- **Kişisel veriyi sorguya gömmek:** Log’da ham PII bırakma.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Search Operators (legacy reference)](https://support.google.com/websearch/answer/2466433) — operatör sözdizimi
- [Bing Advanced Search](https://help.bing.microsoft.com/#apex/abc9ebef-9f04-4ad2-8a6a-2308404f7379) — alternatif motor
- [DuckDuckGo !bangs](https://duckduckgo.com/bangs) — hızlı site yönlendirme
