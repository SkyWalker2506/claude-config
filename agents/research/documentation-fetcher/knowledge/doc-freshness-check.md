---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Doc Freshness Check

## Quick Reference

| Sinyal | Taze | Bayat riski |
|--------|------|-------------|
| Sayfa “Last updated” | <90 gün veya sürümle uyumlu | >1 yıl, API değişmiş |
| Kod örneği import yolu | Mevcut paket yapısıyla eşleşir | Eski namespace |
| Deprecation banner | Üstte uyarı var | Yok ama kaynak kodda `@deprecated` |

```text
Skor: fresh | stale_suspect | confirmed_stale (kanıt ile)
```

## Patterns & Decision Matrix

| Doğrulama | Yöntem |
|-----------|--------|
| Örnek kod | Minimal repro veya resmi starter |
| Davranış | Release notes / diff |
| Alternatif | Issue araması “documentation outdated” |

**Karar:** `stale_suspect` ise kullanıcıya “kaynak kod / test örneği ile doğrula” yaz.

## Code Examples

**Freshness satırı:**

```text
[DOC FRESHNESS]
url: …
page_date: … | repo_tag: v…
match_lockfile: yes | no | n/a
verdict: fresh | stale_suspect
evidence: …
```

## Anti-Patterns

- **Copyright yılını güncellik sanmak:** Footer yılını tek başına kullanma.
- **Çeviri siteleri:** Orijinal İngilizce doc ile karşılaştır.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [MDN Browser compatibility](https://developer.mozilla.org/) — web API güncelliği referansı
- Proje `docs/` klasöründeki `last reviewed` meta verileri
