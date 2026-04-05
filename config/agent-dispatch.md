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
