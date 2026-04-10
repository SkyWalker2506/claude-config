---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Market Analysis Framework

## Quick Reference

| Katman | Soru | Çıktı |
|--------|------|--------|
| **TAM** | Teorik üst limit (tüm talep) | USD veya birim |
| **SAM** | Hizmet verilebilir segment | Coğrafya, segment filtresi |
| **SOM** | 3–5 yıl içinde yakalanabilir pay | Gerçekçi penetrasyon |
| **PESTEL** | Politik, ekonomik, sosyal, teknoloji, çevre, hukuk | Risk / fırsat |
| **Porter 5** | Rekabet yoğunluğu | Marj baskısı özeti |

**Kullanım sırası:** Problem tanımı → müşteri işi (JTBD) → PESTEL tarama → Porter → TAM/SAM/SOM → senaryo (base/upside/downside).

## Patterns & Decision Matrix

| Durum | Öncelik |
|-------|---------|
| Yeni kategori, veri seyrek | TAM’ı top-down + bottom-up ile çapraz doğrula |
| B2B, uzun satış döngüsü | SAM’ı ICP + ACV ile sınırla |
| Regülasyon riski yüksek | PESTEL’de hukuk satırını önce doldur |

### Tek sayfa özet şablonu

1. **Pazar tanımı:** Ürün + coğrafya + müşteri tipi (tek cümle).
2. **Büyüme sürücüleri:** 3 madde (talep, teknoloji, düzenleme).
3. **Kısıtlar:** 3 madde (rekabet, maliyet, dağıtım).
4. **Önerilen SOM varsayımı:** Kaynak (anket, rapor, iç veri).

## Code Examples

### Örnek: TAM/SAM/SOM tablosu

```markdown
| | Definition | Value | Notes |
|---|------------|-------|-------|
| TAM | All firms with BI spend > $10k/yr | $4.2B | Top-down |
| SAM | Product-led SaaS in NA+EU | $620M | Bottom-up accounts |
| SOM | Win 2% SAM in 36 mo | $12.4M | Assumes 18 mo CAC payback |
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| TAM = “dünya nüfusu × fiyat” | Şişirilmiş yatırımcı beklentisi |
| Tek kaynaklı CAGR | Tek senaryoya kilitlenme |
| Rakipsiz pazar iddiası | SAM kontrolü atlanmış demektir |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Harvard Business Review — Five Forces](https://hbr.org/1979/03/how-competitive-forces-shape-strategy) — Porter çerçevesi
- [OECD — Market definition](https://www.oecd.org/competition/) — rekabet ekonomisi bağlamı
- [McKinsey — Growth strategy](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance) — büyüme ve segmentasyon
- [CB Insights — Market sizing](https://www.cbinsights.com/research) — sektör raporları (örnek metodoloji)
- [Gartner — Hype Cycle](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle) — teknoloji benimseme eğrisi
