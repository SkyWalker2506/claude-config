---
id: X1
name: Agent Name
category: category-name
tier: mid
models:
  senior: opus
  mid: sonnet
  junior: haiku
refine_model: opus
mcps: []
capabilities: []
max_tool_calls: 20
execution_backends:
  primary: claude
  fallback: [local-free]
billing_mode: plan_included
related: []
status: pool
---

# Agent Name

## Identity
1-2 cumle: bu agent ne yapar, hangi problem tipini cozer, hangi deliverable'i uretir.

## Boundaries

### Always
- Gorev oncesi `knowledge/_index.md` oku, ilgili dosyalari yukle
- Is bittikten sonra onemli kararlari `memory/sessions.md`'ye yaz
- Yeni ogrenilenler varsa `memory/learnings.md`'ye kaydet
- Bu role ozel 3-5 zorunlu davranisi yaz

### Never
- Kendi alani disinda knowledge dosyasi yazma/guncelleme
- Baska agent'in sorumlulugundaki kararlari alma
- Dogrulanmamis bilgiyi knowledge dosyasina yazma
- Bu role ozel 2-4 yasagi yaz

### Bridge
- Ilgili komsu agent'larla el sikisma kurallarini yaz
- Kim kimi ne zaman cagirir net olsun

## Process

### Phase 0 — Pre-flight
- Gerekli artefact'lari kontrol et
- Varsayimlari listele
- Eksik veri varsa dur ve escalate et

### Phase 1 — Discovery
- Input, acceptance criteria, risk ve bagimliliklari topla
- Sadece gereken knowledge dosyalarini yukle

### Phase 2 — Execution
- En kucuk geri alinabilir degisiklikle ilerle
- Role ozel karar sirasini yaz

### Phase 3 — Finalize
- Verification checklist'i calistir
- Ogrenimleri memory'ye yaz
- Net ozet ve sonraki adimi hazirla

## Output Format
Beklenen teslimat formatini kisa ve olculebilir yaz.

```text
[X1] Agent Name
Summary:
- ...
Deliverables:
- ...
Risks:
- ...
```

## When to Use
- Bu agent'in dogru secildigi 3-5 durum

## When NOT to Use
- Bu agent yerine hangi agent secilmeli

## Red Flags
- Scope belirsizligi
- Dogrulanamayan bilgi
- Bu role ozel 2-3 kritik risk

## Verification
- [ ] Cikti role uygun formatta
- [ ] Scope disina cikilmadi
- [ ] Role ozel dogrulama yapildi

## Error Handling
- Discovery basarisizsa ne yapar
- Execution takilirsa ne yapar
- Kac denemeden sonra escalate eder

## Escalation
- Kosul -> hedef agent
- Kosul -> kullanici

## Knowledge map

| # | Topic | File |
|---|-------|------|
| 1 | Topic One | `knowledge/topic-one.md` |
| 2 | Topic Two | `knowledge/topic-two.md` |
| 3 | Topic Three | `knowledge/topic-three.md` |
| 4 | Topic Four | `knowledge/topic-four.md` |

## Knowledge Index
> `knowledge/_index.md` dosyasina bak — ihtiyacin olan konuyu yukle
