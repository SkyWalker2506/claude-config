#!/bin/bash
# Agent Router — capability match ile registry'den agent sec
# Kullanim: ./agent-router.sh "flutter widget bug fix"
# Cikti:   B7 Bug Hunter (sonnet, medium)

set -euo pipefail

VERBOSE=false
QUERY=""
REGISTRY="${REGISTRY_PATH:-$HOME/Projects/claude-config/config/agent-registry.json}"

for arg in "$@"; do
  case "$arg" in
    --verbose|-v) VERBOSE=true ;;
    *) [ -z "$QUERY" ] && QUERY="$arg" ;;
  esac
done

[ -z "$QUERY" ] && { echo "Kullanim: $0 \"gorev aciklamasi\" [--verbose]" >&2; exit 1; }

if [ ! -f "$REGISTRY" ]; then
  echo "HATA: Registry bulunamadi: $REGISTRY" >&2
  exit 1
fi

python3 - "$QUERY" "$REGISTRY" "$VERBOSE" << 'PYEOF'
import json, sys, re

query = sys.argv[1].lower()
registry_path = sys.argv[2]
verbose = sys.argv[3] == "true"

query_words = set(re.findall(r'[a-z0-9]+', query))

# Intent signals — yüksek ağırlıklı görev türleri
INTENT = {
    'bug':         ('debugging',    3.0),
    'fix':         ('debugging',    2.5),
    'error':       ('debugging',    2.5),
    'crash':       ('debugging',    3.0),
    'debug':       ('debugging',    3.0),
    'security':    ('security-audit', 3.0),
    'audit':       ('security-audit', 2.5),
    'review':      ('code-review',  2.5),
    'deploy':      ('deployment',   2.5),
    'ci':          ('ci-cd',        2.5),
    'pipeline':    ('ci-cd',        2.0),
    'refactor':    ('refactoring',  2.5),
    'architecture':('system-design',3.0),
    'sprint':      ('sprint',       3.0),
    'jira':        ('jira',         2.5),
    'plan':        ('planning',     2.0),
    'research':    ('web-search',   2.5),
    'performance': ('performance',  2.5),
    'test':        ('testing',      2.0),
    'monitor':     ('monitoring',   2.5),
    'data':        ('data-analysis',2.0),
    'seo':         ('seo',          3.0),
    'prompt':      ('prompt-engineering', 3.0),
}

# Capability aliases — düz keyword → capability listesi (normal ağırlık: 1.0)
ALIASES = {
    'flutter': ['flutter', 'dart', 'mobile'],
    'react':   ['react', 'frontend', 'ui'],
    'api':     ['api', 'rest', 'graphql', 'api-design'],
    'docker':  ['docker', 'container', 'orchestration'],
    'database':['database-design', 'migration', 'sql'],
    'mobile':  ['flutter', 'mobile', 'ios', 'android'],
    'unity':   ['unity', 'csharp', 'game-dev'],
    'game':    ['game-dev', 'phaser', 'unity'],
    'css':     ['css', 'tailwind', 'styling'],
    'web':     ['web-search', 'scraping', 'frontend'],
    'vercel':  ['deployment', 'ci-cd', 'cloud-deploy'],
    'github':  ['ci-cd', 'github-actions', 'version-control'],
}

# Build weighted query: term → weight
weighted = {}
for w in query_words:
    weighted[w] = 1.0
    if w in INTENT:
        cap, wt = INTENT[w]
        weighted[cap] = max(weighted.get(cap, 0), wt)
    if w in ALIASES:
        for alias in ALIASES[w]:
            weighted[alias] = max(weighted.get(alias, 0), 1.0)

with open(registry_path) as f:
    reg = json.load(f)

results = []
for aid, agent in reg.get('agents', {}).items():
    if agent.get('status') != 'active':
        continue
    caps = set(c.lower() for c in agent.get('capabilities', []))
    langs = set(l.lower() for l in agent.get('languages', []))
    all_tags = caps | langs

    score = sum(wt for term, wt in weighted.items() if term in all_tags)

    # Bonus: direct word match in agent name
    name_words = set(re.findall(r'[a-z0-9]+', agent.get('name', '').lower()))
    score += len(query_words & name_words) * 0.5

    # Bonus: category keyword match
    cat = agent.get('category', '').lower().replace('-', ' ')
    cat_words = set(cat.split())
    score += len(query_words & cat_words) * 0.3

    if score > 0:
        results.append((score, aid, agent))

if not results:
    print('NO_MATCH — fallback to A1 Lead Orchestrator (sonnet, medium)')
    sys.exit(0)

results.sort(key=lambda x: (-x[0], x[1]))
best_score, best_id, best = results[0]
model = best.get('primary_model', 'sonnet')
effort = best.get('effort', 'medium')
name = best.get('name', 'Unknown')
strategy = best.get('strategy', 'direct')

