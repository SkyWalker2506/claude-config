# Agent Dispatch Protocol

> Sub-agent baslatilirken uygulanacak header, bildirim ve heartbeat kurallari.

## Sub-agent prompt header formati

Her `Agent tool` cagrisinda prompt'un basina su blok eklenmeli:

```
---
AGENT: {id} — {name}
ROLE: {description}
MODEL: {primary_model} | EFFORT: {effort}
TASK: {gorev ozeti - 1 satir}
CALLER: {cagiran agent id veya "user"}
WATCHDOG: {quick|medium|long} — max {max_tool_calls} tool call
---
```

Placeholder'lar `agent-registry.json`'dan doldurulur. `TASK` ve `CALLER` cagiran tarafindan yazilir.

## Ana thread bildirim formati

Agent baslatildiginda kullaniciya gosterilecek ozet:

```
🤖 [{id}] {name} baslatildi → {gorev} ({primary_model}, {effort})
```

Agent tamamlandiginda:

```
✅ [{id}] {name} tamamlandi → {outcome}
```

veya hata durumunda:

```
❌ [{id}] {name} basarisiz → {hata ozeti}
```

## Background agent heartbeat

Her 5 tool call'da sub-agent su komutu calistirir:

```bash
mkdir -p ~/Projects/.watchdog
echo '{"agent":"{id}","task":"{gorev}","step":"{mevcut adim}","progress":"{X/Y}","status":"running","ts":"'$(date -u +%FT%TZ)'"}' >> ~/Projects/.watchdog/agent-log.jsonl
```

## Tamamlanma bildirimi

Gorev bittiginde (basarili veya basarisiz):

```bash
echo '{"agent":"{id}","task":"{gorev}","outcome":"{success|failed}","duration_s":{sure},"tool_calls":{sayi},"ts":"'$(date -u +%FT%TZ)'"}' >> ~/Projects/.watchdog/agent-log.jsonl
```

## Agent chain ornegi

```
user → A1 (Orchestrator)
         → A2 (Router) — gorev analizi, agent secimi
         → B7 (Bug Hunter) — implementasyon
         → C1 (Code Review) — review
         → A1'e donus — sonuc raporu
```

Her zincir adiminda:
1. Caller kendi `[id]` etiketini yazar
2. Callee dispatch header'i alir
3. Heartbeat log'a yazilir
4. Tamamlanma bildirimi gonderilir

## Router entegrasyonu

Agent secimi icin:

```bash
~/Projects/claude-config/config/agent-router.sh "{gorev aciklamasi}"
```

Cikti: `{ID} {Name} ({model}, {effort})`

Bu cikti dispatch header'in `AGENT`, `MODEL`, `EFFORT` alanlarini doldurur.

---

## Agent Index Sistemi

### Session basinda (zorunlu)

Her session/orchestrator basinda kurulu agent'lari tara ve indexle:

```bash
# Kac agent kurulu?
INSTALLED=$(ls ~/.claude/agents/*/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "[Agent Index] $INSTALLED agent kurulu: ~/.claude/agents/"

# Registry ile karsilastir
REGISTRY_TOTAL=$(python3 -c "
import json
with open('$HOME/Projects/claude-config/config/agent-registry.json') as f:
    d = json.load(f)
print(len(d.get('agents', {})))
" 2>/dev/null || echo "?")

echo "[Agent Index] Registry: $REGISTRY_TOTAL | Kurulu: $INSTALLED"
```

Sonucu her session basinda 1 satirda raporla:
```
[Agent Index] 40/134 agent kurulu. Eksik: 94 (marketplace'den indirilebilir)
```

### Marketplace awareness

Bir gorev icin gereken agent kurulu degilse:
1. `agent-registry.json`'dan agent ID'sini bul
2. Kullaniciya bildir: `"[B7 Bug Hunter] kurulu degil — indirmek ister misin?"`
3. Onay gelirse:
```bash
cd ~/Projects/claude-agent-catalog && bash install.sh {CATEGORY}
# veya spesifik agent icin kategori klasorunden kopyala
```

Marketplace repo yoksa once clone et:
```bash
[ -d ~/Projects/claude-agent-catalog ] || git clone https://github.com/SkyWalker2506/claude-agent-catalog ~/Projects/claude-agent-catalog
```

### Periyodik index refresh

- Session basinda: tam tarama
- Her 10 tool call'da: sadece `ls ~/.claude/agents/*/*.md | wc -l` — sayi degistiyse raporla
- Yeni agent algılanirsa: `[Agent Index] +3 yeni agent tespit edildi, index guncellendi`

### Dinamik kapasite — hardcode etme

`agent-registry.json`'daki toplami runtime'da say. "134 agent var" yazma — her zaman:
```python
len(registry['agents'])  # toplam
len([a for a in registry['agents'].values() if a.get('status') == 'active'])  # aktif
```

---

## Eksik Agent Raporlama

Bir görev için gereken agent ne yerel `~/.claude/agents/`'ta ne de `claude-agent-catalog`'da bulunursa:

### Kim istiyor? (requester tespiti)

```python
# git config veya sistem kullanıcısından tespit
import subprocess
git_user = subprocess.getoutput("git config user.email 2>/dev/null").strip()
OWNER_EMAILS = ["musabkara1990@gmail.com"]  # sahip e-postaları
is_owner = git_user in OWNER_EMAILS
```

Alternatif: `$USER` == `musabkara` veya `$HOME` == `/Users/musabkara` → owner.

### Owner ise → Jira CA projesi

```bash
# CA = Claude Agents projesi (id: 10437)
# MCP ile:
# createJiraIssue cloudId=1216fb6b-a912-41d7-9e2e-f19a7db50ae6 projectKey=CA
# summary="[Agent Request] {agent_name} — {capability}"
# description="Görev: {görev}\nGerekli capability: {capability}\nMevcut alternatif: {fallback_agent}"
```

Format:
```
CA-X  [Agent Request] {agent_name}
      Görev: {görev açıklaması}
      Capability: {eksik capability}
      Öneri: marketplace'e eklenmeli veya yeni agent yazılmalı
```

### User (owner değil) ise → GitHub Issue

```bash
gh issue create \
  --repo SkyWalker2506/claude-agent-catalog \
  --title "[Agent Request] {agent_name} — {capability}" \
  --body "## Agent Request

**Requested by:** {requester}
**Task:** {görev açıklaması}
**Missing capability:** {capability}
**Searched in:** local ~/.claude/agents/ + claude-agent-catalog

## Suggested agent spec
- Category: {önerilen kategori}
- Model: {önerilen model}
- Capabilities: [{capability}]

*Auto-generated by claude-config agent-dispatch system*" \
  --label "agent-request"
```

### Raporlama akışı

```
1. Görev geldi → agent-router.sh ile ara
2. Bulunamadı → marketplace'de ara (claude-agent-catalog)
3. Orada da yok → requester tespit et
   - Owner → CA Jira issue aç
   - User  → GitHub issue aç (SkyWalker2506/claude-agent-catalog)
4. Fallback agent ile devam et (en yakın capability match)
5. Kullanıcıya bildir: "X agent bulunamadı, {fallback} ile devam ediyorum. İstek {CA-X / GitHub#N} açıldı."
```
