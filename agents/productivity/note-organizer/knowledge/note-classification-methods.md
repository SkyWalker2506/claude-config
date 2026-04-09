---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Note Classification Methods

## Quick Reference

**Boyutlar:** tür (meeting / idea / reference / project), yaşam döngüsü (fikir → taslak → arşiv), güven (kişisel / ekip / public). **Parçalama:** tek not = tek ana fikir (400–800 kelime üstü → böl).

| Yöntem | Ne zaman |
|--------|----------|
| Klasör önce (PARA) | Aksiyon odaklı bilgi işi |
| Etiket önce (Zettelkasten) | Araştırma ve bağlantı |
| MOC (Maps of Content) | Geniş konu alanları |

```text
PARA: Projects / Areas / Resources / Archives — sık gözden geçirme periyodu: haftalık
```

## Patterns & Decision Matrix

| Sistem | Artı | Eksi |
|--------|------|------|
| PARA | Net iş akışı | "Area" tanımı bulanık kalabilir |
| Johnny.Decimal | Rigid ID, aranabilir | Kurulum maliyeti |
| Zettelkasten | Güçlü link grafı | Disiplin gerekir |

**Karar ağacı:** İş çıktısı mı? → PARA. Akademik sentez mi? → Zettel UID + link.

## Code Examples

**YAML frontmatter (Obsidian uyumlu):**

```yaml
---
type: reference
status: seed
topics: [api-design, rest]
created: 2026-04-09
source_url: https://example.com/doc
confidence: medium
---
```

**Basit sınıflandırma script (dosya adı önerisi):**

```bash
# YYYY-MM-DD-slug.md
slug=$(echo "API Rate Limits Discussion" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
echo "2026-04-09-$slug.md"
```

**PARA hedef klasör eşlemesi:**

```text
contains_actionable_deadline -> 1-Projects/active-project-x/
evergreen_howto -> 2-Areas/engineering/
external_pdf_summary -> 3-Resources/references/
completed_project_notes -> 4-Archive/2026/
```

## Anti-Patterns

- **Tek "Misc" klasörü şişmesi:** Misc max 10 not; üstüne haftalık ayrıştır.
- **Dosya adında vakit kaybı:** İsim net değilse frontmatter `title` + H1 düzelt.
- **Aynı notu iki yerde kopyalamak:** Bir kanonik not + diğerlerinden link.
- **Sınıflandırma için sınıflandırma:** 5 dk’dan uzun sürdüyse yeterince iyi de.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Tiago Forte — PARA method](https://fortelabs.com/blog/para/) — dört kutu metodu
- [Ahrens — How to Take Smart Notes](https://www.soenkeahrens.de/en/take-smart-notes) — Zettelkasten özü
- [Johnny.Decimal](https://johnnydecimal.com/) — numaralı sistem
