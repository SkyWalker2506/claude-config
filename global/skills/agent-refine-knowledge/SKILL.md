---
name: agent-refine-knowledge
description: "Agent'in AGENT.md ve knowledge dosyalarini opus ile review et, kaliteyi artir, gereksizi at, eksigi tamamla. Triggers: agent-refine, agent refine, agent rafine, bilgi rafine."
argument-hint: "{agent-id} [--scope agent|knowledge|all]"
---

# /agent-refine — Knowledge Refinement

Agent'in tum dosyalarini opus ile review eder, kaliteyi artir.

## Process

1. **Agent dizinini oku**: AGENT.md + knowledge/*.md + memory/*.md
2. **Kalite audit** (opus ile):
   - AGENT.md: Identity net mi? Boundaries keskin mi? Process adim adim mi?
   - knowledge/*.md: Bilgi guncel mi? Kaynakli mi? Tekrar var mi? Fazla genel mi?
   - memory/learnings.md: Knowledge'a tasinmasi gereken learning var mi?
3. **Aksiyonlar**:
   - Gereksiz/tekrar bilgiyi sil
   - Eksik section'lari tamamla
   - Belirsiz ifadeleri netlestir
   - Learnings → knowledge promosyonu yap (yeterli birikimde)
   - Boundary disina tasmis bilgiyi kaldir
4. **Refinement log**: `memory/refinements.md`'ye ne degisti, neden, kim (model) yapti
5. **Index guncelle**: Silinen/eklenen dosyalari `_index.md`'de yansit

## Refine Model Kurali

**Knowledge dosyalarini dusunup guncellemek HER ZAMAN opus ile yapilir.**
Bu dosyalar surekli kullanilacak — kalite kritik. Tier ne olursa olsun refine = opus.

## When to Use
- Knowledge dosyalari dolduktan sonra kalite artirma
- Duzensiz/dagink bilgiyi yapilandirma
- Periyodik bakim (ayda 1)
- Agent performansi dusukse (bilgi kalitesi sorunu olabilir)

## When NOT to Use
- Knowledge bos ise (once `/agent-sharpen`)
- Agent yapisi degismesi gerekiyorsa (→ `/agent-setup`)

## Scope Secenekleri
- `--scope agent`: Sadece AGENT.md refine
- `--scope knowledge`: Sadece knowledge/*.md refine
- `--scope all` (default): Her sey

## Red Flags
- Refine sonrasi knowledge dosyasi %50'den fazla degistiyse — buyuk sorun, onceki sharpen kalitesiz
- Tum bilgi silindiyse — kaynak kalitesi sorunu
- Ayni refinement'i 3+ kez yapmak gerekiyorsa — AGENT.md boundary'si yanlis olabilir

## Verification
- [ ] Tum dosyalar tutarli ve cakismasiz
- [ ] Gereksiz tekrar yok
- [ ] Her knowledge dosyasinda kaynak ve tarih var
- [ ] refinements.md'ye entry eklendi
- [ ] _index.md guncel
