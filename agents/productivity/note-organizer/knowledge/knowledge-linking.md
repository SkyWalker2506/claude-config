---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Knowledge Linking

## Quick Reference

**Link türleri:** yapısal (MOC → alt not), referans (kaynak → özet), temporal (günlük → proje). **Zettel UID:** `202604091030` gibi zaman tabanlı veya `prefix-sequential`.

| Bağ türü | Anlam |
|----------|-------|
| `supports` | Kanıt / kaynak |
| `contradicts` | Alternatif görüş |
| `next_step` | İş akışı |

```text
Kural: yeni not en az 1 mevcut nota bağlanana kadar "orphan" sayılır
```

## Patterns & Decision Matrix

| Graf stratejisi | Artı | Eksi |
|-----------------|------|------|
| Hub-and-spoke (MOC) | Keşif kolay | Hub şişebilir |
| Mesh (çok link) | Zengin | Bakım maliyeti |
| Sıralı zincir | Hikâye | Geri dönüş zor |

**K7 (Knowledge Base Agent) ile ayrım:** L4 kişisel vault düzeni; K7 kurumsal RAG ve vektör indeks.

## Code Examples

**Markdown bağlantı bloğu:**

```markdown
See also: [[MOC API Design]] · relates to [[ADR-004-rest-versioning]]
Sources: supports [[ref-fielding-dissertation]]
```

**Basit orphan raporu (grep):**

```bash
cd ~/Vault && rg -l '^#' *.md | sort > all.txt
rg -o '\[\[([^\]|]+)' *.md | sed 's/.*\[\[//' | sort -u > linked.txt
comm -23 all.txt linked.txt  # yaklaşık orphan tespiti
```

**JSON-LD düşünsel (kurumsal entegrasyon):**

```json
{
  "@id": "note:20260409-api-limits",
  "related": [{ "@id": "note:adr-004", "relation": "supports" }]
}
```

## Anti-Patterns

- **Sadece geri link yok:** İki yönlü farkında ol; en azından "backlink" panelinde görünsün.
- **Kırık `[[Yanlış İsim]]`:** Not oluşturmadan link verme alışkanlığı.
- **Her nota her not:** Link spam; sadece anlamlı kenarlar.
- **Telif içeriğini tam kopyalayıp link vermemek:** Özet + kaynak URL zorunlu.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Nick Milo — Linking Your Thinking](https://www.linkingyourthinking.com/) — bağlantı felsefesi
- [W3C — OWL primer](https://www.w3.org/TR/owl-primer/) — ilişki tipleri (ileri düzey)
- [Obsidian — Graph view](https://help.obsidian.md/Plugins/Graph+view) — görselleştirme
