---
name: dispatch
description: "Gorevi analiz et, registry'den uygun agent sec, o kurallarla sub-agent baslat. Triggers: dispatch, agent sec, route, gorev ata."
argument-hint: "[gorev aciklamasi]"
---

# /dispatch — Agent Router & Dispatcher

Gelen gorevi analiz edip `config/agent-registry.json`'dan uygun agent'i secer ve o agent'in kurallariyla sub-agent baslatir.

## Source Availability Kontrolü

Her dispatch öncesi `source_requirements` tablosunu oku:

| Source | Secret Key | Durum |
|--------|-----------|-------|
| openrouter | OPENROUTER_API_KEY | ✅ available |
| groq | GROQ_API_KEY | ❌ missing_key |
| anthropic | (session) | ✅ available |
| huggingface | HF_TOKEN | ? not_tested |

**Ulaşılamayan source ile karşılaşılırsa:**
1. `on_source_unavailable == "use_fallbacks"` → sessizce fallback'e geç, loglа: `[FALLBACK] {agent_id} {primary} → {fallback}`
2. `on_source_unavailable == "ask_user"` → kullanıcıya sor: "X servisi için key gerekiyor, kurmak ister misiniz? [E/H]"
   - E → setup_url ver ve bekle
   - H → bir sonraki fallback'e geç
3. Tüm fallback'ler tükendiyse → farklı capability'li alternatif agent sec

**Şu an bilinen durum:** Groq key yok → Groq primary'li agentlar otomatik OpenRouter fallback'e düşer.

## Akis

### 1. Gorev analizi (max 3 tool call)

Kullanicinin gorevini analiz et:
- Hangi capability'ler gerekiyor? (api, flutter, security, jira, research, vb.)
- Hangi kategoriye dusuyor? (backend, code-review, market-research, vb.)
- Kac kategori overlap ediyor?

### 2. Agent secimi

`~/.claude/config/agent-registry.json` oku → sadece `active_agents` listesindeki agent'lar arasindan sec.

**Matching kurallari:**
- Agent'in `capabilities` alani ile gorev gereksinimlerini esle
- Birden fazla uygun agent varsa → `primary_model` maliyetine gore en ucuzunu sec
- Hicbir agent uyusmuyorsa → A1 (Lead Orchestrator) escalate et
- 3+ kategori overlap → Opus'a escalate et (`A2.escalate_when` kurali)

**Confidence skorlama:**
- >= 0.85 → tek agent dispatch
- 0.6 - 0.85 → primary + secondary parallel
- < 0.6 → kullaniciya sor

### 3. Model & effort atama

Secilen agent'in registry'deki ayarlarini kullan:
- `primary_model` → model olarak ata
- `effort` → effort seviyesi
- `max_tool_calls` → sub-agent limiti
- `fallbacks` → model duserse sirayla dene
- `mcps` → hangi MCP'ler aktif

### 3.5. Strategy-aware dispatch

Agent secildikten sonra `strategy` alanina bak:

| Strategy | Model atama | Dispatch yontemi |
|----------|-------------|-----------------|
| `direct` | `primary_model` olarak kullan | Tek agent, degisiklik yok |
| `cheap_first` | `primary_model` (ucuz/free/haiku) ile basla | Basarisizsa `fallbacks` zincirinden yuksel |
| `two_pass` | Executor: `primary_model`, Reviewer: `opus` | Sonnet/free ile kod yaz, Opus ile review |
| `opus_plan` | Plan: `opus`, Execution: `sonnet` | /plan modunda Opus, execution'da Sonnet |

**`cheap_first` basari kriteri:**
- Sub-agent ciktisi bos degil + hata mesaji yok → basarili
- Basarisizsa → `fallbacks[0]` ile tekrar dispatch (retry_strategy adimlari)

**`two_pass` nasil calisir:**
- Forge / jira-start-new-task pipeline'i otomatik uygular bu stratejiyi
- Manuel dispatch'te: once coder agent → PR olustur → sonra C3 (reviewer) agent'ini dispatch et

**Strategy eksikse:** `direct` olarak davran.

### 4. Sub-agent baslat

Agent tool ile sub-agent dispatch et. Sub-agent prompt'u:

```
AGENT: {id} ({name})
MODEL: {primary_model} | EFFORT: {effort} | MAX: {max_tool_calls} tool call | STRATEGY: {strategy}
MCP: {mcps}
CAPABILITIES: {capabilities}

GOREV: {kullanici gorevi}

KURALLAR:
- {agent .md dosyasindan kapsam ve escalation kurallari}
- WATCHDOG: Her {watchdog.self_check_interval} call self-check, max {max_tool_calls} call
- Escalation gerekirse → {related agent'lar}
```

### 5. Sonuc

Sub-agent tamamladiginda:
- Basarili → sonucu kullaniciya goster
- Basarisiz → retry_strategy uygula (1. ayni agent farkli model, 2. farkli agent ayni capability, 3. A1'e escalate)

## Ozel durumlar

### Paralel dispatch
Gorev birden fazla bagimsiz parcaya bolunebiliyorsa:
```
"REST endpoint yaz + test yaz" → B2 (Backend Coder) + B6 (Test Writer) paralel
"Pazar arastir + landing page yaz" → H1 (Market Researcher) + M2 (Landing Page) paralel
```

### Escalation zincirleri
| Durum | Aksiyon |
|-------|---------|
| Mimari karar | → B1 (Opus) |
| Guvenlik endisesi | → B13 (Opus) |
| 3+ kategori | → A1 (Lead Orchestrator) |
| Model dusuk performans | → fallback zinciri |
| Tum fallback'ler tukenirse | → kullaniciya sor |

## Kurallar
- Pool agent'lari GORMEZ — sadece active_agents
- Her dispatch'te 1 satir log: `[DISPATCH] {gorev} → {agent_id} ({model})`
- Max 5 tool call dispatch icin (gorev analizi + registry oku + agent sec + dispatch)
- Gereksiz dispatch yapma — basit soru/cevap icin agent atama

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
