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
