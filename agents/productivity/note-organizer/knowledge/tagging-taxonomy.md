---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Tagging Taxonomy

## Quick Reference

**Katmanlar:** (1) `type/` — `type/meeting`, `type/howto`; (2) `status/` — `status/triage`; (3) `topic/` — `topic/security`. Maksimum 5 etiket/not; çakışan etiketleri birleştir.

| Kural | Örnek |
|-------|-------|
| Namespace | `proj/acme` de `acme` değil |
| Tekil | `meeting` / `meetings` ikisi olmasın |
| Kontrollü sözlük | `tags.yml` ile doğrula |

```text
Yeni etiket ekleme eşiği: 3+ not aynı ihtiyacı gösterene kadar bekle
```

## Patterns & Decision Matrix

| Yaklaşım | Artı | Eksi |
|----------|------|------|
| Hiyerarşik `a/b` | Net | Uzun isimler |
| Düz + arama | Hızlı | Kirlilik |
| Hem klasör hem tag | Güçlü filtre | Senkron tutma zorluğu |

**Obsidian:** nested tags `#topic/api/rest` — sürüm 0.15+ ile çalışır.

## Code Examples

**tags.yml (sözlük — örnek):**

```yaml
version: 1
allowed_prefixes:
  - type
  - status
  - topic
  - proj
aliases:
  ml: machine-learning
  k8s: kubernetes
```

**Etiket doğrulama (Python):**

```python
ALLOWED = {"type/meeting", "type/howto", "status/draft"}
def validate(tags):
    return [t for t in tags if t in ALLOWED or t.startswith("proj/")]
```

**Graph sorgusu (Obsidian Dataview benzeri düşünce):**

```text
LIST FROM #type/meeting AND #proj/acme WHERE date >= 2026-04-01
```

## Anti-Patterns

- **Synonym cehennemi:** `bug`, `bugs`, `defect` — sözlükte tek canonical.
- **Etiket = klasör:** İkisi aynı bilgiyi taşımasın; biri birincil.
- **Çok geniş `important`:** Her şey önemli olunca hiçbiri değil.
- **Emoji-only tags:** Arama ve taşınabilirlik kötü; emoji sadece görünüm için.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Obsidian — Tags](https://help.obsidian.md/Editing+and+formatting/Tags) — nested tags
- [Dublin Core — subject element](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/) — kontrollü sözlük düşüncesi
- [SKOS — taxonomy patterns](https://www.w3.org/TR/skos-reference/) — kavram hiyerarşisi
