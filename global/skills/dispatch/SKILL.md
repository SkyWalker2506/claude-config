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
| groq | GROQ_API_KEY | ✅ available |
| anthropic | (session Max) | ✅ available |
| codex | codex CLI login | ✅ available |
| huggingface | HF_TOKEN | ? not_tested |

**Ulaşılamayan source ile karşılaşılırsa:**
1. `on_source_unavailable == "use_fallbacks"` → sessizce fallback'e geç, loglа: `[FALLBACK] {agent_id} {primary} → {fallback}`
2. `on_source_unavailable == "ask_user"` → kullanıcıya sor: "X servisi için key gerekiyor, kurmak ister misiniz? [E/H]"
   - E → setup_url ver ve bekle
   - H → bir sonraki fallback'e geç
3. Tüm fallback'ler tükendiyse → farklı capability'li alternatif agent sec

## Agent Truth Check

Dispatch karari vermeden once **zorunlu olarak** su komutu calistir:

```bash
python3 ~/Projects/claude-config/scripts/inspect_agent_truth.py <agent-id-veya-slug>
```

Bu komut ayni agent'i dort katmanda yan yana gosterir:
- `~/Projects/claude-config/agents/<kategori>/<slug>/AGENT.md` → kapsam, escalation, knowledge kurallari
- `~/Projects/claude-config/config/agent-registry.json` → **kanonik model/backend truth**
- `~/.claude/agents/<kategori>/<slug>.md` → session sync ile uretilen runtime mirror
- `~/.claude/config/agent-registry.json` → runtime capability ve active-agent index

**Sert kurallar:**
- `primary_model` hakkinda yorum yaparken once source registry'yi esas al
- Scope veya escalation anlatmadan once source `AGENT.md` dosyasini gor
- Runtime mirror ile source registry cakisiyorsa drift vardir; source registry'yi esas al ve sync bekle
- Tek bir katmandan tum gercegi cikarmaya calisma

## Akis

### Dispatch Decision Flow

Jarvis does NOT make dispatch decisions directly. The flow is:

1. **Jarvis receives task** from user
2. **Jarvis passes to A2** (Task Router & Dispatcher) with:
   - Task description
   - User constraints (e.g., "use GPT 5.4", "break into small tasks", "no Claude")
   - Project context (tech stack, current branch)
3. **A2 decides:**
   - Which agent(s) to assign
   - Which model/backend to use (respecting user constraints)
   - Whether to split into sub-tasks
   - Confidence score for routing
4. **A2 dispatches** — launches sub-agent(s) with full knowledge injection
5. **Jarvis monitors** — tracks progress, reports results

Jarvis NEVER:
- Selects agents from registry directly
- Decides model assignments
- Writes dispatch prompts
- Contains routing logic or model selection tables

All routing intelligence lives in A2. Jarvis only passes task + constraints.

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

Secilen agent icin katmanlari ayir:
- **Kanonik model/backend truth:** `~/Projects/claude-config/config/agent-registry.json`
- **Scope/escalation truth:** source `agents/<kategori>/<slug>/AGENT.md`
- **Runtime mirror/cache:** `~/.claude/agents/<kategori>/<slug>.md`

Atama sirasi:
- `primary_model`, `fallbacks`, `effort`, `template` → source registry
- `max_tool_calls`, `mcps`, `capabilities`, `related` → source `AGENT.md`, yoksa source registry
- Kapsam ve escalation kurallari → source `AGENT.md`
- Runtime mirror sadece hizli kontrol icindir; source ile cakisirsa mirror'a guvenme

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

### 3.6. Knowledge Assembly

Sub-agent prompt header'i kurulmadan hemen once bu adim **zorunlu**:
1. Secilen agent'in registry kaydindan `category` bilgisini al.
2. `slug`'u varsayma; source repo'da `agents/{category}/*/AGENT.md` dosyalari icinde `id: {agent_id}` eslesmesini bularak gercek agent klasorunu tespit et.
3. `agents/{category}/{slug}/AGENT.md` dosyasini oku ve yalnizca `Identity` + `Boundaries` bolumlerini cikar.
4. `agents/{category}/{slug}/knowledge/_index.md` dosyasini oku ve tam icerigini al.
5. Bu iki kaynagi dispatch header'indaki `KNOWLEDGE.identity` ve `KNOWLEDGE.knowledge_index` alanlarina inject et.
6. `knowledge_path` alanini `agents/{category}/{slug}/knowledge/` olarak yaz ve `instruction` satirini ekle: `Read knowledge files relevant to your task from the path above before starting work.`

Agent tool cagrilmadan once `KNOWLEDGE` blogu bos birakilmaz. Sub-agent kendi source `AGENT.md` kimligi ve `knowledge/_index.md` icerigini header'da gormeden baslatilmaz. Bu dosyalardan biri eksikse runtime mirror'dan uydurma bilgi cekme; dispatch'i durdur ve blocker olarak raporla.

### 4. Sub-agent baslat

Before calling the Agent tool, write dispatch metadata to a sidecar file:

```bash
mkdir -p /tmp/watchdog
echo '{"agent_id":"{id}","agent_name":"{name}","model":"{primary_model}","task":"{task_summary}","ts":"'$(date -Iseconds)'"}' > /tmp/watchdog/current_dispatch.json
```
Replace `{id}`, `{name}`, `{primary_model}`, `{task_summary}` with actual values from the selected agent.

Agent tool ile sub-agent dispatch et. Sub-agent prompt'u:

```
---
AGENT: {id} — {name}
ROLE: {description}
MODEL: {primary_model} | EFFORT: {effort}
TASK: {kullanici gorevi - 1 satir ozet}
CALLER: {cagiran agent id veya "user"}
WATCHDOG: {quick|medium|long} — max {max_tool_calls} tool call

KNOWLEDGE:
  identity: |
    {AGENT.md dosyasindan Identity + Boundaries}
  knowledge_index: |
    {agents/{category}/{slug}/knowledge/_index.md tam icerigi}
  knowledge_path: agents/{category}/{slug}/knowledge/
  instruction: Read knowledge files relevant to your task from the path above before starting work.
---

STRATEGY: {strategy}
MAX_TOOL_CALLS: {max_tool_calls}
MCP: {mcps}
CAPABILITIES: {capabilities}

GOREV: {kullanici gorevi}

KURALLAR:
- {agent .md dosyasindan kapsam ve escalation kurallari}
- KNOWLEDGE: Header'daki `Identity + Boundaries` ve `knowledge_index` source of truth'tur; ise baslamadan once `knowledge_path` altindan gorevle ilgili dosyalari oku
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

### Codex CLI Dispatch Rules

When dispatching to an agent with `execution_mode: codex_cli`:

1. **No git instructions** — Codex cannot commit/push. Remove "Commit: ..." from prompts. Jarvis commits separately after verifying output.
2. **Max file size** — If target file is >500 lines, break the task into sub-tasks of max 300 lines each.
3. **No network tasks** — Codex has no internet. Don't ask it to fetch URLs, install packages, or call APIs.
4. **Verify after each task** — Check that output files exist and were modified. `codex exec` exit code 0 does not guarantee file changes.
5. **Kill timeout** — If codex runs >15 minutes on a medium task, it's likely stuck. Kill and retry with a smaller scope.
6. **Prompt format** — Use stdin: `cat prompt.md | codex exec --model gpt-5.4 --full-auto -`. This avoids shell escaping issues with complex prompts.