# --- Phase 2: Backend resolution ---
backend_primary = best.get('execution_backends', {}).get('primary', 'claude')
backend_fallback = best.get('execution_backends', {}).get('fallback', ['claude'])

# Load execution-backends.json
import os
backends_path = os.path.expanduser('~/Projects/claude-config/config/execution-backends.json')
backends = {}
if os.path.exists(backends_path):
    with open(backends_path) as bf:
        backends = json.load(bf).get('backends', {})

# Check cost policy (from execution-backends.json or agent-registry.json)
cost_policy = {}
if os.path.exists(backends_path):
    with open(backends_path) as bf2:
        cost_policy = json.load(bf2).get('cost_policy', {})
if not cost_policy:
    cost_policy = reg.get('cost_policy', {})
api_billing_enabled = cost_policy.get('api_billing_enabled', False)

def backend_ok(backend_id):
    b = backends.get(backend_id, {})
    if b.get('api_billing') and not api_billing_enabled:
        return False, 'api_billing_disabled'
    return True, 'ok'

resolved_backend = backend_primary
resolved_reason = 'primary'
ok, reason = backend_ok(backend_primary)
if not ok:
    # Try fallbacks
    for fb in backend_fallback:
        ok2, _ = backend_ok(fb)
        if ok2:
            resolved_backend = fb
            resolved_reason = f'fallback (primary {backend_primary} blocked: {reason})'
            break
    else:
        resolved_backend = 'claude'
        resolved_reason = f'default fallback (all blocked)'

# --- Phase 3: Codex quota check ---
quota_file = os.path.expanduser('~/.watchdog/codex-quota.json')
codex_exhausted = False
if os.path.exists(quota_file):
    try:
        with open(quota_file) as qf:
            qstate = json.load(qf)
        if qstate.get('status') == 'exhausted':
            import datetime
            reset_at = qstate.get('reset_at', '')
            if reset_at:
                reset_dt = datetime.datetime.fromisoformat(reset_at.replace('Z', '+00:00'))
                if datetime.datetime.now(datetime.timezone.utc) < reset_dt:
                    codex_exhausted = True
    except:
        pass

if codex_exhausted and resolved_backend == 'openai-codex-cli':
    resolved_backend = 'claude'
    resolved_reason = 'codex_quota_exhausted'
    caps = set(c.lower() for c in best.get('capabilities', []))
    planning_caps = {'architecture_decision', 'planning', 'orchestration', 'system-design'}
    if caps & planning_caps:
        model = 'claude-opus-4-6'
    else:
        model = 'claude-sonnet-4-6'
    print(f'⚠️  Codex kullanım limiti doldu → {model} fallback aktif', file=sys.stderr)

backend_model = ""
if resolved_backend == "openai-codex-cli" and os.path.exists(backends_path):
    with open(backends_path) as bm:
        bdata = json.load(bm)
    backend_model = bdata.get("backends", {}).get("openai-codex-cli", {}).get("default_model", "")
model_suffix = f" ({backend_model})" if backend_model else ""
print(f'{best_id} {name} ({model}, {effort}, {strategy}) → backend:{resolved_backend}{model_suffix}')

if resolved_reason != 'primary':
    print(f'⚠️  Backend downgraded: {backend_primary} → {resolved_backend} ({resolved_reason})', file=sys.stderr)
    warning_msg = cost_policy.get('warning_message', 'API billing disabled, using fallback backend.')
    print(f'   {warning_msg}', file=sys.stderr)

# Log dispatch decision
import datetime
log_path = os.path.expanduser('~/Projects/.watchdog/dispatch-log.jsonl')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
top3 = [{'id': aid, 'name': agent['name'], 'score': round(score,2)} for score, aid, agent in results[:3]]
log_entry = {
    'ts': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'query': query,
    'selected': {'id': best_id, 'name': name, 'model': model, 'effort': effort, 'strategy': strategy, 'score': round(best_score,2)},
    'resolved_backend': resolved_backend,
    'resolved_reason': resolved_reason,
    'top3': top3,
    'total_candidates': len(results)
}
with open(log_path, 'a') as lf:
    lf.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

if verbose:
    print(f'\nQuery words: {sorted(query_words)}')
    print(f'Weighted terms: {dict(sorted(weighted.items(), key=lambda x: -x[1]))}')
    print(f'\nTop 5 candidates:')
    for score, aid, agent in results[:5]:
        matched = [t for t in weighted if t in set(c.lower() for c in agent.get('capabilities',[]))]
        print(f'  {score:5.1f}  {aid:4s} {agent["name"]:<30} matched={matched}')
PYEOF
