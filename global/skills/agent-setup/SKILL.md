---
name: agent-setup
description: "Agent'i yeni Knowledge-First yapiya cevir — dizin olustur, AGENT.md yaz, knowledge/_index.md baslat, memory/ kur. Triggers: agent-setup, agent setup, agent kur, agent olustur."
argument-hint: "{agent-id | agent-name | --all}"
---

# /agent-setup — Knowledge-First Agent Setup

Mevcut tek-dosya agent tanimini yeni dizin yapisina cevirir.

## Yeni Yapi

```
agents/{category}/{agent-name}/
  AGENT.md                 # Kimlik + kurallar (L0)
  knowledge/
    _index.md              # Bilgi haritasi (L1)
    {topic}.md             # Alan bilgisi (L2 — lazy load)
  memory/
    sessions.md            # Karar + reasoning kaydi
    learnings.md           # Ogrenilenler
    refinements.md         # Refine gecmisi
```

## Process

1. **Agent'i bul**: ID veya isimle `agents/` altinda mevcut .md dosyasini bul
2. **Mevcut bilgiyi oku**: Eski .md'deki frontmatter + Amac + Kapsam + Escalation'i parse et
3. **Dizin olustur**: `agents/{category}/{agent-name}/` + `knowledge/` + `memory/`
4. **AGENT.md yaz**: Template'ten (`agents/_template/AGENT.md`) yeni formata cevir:
   - Frontmatter: eski alanlari tasi + yeni alanlar ekle (tier, models, refine_model)
   - Identity: eski Amac'tan yaz
   - Boundaries: eski Kapsam'dan Always/Never/Bridge cikar
   - Process: agent tipine uygun adimlar
   - When to Use / When NOT to Use: capability'lerden cikar
   - Red Flags: alan bazli tanimla
   - Verification: cikti tipine gore tanimla
   - Escalation: eski Escalation'dan tasi
5. **knowledge/_index.md olustur**: Agent'in alanina gore bos konu listesi hazirla (ileride doldurulacak)
6. **memory/ dosyalari olustur**: Template'ten kopyala
7. **Eski .md'yi sil**: Yeni dizin yapisi hazirlandi, eski dosya gereksiz
8. **Registry guncelle**: `config/agent-registry.json`'da yapisi guncelle (opsiyonel)

## When to Use
- Yeni agent olusturulurken
- Mevcut agent yeni Knowledge-First yapiya cevirilirken
- `/agent-setup --all` ile toplu gecis yapilirken

## When NOT to Use
- Agent zaten yeni yapida ise (dizin + AGENT.md mevcut)
- Sadece knowledge doldurmak icin (→ `/agent-sharpen` kullan)

## Red Flags
- Eski .md'deki bilgi kayboluyorsa — dur, kontrol et
- Agent ID cakismasi varsa — dur, registry'yi kontrol et
- Dizin zaten varsa — ustune yazma, kullaniciya sor

## Verification
- [ ] Dizin yapisi dogru olusturuldu (AGENT.md, knowledge/_index.md, memory/*.md)
- [ ] AGENT.md tum section'lari iceriyor
- [ ] Eski bilgi tasindi, kayip yok
- [ ] _index.md en az 3 bos konu iceriyor (doldurulmaya hazir)

## Tier Kurali

Tier = sadece model secimi. AGENT.md'de:
```yaml
models:
  senior: opus      # Kritik karar, mimari
  mid: sonnet       # Rutin is
  junior: haiku     # Basit gorev
refine_model: opus  # Knowledge dosya guncelleme her zaman opus
```

Ayni AGENT.md, ayni knowledge/, ayni memory/ — tier degistirmek sadece hangi modelin calisacagini belirler.

## Boundary Kurali

Her agent sadece kendi alaninda knowledge yazar. Bridge alanlari AGENT.md'de tanimlanir:
```markdown
### Bridge
- Frontend: sadece API contract noktasinda
- DevOps: sadece deployment architecture noktasinda
```

Agent bridge disinda bilgi yazmaya kalkarsa → Red Flag.
