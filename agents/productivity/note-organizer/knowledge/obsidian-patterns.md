---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Obsidian Patterns

## Quick Reference

**Vault yapısı:** `00-Inbox`, `10-Projects`, `20-Areas`, `30-Resources`, `90-Archive` + `_templates`. **Çekirdek eklentiler:** Daily notes, Templates, Backlinks, Graph view; opsiyonel Dataview, Templater.

| Dosya | Amaç |
|-------|------|
| `MOC Topic.md` | Harita — alt notlara indeks |
| `YYYY-MM-DD.md` | Günlük giriş |

**Link sözdizimi:** `[[Note Title]]` veya `[[Note Title|görünen metin]]`; blok referansı `[[Note#Heading]]`.

```text
Sync: Obsidian Sync veya Git; çakışma çözümü: dosya bazlı merge
```

## Patterns & Decision Matrix

| Senaryo | Öneri |
|---------|-------|
| Kod + dokümantasyon | Ayrı vault veya `attachments/` büyük ikili |
| Ekip notları | Git + PR review; `.obsidian` minimal paylaş |
| Mobil | Sync çözümü şart; büyük PDF’leri dışarıda tut |

**Templater vs core Templates:** Dinamik tarih/saat için Templater.

## Code Examples

**Templater başlık şablonu:**

```markdown
---
created: <% tp.file.creation_date() %>
tags: [type/seed]
---

# <% tp.file.title %>
```

**Dataview tablo (örnek sözdizimi):**

```dataview
TABLE file.mtime as updated
FROM "10-Projects"
WHERE contains(file.tags, "proj/active")
SORT file.mtime desc
LIMIT 10
```

**Callout kullanımı:**

```markdown
> [!warning] Kararsız
> Bu bölüm henüz gözden geçirilmedi.
```

## Anti-Patterns

- **Tüm eklentileri açmak:** Yükleme süresi ve taşınabilirlik kötüleşir.
- **Wikilink hedefi silinince kırık graf:** Periyodik orphan report.
- **Aynı vault’ta müşteri sırları:** Vault’u güven seviyesine göre ayır.
- **Binary’leri Git’e:** Git LFS veya dış depolama.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Obsidian Help](https://help.obsidian.md/) — resmi dokümantasyon
- [Obsidian Forum — best practices](https://forum.obsidian.md/) — topluluk kalıpları
- [YAML spec 1.2](https://yaml.org/spec/1.2/spec.html) — frontmatter doğruluğu
