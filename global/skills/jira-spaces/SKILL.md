---
name: jira-spaces
description: "Jira'daki tüm projeleri açık task sayısıyla listele. Triggers: jira-spaces, jira projeleri, proje listesi, hangi projeler var, spaces."
argument-hint: "[]"
---

# /jira-spaces — Jira Proje Listesi

`mcp__atlassian__getVisibleJiraProjects` ile tüm projeleri çek, her biri için açık task sayısını al, tablo göster.

## Akış

1. Tüm projeleri çek
2. Her proje için: `project = {KEY} AND status != Done` JQL ile açık task sayısı al
3. Açık task sayısına göre sırala (çok → az), 0 olanlar en alta

## Çıktı

```
| Proje           | Key  | Açık |
|-----------------|------|------|
| Vocab           | VOC  | 294  |
| ApApp           | AC   | 123  |
| ...             | ...  | ...  |
```

## Kurallar
- Max 10 tool call
- 0 açık task'lı projeler en alta

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
