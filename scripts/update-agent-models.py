#!/usr/bin/env python3
"""Update all AGENT.md files — GPT-5.4 primary, Claude fallback when limits hit."""

import os
import re
import glob

AGENTS_DIR = os.path.expanduser("~/Projects/claude-config/agents")

# Principle: GPT default everywhere. Claude only as fallback or where CLEARLY superior.
# "lead" = en zor task, "junior" = en basit task
# Fallback chain: gpt-5.4-nano → gpt-5.4-mini → gpt-5.4 → sonnet → opus

CATEGORY_MODELS = {
    # Research, market, sales, marketing: full GPT stack
    "research": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    "market-research": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    "marketing-engine": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    "sales-bizdev": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # Productivity, AI ops, Jira: full GPT
    "productivity": {
        "lead": "gpt-5.4-mini",
        "senior": "gpt-5.4-nano",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    "ai-ops": {
        "lead": "gpt-5.4-mini",
        "senior": "gpt-5.4-nano",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    "jira-pm": {
        "lead": "gpt-5.4-mini",
        "senior": "gpt-5.4-nano",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # DevOps: GPT strong at terminal, full GPT
    "devops": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # Backend: GPT primary, Claude fallback for complex multi-file
    "backend": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-mini",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # Code review: GPT primary (gap small), Claude fallback
    "code-review": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # Design: GPT primary
    "design": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # 3D/CAD: GPT primary
    "3d-cad": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-mini",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # Data analytics: GPT primary
    "data-analytics": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-mini",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # Prompt engineering: GPT primary, Claude fallback for nuance
    "prompt-engineering": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
    # Orchestrator: GPT primary for most
    "orchestrator": {
        "lead": "gpt-5.4",
        "senior": "gpt-5.4-mini",
        "mid": "gpt-5.4-nano",
        "junior": "gpt-5.4-nano",
        "fallback": "sonnet",
    },
}

# Decision-makers & large-context reasoning → Opus at lead/senior
# Principle: karar veren = Opus, uygulayan = GPT
AGENT_OVERRIDES = {
    # Orchestrators — karar mekanizması
    "A0": {"lead": "sonnet", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"}, # Jarvis — yaver, karar vermez, iletir
    "A1": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "opus"},  # Lead Orchestrator
    "A3": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# Code Lead
    "A9": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# Sec Lead
    "A5": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# Biz Lead
    "A6": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# Growth Lead
    "A8": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# Art Lead
    # Architecture & Security — büyük context, yüksek hata maliyeti
    "B1": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4", "junior": "gpt-5.4-mini", "fallback": "opus"},       # Backend Architect
    "B13": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4", "junior": "gpt-5.4-mini", "fallback": "opus"},      # Security Auditor
    "B5": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4", "junior": "gpt-5.4-mini", "fallback": "sonnet"},     # Bug Hunter
    # Code Review — kalite kararı
    "C1": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# Lead Reviewer
    "C3": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# AI Reviewer
    # Sprint Planning — planlama kararı
    "I1": {"lead": "opus", "senior": "sonnet", "mid": "gpt-5.4-mini", "junior": "gpt-5.4-nano", "fallback": "sonnet"},# Sprint Planner
}

CODEX_CLI_NOTE = """
## Codex CLI Usage (GPT models)

GPT model atandiysa, kodu kendin yazma. Codex CLI ile calistir:

```bash
codex exec -c model="{model}" "{prompt}"
```

Kurallar:
- GPT model (gpt-5.4, gpt-5.4-mini, gpt-5.4-nano) secildiyse **her zaman** Codex CLI kullan
- Claude model (opus, sonnet) secildiyse normal Claude sub-agent kullan
- Codex CLI cagrisini **Haiku** yapar — Haiku komutu olusturur, Bash ile calistirir, sonucu toplar
- Codex `exec` modu kullan (non-interactive), `--quiet` flag ile gereksiz output azalt
- Tek seferde tek dosya/gorev ver, buyuk isi parcala
- Codex ciktisini dogrula — hata varsa tekrar calistir veya Claude'a escalate et

Fallback zinciri (limit/hata durumunda):
```
gpt-5.4-nano → gpt-5.4-mini → gpt-5.4 → sonnet → opus
```
GPT limiti bittiyse veya Codex CLI hata veriyorsa → bir ust tier'a gec.
3 ardisik GPT hatasi → otomatik Claude fallback'e dus.

Model secim tablosu:
| Tier | Model | Invoke |
|------|-------|--------|
| junior | gpt-5.4-nano | `codex exec -c model="gpt-5.4-nano" "..."` |
| mid | gpt-5.4-mini | `codex exec -c model="gpt-5.4-mini" "..."` |
| senior | gpt-5.4 | `codex exec -c model="gpt-5.4" "..."` |
| fallback | sonnet/opus | Normal Claude sub-agent |
"""


def get_category(content):
    m = re.search(r'^category:\s*(.+)$', content, re.MULTILINE)
    if m:
        cat = m.group(1).strip()
        if '/' in cat:
            cat = cat.split('/')[0]
        return cat
    return None


def get_agent_id(content):
    m = re.search(r'^id:\s*(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def update_models_block(content, models):
    models_yaml = "models:\n"
    models_yaml += f"  lead: {models['lead']}\n"
    models_yaml += f"  senior: {models['senior']}\n"
    models_yaml += f"  mid: {models['mid']}\n"
    models_yaml += f"  junior: {models['junior']}\n"
    models_yaml += f"fallback: {models.get('fallback', 'sonnet')}"

    # Match existing models block (4 tiers: lead, senior, mid, junior) + optional fallback
    pattern = r'models:\n\s+lead:\s+\S+\n\s+senior:\s+\S+\n\s+mid:\s+\S+\n\s+junior:\s+\S+\n(?:fallback:\s+\S+)?'
    if re.search(pattern, content):
        content = re.sub(pattern, models_yaml, content)
    else:
        # Try old format (3 tiers: senior, mid, junior)
        pattern_old = r'models:\n\s+senior:\s+\S+\n\s+mid:\s+\S+\n\s+junior:\s+\S+'
        if re.search(pattern_old, content):
            content = re.sub(pattern_old, models_yaml, content)
    return content


def update_codex_note(content):
    """Replace existing Codex CLI note or add new one."""
    # Remove old note first
    pattern = r'\n## Codex CLI Usage \(GPT models\).*?(?=\n## |\Z)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Add new note before Escalation/Knowledge or at end
    for marker in ["## Escalation", "## Knowledge map", "## Knowledge Index"]:
        if marker in content:
            content = content.replace(marker, CODEX_CLI_NOTE.strip() + "\n\n" + marker)
            return content

    content = content.rstrip() + "\n\n" + CODEX_CLI_NOTE.strip() + "\n"
    return content


def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    category = get_category(content)
    agent_id = get_agent_id(content)

    if not category:
        return False, f"no category: {filepath}"

    if agent_id and agent_id in AGENT_OVERRIDES:
        models = AGENT_OVERRIDES[agent_id]
    elif category in CATEGORY_MODELS:
        models = CATEGORY_MODELS[category]
    else:
        models = {
            "lead": "gpt-5.4",
            "senior": "gpt-5.4-mini",
            "mid": "gpt-5.4-nano",
            "junior": "gpt-5.4-nano",
            "fallback": "sonnet",
        }

    if not re.search(r'models:\n\s+(?:lead|senior):', content):
        return False, f"no models block: {filepath}"

    new_content = update_models_block(content, models)
    new_content = update_codex_note(new_content)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True, f"{agent_id} ({category}) -> lead:{models['lead']} senior:{models['senior']} mid:{models['mid']} junior:{models['junior']} fallback:{models.get('fallback','sonnet')}"
    return False, f"no change: {filepath}"


def main():
    files = glob.glob(os.path.join(AGENTS_DIR, "**/AGENT.md"), recursive=True)
    updated = 0
    skipped = 0
    errors = []

    for f in sorted(files):
        success, msg = process_file(f)
        if success:
            updated += 1
            print(f"  OK: {msg}")
        else:
            skipped += 1
            if "no change" not in msg:
                errors.append(msg)

    print(f"\n=== Summary ===")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

    # Stats
    gpt_lead = 0
    claude_lead = 0
    for f in files:
        with open(f) as fh:
            c = fh.read()
        m = re.search(r'lead:\s+(\S+)', c)
        if m:
            val = m.group(1)
            if 'gpt' in val:
                gpt_lead += 1
            else:
                claude_lead += 1
    print(f"\nLead tier: GPT={gpt_lead}, Claude={claude_lead}")


if __name__ == "__main__":
    main()
