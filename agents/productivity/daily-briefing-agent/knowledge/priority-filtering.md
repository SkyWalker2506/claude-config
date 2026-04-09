---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Priority Filtering

## Quick Reference

**Girdi:** L1 öncelik skorları + kullanıcı sabit kuralları + deadline yakınlığı. **Çıktı:** Brifing’e giren en fazla N öğe (öneri: N=5 mail, N=7 görev).

| Filtre | Ağırlık örneği |
|--------|----------------|
| Deadline <24h | +30 |
| Bloklayıcı etiketi | +25 |
| Üst yönetici kaynaklı | +20 |

**Noise floor:** Skor < eşik → "Diğer 12 öğe — L1’de tam liste" dipnotu.

```text
hard_cap: briefing_items_total <= 25 lines printable
```

## Patterns & Decision Matrix

| Strateji | Açıklama |
|----------|----------|
| Top-K | En yüksek skorlu K öğe |
| MMR | Benzer öğeleri çeşitlendir (konu embedding) |
| Rotasyon | Dün gösterilen düşük skorlu bugün gösterilmez |

**Çatışma:** Takvim P0 ile mail P0 aynı saatte — brifingde tek satırda birleştirilmiş uyarı.

## Code Examples

**Öncelik birleşik skor:**

```text
final = 0.5 * L1_score + 0.3 * deadline_urgency + 0.2 * user_starred
```

**YAML kullanıcı politikası:**

```yaml
briefing_filters:
  mail:
    min_score_for_body: 60
    always_include_senders:
      - "ceo@company.com"
  tasks:
    include_status: ["In Progress", "Blocked"]
    max_items: 7
```

**Çıktı dipnotu:**

```text
... 12 lower-priority threads hidden — open L1 Email Summarizer for full triage.
```

## Anti-Patterns

- **Her şeyi gösterme:** Brifing özettir; tam liste başka agent.
- **Statik N:** Yoğun günlerde N’yi 1.2x artır (üst sınır ile).
- **Kullanıcı yıldızını yok sayma:** Manuel işaret her zaman bonus.
- **P3’ü asla göstermeme:** Bazen "quick win" moral için 1 düşük öncelik eklenebilir.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [RICE prioritization](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) — ürün önceliği (adaptasyon)
- [WSJF](https://scaledagileframework.com/wsjf/) — ağırlıklı kısa iş sıralaması
- [Attention economy — Hick’s law](https://lawsofux.com/hicks-law/) — seçenek sayısı ve bilişsel yük
