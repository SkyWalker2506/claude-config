---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Fact-Checking Methods

## Quick Reference

| Method | Ne zaman | Çıktı |
|--------|----------|-------|
| **Lateral read** | Şüpheli site | Aynı iddiayı bağımsız kaynakta ara |
| **Primary trace** | İstatistik, alıntı | Orijinal tabloya / paper’a git |
| **Reverse image** | Görsel iddia | İlk yayın tarihi ve bağlam |
| **Consensus check** | Bilimsel iddia | İki review veya survey meta-analiz |

```text
Durum etiketi: VERIFIED | PARTIAL | CONTRADICTED | UNKNOWN
```

## Patterns & Decision Matrix

| Durum | Aksiyon |
|-------|---------|
| Tek kaynak, çok paylaşılmış | “Viral tekrar” — birincil kaynak bul |
| Sayısal iddia | Birim ve yıl eşleşmesi zorunlu |
| “Yakında” / gelecek tarih | Resmi roadmap veya press release |
| Çelişen kaynaklar | Güç sıralaması + tarih (yeni kanıt öncelikli) |

**Karar:** Çelişki çözülene kadar raporda her iki görüşü “disputed” ile göster.

## Code Examples

**Fact satırı şablonu:**

```text
[FACT id=fc-001]
claim: "…"
status: PARTIAL
evidence:
  - {url, tier:T1, supports:partial}
  - {url, tier:T2, supports:contradicts}
notes: …
```

## Anti-Patterns

- **Snippet’ten sayı kopyalamak:** Tablodaki bağlam (ör. “YoY”) kaybolur.
- **“Experts agree” ile kapatmak:** İsim veya literatür ver.
- **Onay eğilimi:** Zaten inandığın sonucu destekleyen kaynakları seçme.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [IFCN Code of Principles](https://ifcncodeofprinciples.poynter.org/) — profesyonel doğrulama standartları
- [Semantic Scholar](https://www.semanticscholar.org/) — akademik iz sürme
