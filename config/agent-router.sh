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

print(f'{best_id} {name} ({model}, {effort})')

if verbose:
    print(f'\nQuery words: {sorted(query_words)}')
    print(f'Weighted terms: {dict(sorted(weighted.items(), key=lambda x: -x[1]))}')
    print(f'\nTop 5 candidates:')
    for score, aid, agent in results[:5]:
        matched = [t for t in weighted if t in set(c.lower() for c in agent.get('capabilities',[]))]
        print(f'  {score:5.1f}  {aid:4s} {agent["name"]:<30} matched={matched}')
PYEOF
