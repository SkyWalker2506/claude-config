---
id: C1
name: Lint & Format Hook
category: code-review
tier: mid
models:
  lead: opus
  senior: sonnet
  mid: gpt-5.4-mini
  junior: gpt-5.4-nano
fallback: sonnet opus
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

## Codex CLI Usage (GPT models)

GPT model atandiysa, kodu kendin yazma. Codex CLI ile calistir:

```bash
codex exec -c model="{model}" "{prompt}"
```

Kurallar:
- GPT model (gpt-5.4, gpt-5.4-mini, gpt-5.4-nano) secildiyse **her zaman** Codex CLI kullan
- Claude model (opus, sonnet) secildiyse normal Claude sub-agent kullan
- Codex CLI cagrisini **Haiku** yapar — Haiku komutu olusturur, Bash ile calistirir, sonucu toplar
- Codex `exec` modu kullan (non-interactive), `--quiet` flag ile gereksiz output azalt
- Tek seferde tek dosya/gorev ver, buyuk isi parcala
- Codex ciktisini dogrula — hata varsa tekrar calistir veya Claude'a escalate et

Fallback zinciri (limit/hata durumunda):
```
gpt-5.4-nano → gpt-5.4-mini → gpt-5.4 → sonnet → opus
```
GPT limiti bittiyse veya Codex CLI hata veriyorsa → bir ust tier'a gec.
3 ardisik GPT hatasi → otomatik Claude fallback'e dus.

Model secim tablosu:
| Tier | Model | Invoke |
|------|-------|--------|
| junior | gpt-5.4-nano | `codex exec -c model="gpt-5.4-nano" "..."` |
| mid | gpt-5.4-mini | `codex exec -c model="gpt-5.4-mini" "..."` |
| senior | gpt-5.4 | `codex exec -c model="gpt-5.4" "..."` |
| fallback | sonnet/opus | Normal Claude sub-agent |

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
