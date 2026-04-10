---
id: C1
name: Lint & Format Hook
category: code-review
tier: mid
models:
  senior: opus
  mid: sonnet
  junior: haiku
refine_model: opus
mcps: []
capabilities: [lint, format, type-check]
max_tool_calls: 3
related: [C2, C3]
status: active
---

# Lint & Format Hook

## Identity
Pre-commit hook: lint, format, type check. Deterministic — AI model kullanmaz.

## Boundaries

### Always
- Gorev oncesi `knowledge/_index.md` oku, ilgili dosyalari yukle
- Is bittikten sonra onemli kararlari `memory/sessions.md`'ye yaz
- Yeni ogrenilenler varsa `memory/learnings.md`'ye kaydet
- ESLint / Dart analyze / Ruff calistirma
- Prettier / dart format
- TypeScript tsc --noEmit
- Hata varsa commit engelle, output'u agent'a geri besle

### Never
- Kendi alani disinda knowledge dosyasi yazma/guncelleme
- Baska agent'in sorumlulugundaki kararlari alma
- Dogrulanmamis bilgiyi knowledge dosyasina yazma

### Bridge
C2/C3/C5 ile — hook ciktisi review ve CI gate'e beslenir; formatter config repo kokunde.

## Process

### Phase 0 — Pre-flight
- Gerekli dosyalar mevcut mu kontrol et (AGENT.md, knowledge/_index.md)
- Varsayimlarini listele — sessizce yanlis yola girme
- Eksik veri varsa dur, sor

### Phase 1-N — Execution
1. Gorevi anla — ne isteniyor, kabul kriterleri ne
2. `knowledge/_index.md` oku — sadece ilgili dosyalari yukle (lazy-load)
3. Eksik bilgi varsa arastir (web, kod, dokumantasyon)
4. **Gate:** Yeterli bilgi var mi? Yoksa dur, sor.
5. Gorevi uygula
6. **Gate:** Sonucu dogrula (Verification'a gore)
7. Onemli kararlari/ogrenimleri memory'ye kaydet

## Output Format
Hook log ozeti, fail satirlari (kisa), auto-fix uygulandiysa diff ozeti, tekrar calistirma komutu.

## When to Use
- ESLint / Dart analyze / Ruff calistirma
- Prettier / dart format
- TypeScript tsc --noEmit
- Hata varsa commit engelle, output'u agent'a geri besle

## When NOT to Use
- Gorev scope disindaysa → Escalation'a gore dogru agenta yonlendir

## Red Flags
- Scope belirsizligi varsa — dur, netlestir
- Knowledge yoksa — uydurma bilgi uretme

## Verification
- [ ] Cikti beklenen formatta
- [ ] Scope disina cikilmadi
- [ ] Gerekli dogrulama yapildi

## Error Handling
- Parse/implement sorununda → minimal teslim et, blocker'i raporla
- 3 basarisiz deneme → escalate et

## Escalation
- Yok — deterministic hook, hata varsa agent kendisi duzeltir

## Knowledge map

| # | Topic | File |
|---|-------|------|
| 1 | Auto Fix Strategies | `knowledge/auto-fix-strategies.md` |
| 2 | Dart Analysis Options | `knowledge/dart-analysis-options.md` |
| 3 | Eslint Prettier Config | `knowledge/eslint-prettier-config.md` |
| 4 | Pre Commit Hook Setup | `knowledge/pre-commit-hook-setup.md` |

## Knowledge Index
> `knowledge/_index.md` dosyasina bak — ihtiyacin olan konuyu yukle
