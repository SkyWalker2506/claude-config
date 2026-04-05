#!/bin/bash
# dispatch-reflect.sh — Dispatch kararlarını analiz et, sistemi refine et
# Kullanım: bash dispatch-reflect.sh [--last N] [--apply]
# Stop hook'tan tetiklenir, bg'de çalışır

DISPATCH_LOG="$HOME/Projects/.watchdog/dispatch-log.jsonl"
REGISTRY="$HOME/Projects/claude-config/config/agent-registry.json"
REFLECT_LOG="$HOME/Projects/.watchdog/reflect-log.jsonl"
ROUTER="$HOME/Projects/claude-config/config/agent-router.sh"

LAST="${2:-20}"   # Son kaç kaydı analiz et
APPLY=false
for arg in "$@"; do
  [ "$arg" = "--apply" ] && APPLY=true
  [[ "$arg" =~ ^[0-9]+$ ]] && LAST="$arg"
done

[ ! -f "$DISPATCH_LOG" ] && exit 0

python3 - "$DISPATCH_LOG" "$REGISTRY" "$REFLECT_LOG" "$ROUTER" "$LAST" "$APPLY" << 'PYEOF'
import json, sys, os, re, datetime, subprocess

log_path, registry_path, reflect_log, router_path, last_n, apply_str = sys.argv[1:]
last_n = int(last_n)
apply = apply_str == "True"

# Son N dispatch kararını oku
with open(log_path) as f:
    entries = [json.loads(l) for l in f if l.strip()]
recent = entries[-last_n:]

if not recent:
    sys.exit(0)

with open(registry_path) as f:
    reg = json.load(f)

# Analiz: hangi agent'lar seçildi, skor dağılımı, yakın rakipler
agent_counts = {}
low_confidence = []   # top1 ve top2 skor farkı < 1.0
no_match = []

for e in recent:
    sel = e.get('selected', {})
    aid = sel.get('id', 'UNKNOWN')
    agent_counts[aid] = agent_counts.get(aid, 0) + 1

    top3 = e.get('top3', [])
    if len(top3) >= 2:
        gap = top3[0]['score'] - top3[1]['score']
        if gap < 1.0:
            low_confidence.append({
                'query': e['query'],
                'winner': top3[0],
                'runner_up': top3[1],
                'gap': round(gap, 2)
            })
    if sel.get('id') == 'UNKNOWN' or 'NO_MATCH' in e.get('query',''):
        no_match.append(e['query'])

# Refinement önerileri
suggestions = []

# 1. Düşük güven → capabilities veya alias ekle
for lc in low_confidence:
    q = lc['query']
    winner_id = lc['winner']['id']
    runner_id = lc['runner_up']['id']
    suggestions.append({
        'type': 'low_confidence',
        'query': q,
        'winner': winner_id,
        'runner_up': runner_id,
        'gap': lc['gap'],
        'suggestion': f"{winner_id} için capabilities güçlendir veya intent alias ekle"
    })

# 2. Tek agent çok seçiliyor → o agent overfit olmuş olabilir
for aid, cnt in agent_counts.items():
    if cnt > last_n * 0.5 and len(agent_counts) > 1:
        suggestions.append({
            'type': 'overfit',
            'agent': aid,
            'count': cnt,
            'total': last_n,
            'suggestion': f"{aid} son {last_n} kararın {cnt}'inde seçildi — capabilities çok geniş olabilir"
        })

# Auto-apply: güven skoru düşük ama pattern açıksa capability güçlendir
applied = []
if apply and suggestions:
    for s in suggestions:
        if s['type'] == 'low_confidence':
            winner_id = s['winner']
            query_words = set(re.findall(r'[a-z0-9]+', s['query'].lower()))
            if winner_id in reg.get('agents', {}):
                agent = reg['agents'][winner_id]
                existing = set(agent.get('capabilities', []))
                # Query'deki anlamlı kelimeleri capability olarak ekle (stop words hariç)
                stop = {'a','the','is','in','for','fix','do','to','of','and','or','with','on','at'}
                new_caps = [w for w in query_words if w not in stop and w not in existing and len(w) > 2]
                if new_caps:
                    agent['capabilities'] = list(existing) + new_caps[:2]
                    applied.append(f"{winner_id}: +{new_caps[:2]}")

    if applied:
        with open(registry_path, 'w') as f:
            json.dump(reg, f, indent=2)

# Reflect log'a yaz
reflect_entry = {
    'ts': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'analyzed': last_n,
    'agent_counts': agent_counts,
    'low_confidence_count': len(low_confidence),
    'suggestions_count': len(suggestions),
    'applied': applied,
    'top_suggestions': suggestions[:3]
}
os.makedirs(os.path.dirname(reflect_log), exist_ok=True)
with open(reflect_log, 'a') as f:
    f.write(json.dumps(reflect_entry, ensure_ascii=False) + '\n')

# Özet çıktı (bg'de çalışınca sessiz, ama log'a düşer)
if applied:
    print(f"[dispatch-reflect] {len(recent)} karar analiz edildi. {len(applied)} iyileştirme uygulandı: {applied}")
elif suggestions:
    print(f"[dispatch-reflect] {len(recent)} karar analiz edildi. {len(suggestions)} öneri → reflect-log'a yazıldı.")
else:
    print(f"[dispatch-reflect] {len(recent)} karar analiz edildi. Sorun yok.")
PYEOF
