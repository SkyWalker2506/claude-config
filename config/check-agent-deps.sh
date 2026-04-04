#!/usr/bin/env bash
set -euo pipefail

AGENT_ID="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}"
AGENTS_DIR="${SCRIPT_DIR}/../agents"
SECRETS_FILE="$HOME/.claude/secrets/secrets.env"
SETTINGS_FILE="$HOME/.claude/settings.json"

if [ -z "$AGENT_ID" ]; then
  echo '{"error": "Usage: check-agent-deps.sh <agent-id>"}'; exit 1
fi

AGENT_FILE=$(grep -rl "^id: $AGENT_ID$" "$AGENTS_DIR" --include="*.md" 2>/dev/null | head -1)
if [ -z "$AGENT_FILE" ]; then
  echo "{\"error\": \"Agent $AGENT_ID not found\"}"; exit 1
fi

export AGENT_ID AGENT_FILE CONFIG_DIR SECRETS_FILE SETTINGS_FILE

python3 << 'PYEOF'
import json, re, subprocess, os, sys

agent_file = os.environ["AGENT_FILE"]
config_dir = os.environ["CONFIG_DIR"]
secrets_file = os.environ["SECRETS_FILE"]
settings_file = os.environ["SETTINGS_FILE"]
agent_id = os.environ["AGENT_ID"]

def parse_fm(fp):
    with open(fp) as f: c = f.read()
    m = re.match(r'^---\n(.*?)\n---', c, re.DOTALL)
    if not m: return {}
    fm = {}
    for line in m.group(1).split('\n'):
        s = line.strip()
        if ':' in s and not s.startswith('-'):
            k, _, v = s.partition(':'); k=k.strip(); v=v.strip()
            fm[k] = [x.strip() for x in v[1:-1].split(',') if x.strip()] if v.startswith('[') and v.endswith(']') else v
    return fm

def env_exists(var):
    if os.path.exists(secrets_file):
        with open(secrets_file) as f:
            for l in f:
                if l.strip().startswith(var+'=') and l.strip().split('=',1)[1].strip('"').strip("'"): return True
    return bool(os.environ.get(var))

def mcp_exists(name):
    if os.path.exists(settings_file):
        try:
            with open(settings_file) as f: return name in json.load(f).get('mcpServers',{})
        except: pass
    return False

fm = parse_fm(agent_file)
pm = fm.get('primary_model','')
fb = fm.get('fallbacks',[])
if isinstance(fb,str): fb=[x.strip() for x in fb.strip('[]').split(',') if x.strip()]

mr={}; mrf=os.path.join(config_dir,'model-requirements.json')
if os.path.exists(mrf):
    with open(mrf) as f: mr=json.load(f).get('model_requirements',{})

req=[]; opt=[]
mcps=fm.get('mcps',[])
if isinstance(mcps,str): mcps=[x.strip() for x in mcps.strip('[]').split(',') if x.strip()]
for m in mcps:
    if m=='*': continue
    if not mcp_exists(m): opt.append({"type":"mcp","name":m})

skip={'none','free-script','free-cron','free-deterministic','free-web','free-coderabbit','free-github-action','free-gmail-mcp','free-context7','free-router'}
for model in [pm]+(fb if isinstance(fb,list) else []):
    if not model or model in skip: continue
    r=mr.get(model,{})
    if not r: continue
    n=r.get('needs',[])
    if 'ollama' in n:
        om=r.get('ollama_model','')
        if om:
            try: chk=subprocess.run(f"ollama list 2>/dev/null|grep -q '{om}'",shell=True,capture_output=True,timeout=10).returncode!=0
            except: chk=True
            if chk: (req if model==pm else opt).append({"type":"model","name":om,"install":r.get('install','')})
    if 'claude-api' in n and not env_exists('ANTHROPIC_API_KEY'):
        req.append({"type":"api","name":"ANTHROPIC_API_KEY","console":r.get('console','')})
    if 'openrouter-api' in n and not env_exists('OPENROUTER_API_KEY'):
        opt.append({"type":"api","name":"OPENROUTER_API_KEY","console":r.get('console','')})

res={"agent":agent_id,"primary_model":pm,"ready":len(req)==0,"missing_required":req,"missing_optional":opt}
print(json.dumps(res,indent=2))
sys.exit(0 if res["ready"] else 1)
PYEOF
