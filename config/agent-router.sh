#!/bin/bash
# Agent Router — capability match ile registry'den agent sec
# Kullanim: ./agent-router.sh "flutter widget bug fix"
# Cikti:   B7 Bug Hunter (sonnet, medium)

set -euo pipefail

QUERY="${1:?Kullanim: $0 \"gorev aciklamasi\"}"
REGISTRY="${REGISTRY_PATH:-$HOME/Projects/claude-config/config/agent-registry.json}"

if [ ! -f "$REGISTRY" ]; then
  echo "HATA: Registry bulunamadi: $REGISTRY" >&2
  exit 1
fi

python3 -c "
import json, sys, re

query = sys.argv[1].lower()
query_words = set(re.findall(r'[a-z0-9]+', query))

# Keyword aliases — yaygın görev terimlerini capability terimlerine eşle
ALIASES = {
    'bug': ['debugging', 'root-cause-analysis', 'error-tracing'],
    'fix': ['debugging', 'root-cause-analysis'],
    'debug': ['debugging', 'error-tracing', 'log-analysis'],
    'security': ['security-audit', 'vulnerability-scan', 'penetration-test'],
    'audit': ['security-audit', 'code-review'],
    'review': ['code-review', 'pr-review'],
    'deploy': ['deployment', 'ci-cd', 'cloud-deploy'],
    'test': ['testing', 'unit-test', 'integration-test', 'tdd'],
    'flutter': ['flutter', 'dart', 'mobile', 'ui', 'components'],
    'react': ['react', 'ui', 'components', 'frontend'],
    'api': ['api', 'rest', 'graphql', 'api-design', 'api-integration'],
    'jira': ['jira', 'sprint', 'backlog', 'task-management'],
    'sprint': ['sprint', 'planning', 'estimation'],
    'plan': ['planning', 'sprint', 'architecture'],
    'research': ['web-search', 'trend-analysis', 'documentation'],
    'web': ['web-search', 'scraping', 'fetch'],
    'docker': ['docker', 'container', 'orchestration'],
    'database': ['database-design', 'migration', 'sql'],
    'refactor': ['refactoring', 'code-quality', 'clean-code'],
    'performance': ['performance', 'optimization', 'profiling'],
    'architecture': ['architecture', 'system-design', 'api-design'],
    'mobile': ['flutter', 'mobile', 'dart', 'ios', 'android'],
    'unity': ['unity', 'csharp', 'game-dev', '3d'],
    'game': ['game-dev', 'phaser', 'unity'],
    'error': ['debugging', 'error-tracing', 'log-analysis'],
    'css': ['css', 'tailwind', 'ui', 'styling'],
    'ci': ['ci-cd', 'pipeline', 'github-actions'],
    'monitor': ['monitoring', 'health-check', 'alerting'],
    'data': ['data-analysis', 'etl', 'visualization'],
    'seo': ['seo', 'metadata', 'search-optimization'],
    'prompt': ['prompt-engineering', 'agent-design'],
}

# Expand query words with aliases
expanded = set()
for w in query_words:
    expanded.add(w)
    if w in ALIASES:
        expanded.update(ALIASES[w])

with open(sys.argv[2]) as f:
    reg = json.load(f)

results = []
for aid, agent in reg.get('agents', {}).items():
    if agent.get('status') != 'active':
        continue
    caps = set(c.lower() for c in agent.get('capabilities', []))
    langs = set(l.lower() for l in agent.get('languages', []))
    all_tags = caps | langs

    # Score: how many expanded query terms match agent tags
    score = len(expanded & all_tags)

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

# Show top 3 if verbose
if '--verbose' in sys.argv or '-v' in sys.argv:
    print('---')
    for score, aid, agent in results[:5]:
        print(f'  {score:.1f}  {aid} {agent[\"name\"]} [{\" \".join(agent.get(\"capabilities\",[])[:4])}]')
" "$QUERY" "$REGISTRY" "${@:2}"
