---
name: dispatch
description: "Gorevi analiz et, registry'den uygun agent sec, o kurallarla sub-agent baslat. Triggers: dispatch, agent sec, route, gorev ata."
argument-hint: "[gorev aciklamasi]"
---

# /dispatch — Agent Router & Dispatcher

Gelen gorevi analiz edip `config/agent-registry.json`'dan uygun agent'i secer ve o agent'in kurallariyla sub-agent baslatir.

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

### 4. Sub-agent baslat

Agent tool ile sub-agent dispatch et. Sub-agent prompt'u:

```
AGENT: {id} ({name})
MODEL: {primary_model} | EFFORT: {effort} | MAX: {max_tool_calls} tool call
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
