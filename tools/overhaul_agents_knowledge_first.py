#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"

PROTECTED = {
    "orchestrator/jarvis",
    "backend/frontend-coder",
    "backend/mobile-dev-agent",
    "design/design-system-agent",
    "design/motion-graphics-agent",
    "design/ui-ux-researcher",
    "devops/github-manager",
    "research/ai-tool-evaluator",
    "prompt-engineering/ai-systems-architect",
    "prompt-engineering/prompt-engineer",
    "prompt-engineering/skill-design-specialist",
    "prompt-engineering/workflow-engineer",
}


def today() -> str:
    return dt.date.today().isoformat()


def ascii_tr(s: str) -> str:
    # Turkish -> ASCII-safe mapping per prompt.
    table = str.maketrans(
        {
            "ı": "i",
            "İ": "I",
            "ş": "s",
            "Ş": "S",
            "ç": "c",
            "Ç": "C",
            "ğ": "g",
            "Ğ": "G",
            "ü": "u",
            "Ü": "U",
            "ö": "o",
            "Ö": "O",
        }
    )
    return s.translate(table)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write_text(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def split_frontmatter(md: str) -> tuple[str, str]:
    m = re.search(r"^---\n([\s\S]*?)\n---\n", md)
    if not m:
        return "", md
    fm = md[: m.end()]
    body = md[m.end() :].lstrip("\n")
    return fm, body


def parse_frontmatter_top(md: str) -> dict[str, Any]:
    fm, _ = split_frontmatter(md)
    if not fm:
        return {}
    inner = fm.splitlines()[1:-1]
    out: dict[str, Any] = {}
    for line in inner:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def parse_flow_list(v: str) -> list[str]:
    v = v.strip()
    if not v:
        return []
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
    else:
        inner = v
    if not inner:
        return []
    parts = [p.strip() for p in inner.split(",")]
    out: list[str] = []
    for p in parts:
        if not p:
            continue
        if (p[0] == p[-1]) and p[0] in ("'", '"'):
            p = p[1:-1]
        out.append(p)
    return out


@dataclass(frozen=True)
class AgentMeta:
    agent_id: str
    name: str
    category: str
    related: list[str]
    capabilities: list[str]


def meta_from_file(agent_md: Path) -> AgentMeta:
    txt = read_text(agent_md)
    fm = parse_frontmatter_top(txt)
    agent_id = fm.get("id", "").strip()
    name = fm.get("name", "").strip() or agent_md.parent.name
    category = fm.get("category", "").strip() or agent_md.parent.parent.name
    rel = parse_flow_list(fm.get("related", ""))
    caps = parse_flow_list(fm.get("capabilities", ""))
    return AgentMeta(agent_id=agent_id, name=name, category=category, related=rel, capabilities=caps)


def default_bridges(meta: AgentMeta) -> list[tuple[str, str]]:
    # 2-3 references, prefer related; else category defaults.
    bridges: list[str] = []
    for r in meta.related:
        if r and r != meta.agent_id:
            bridges.append(r)
    # fallbacks
    fallbacks = ["A2", "A1", "B2", "B1", "B13", "B3", "I1", "K1", "N6"]
    for f in fallbacks:
        if f != meta.agent_id and f not in bridges:
            bridges.append(f)
    chosen = bridges[:3]
    # Describe intersection briefly.
    desc: dict[str, str] = {
        "A1": "stratejik karar ve risk escalation",
        "A2": "routing ve dispatch kurallari",
        "B1": "mimari karar ve sistem tasarimi",
        "B2": "implementasyon detaylari ve delivery",
        "B3": "UI contract ve component entegrasyonu",
        "B13": "guvenlik risk analizi",
        "I1": "Jira akisi ve ticket hijyeni",
        "K1": "web arastirma ve kaynak derleme",
        "N6": "agent/memory mimarisi",
    }
    out: list[tuple[str, str]] = []
    for cid in chosen:
        out.append((cid, desc.get(cid, "kesisim noktasi")))
    return out


def build_agent_body(meta: AgentMeta) -> str:
    # Domain hint from name + capabilities.
    caps = meta.capabilities[:]
    cap_hint = ", ".join(caps[:6]) if caps else "domain"

    bridges = default_bridges(meta)

    identity = (
        f"{meta.name} ({meta.agent_id}) icin domain-odakli uzman. "
        f"Bu rol pratikte \"{meta.name}\" benzeri bir specialist olarak konumlanir. "
        f"Odak alanlari: {cap_hint}. "
        f"Gorevlerde hedef: net kabul kriteri, dogrulanabilir cikti, minimum risk."
    )

    always_rules = [
        "Gorev hedefini kabul kriteriyle netlestir",
        "Once mevcut sistem/artefact oku (config, docs, code, ticket)",
        "Degisiklikleri kucuk ve geri alinabilir tut",
        "Ciktiyi dogrula (lint/test/runbook/checklist)",
    ]
    never_rules = [
        "Scope disina tasma; uygun agent'a yonlendir",
        "Kritik degisiklikte insan onayi olmadan ilerleme",
        "Knowledge dosyasina uydurma bilgi yazma",
    ]

    # Process phases vary lightly by category.
    phase1 = "Discovery"
    phase2 = "Execution"
    if meta.category in {"code-review"}:
        phase1, phase2 = "Review", "FixProposal"
    elif meta.category in {"jira-pm"}:
        phase1, phase2 = "Triage", "Plan"
    elif meta.category in {"market-research", "research"}:
        phase1, phase2 = "Research", "Synthesis"
    elif meta.category in {"devops", "ai-ops"}:
        phase1, phase2 = "Diagnose", "Remediate"
    elif meta.category in {"design", "3d-cad"}:
        phase1, phase2 = "Brief", "Produce"

    output_example = (
        "```text\n"
        f"[{meta.agent_id}] {meta.name}\n"
        "Summary:\n"
        "- ...\n"
        "Deliverables:\n"
        "- file/path.ext\n"
        "- checklist items\n"
        "Risks:\n"
        "- ...\n"
        "```\n"
    )

    when_to_use = [
        f"{cap_hint} kapsaminda implementasyon/analiz gerektiginde",
        "Mevcut davranis beklenenden sapinca (bug/regression)",
        "Net deliverable uretilecekse (PR, doc, checklist)",
        "Tek kategoride derin uzmanlik gerekince",
    ]
    when_not = [
        "Stratejik/mimari karar gerekiyorsa → A1 veya B1",
        "Guvenlik/kvkk riski varsa → B13",
        "Routing belirsizse → A2",
    ]

    red_flags = [
        "Belirsiz kabul kriteri",
        "Kritik degisiklik icin rollback plani yok",
        "Tek degisiklik 3+ sistemi etkiliyor",
        "Gerekli kaynak/secret/izin eksik",
        "Ayni hata 2+ kez tekrarlandi",
    ]

    verification = [
        "Cikti calisiyor ve tekrar edilebilir",
        "Scope disina cikilmadi",
        "Log/test/lint temiz",
        "Dokumantasyon/rapor guncel",
    ]

    error_handling = [
        f"{phase1} basarisiz → eksik input listele, K1 ile kaynak topla",
        f"{phase2} basarisiz → degisiklikleri parcala, en kucuk teslimatla devam et",
        "Genel hata → A1'e escalate veya kullaniciya sor",
    ]

    escalation = [
        "Mimari karar → B1 (Backend Architect) / A1 (Lead Orchestrator)",
        "Guvenlik riski → B13 (Security Auditor)",
        "Belirsiz scope → A2 (Task Router)",
        "Son care → kullaniciya sor",
    ]

    md = []
    md.append(f"# {meta.name}")
    md.append("")
    md.append("## Identity")
    md.append(ascii_tr(identity))
    md.append("")
    md.append("## Boundaries")
    md.append("")
    md.append("### Always")
    md.append("- Gorev oncesi `knowledge/_index.md` oku, ilgili dosyalari yukle")
    md.append("- Is bittikten sonra onemli kararlari `memory/sessions.md`'ye yaz")
    md.append("- Yeni ogrenilenler varsa `memory/learnings.md`'ye kaydet")
    for r in always_rules:
        md.append(f"- {ascii_tr(r)}")
    md.append("")
    md.append("### Never")
    md.append("- Kendi alani disinda knowledge dosyasi yazma/guncelleme")
    md.append("- Baska agent'in sorumlulugundaki kararlari alma")
    md.append("- Dogrulanmamis bilgiyi knowledge dosyasina yazma")
    for r in never_rules:
        md.append(f"- {ascii_tr(r)}")
    md.append("")
    md.append("### Bridge")
    for bid, bdesc in bridges:
        md.append(f"- {bid}: {ascii_tr(bdesc)}")
    md.append("")
    md.append("## Process")
    md.append("")
    md.append("### Phase 0 — Pre-flight")
    md.append("- Gerekli dosyalar mevcut mu kontrol et (AGENT.md, knowledge/_index.md)")
    md.append("- Varsayimlarini listele — sessizce yanlis yola girme")
    md.append("- Eksik veri varsa dur, sor")
    md.append(f"- {ascii_tr('Gorev kapsaminda gereken artefact listesi cikar')}")
    md.append("")
    md.append(f"### Phase 1 — {phase1}")
    md.append(ascii_tr("1. Inputlari topla (ticket, repro, log, beklenti)"))
    md.append(ascii_tr("2. Risk ve bagimliliklari belirle"))
    md.append(ascii_tr("3. Basari kriterlerini yaz"))
    md.append("")
    md.append(f"### Phase 2 — {phase2}")
    md.append(ascii_tr("1. En kucuk degisiklikle ilerle"))
    md.append(ascii_tr("2. Alternatifleri kisa trade-off ile sec"))
    md.append(ascii_tr("3. Ciktiyi uret (PR/doc/komut seti)"))
    md.append("")
    md.append("### Phase 3 — Finalize")
    md.append(ascii_tr("1. Verification checklist calistir"))
    md.append(ascii_tr("2. Karar ve ogrenimleri memory'e yaz"))
    md.append(ascii_tr("3. Kullaniciya net ozet + sonraki adim ver"))
    md.append("")
    md.append("## Output Format")
    md.append(ascii_tr("Cikti: ozet + deliverable listesi + risk/next steps."))
    md.append("")
    md.append(output_example.rstrip())
    md.append("")
    md.append("## When to Use")
    for w in when_to_use:
        md.append(f"- {ascii_tr(w)}")
    md.append("")
    md.append("## When NOT to Use")
    for w in when_not:
        md.append(f"- {ascii_tr(w)}")
    md.append("")
    md.append("## Red Flags")
    for r in red_flags:
        md.append(f"- {ascii_tr(r)}")
    md.append("")
    md.append("## Verification")
    for v in verification:
        md.append(f"- [ ] {ascii_tr(v)}")
    md.append("")
    md.append("## Error Handling")
    for e in error_handling:
        md.append(f"- {ascii_tr(e)}")
    md.append("")
    md.append("## Escalation")
    for e in escalation:
        md.append(f"- {ascii_tr(e)}")
    md.append("")
    md.append("## Knowledge Index")
    md.append("> `knowledge/_index.md` dosyasina bak — ihtiyacin olan konuyu yukle")
    md.append("")
    return "\n".join(md)


def knowledge_topics(meta: AgentMeta) -> list[tuple[str, str, str]]:
    # 3 topics per agent, deterministic.
    caps = meta.capabilities
    base = caps[0] if caps else meta.category
    t1 = (f"{meta.name} Core Patterns", f"{base}-core-patterns.md", f"Core patterns for {meta.name}")
    t2 = (f"{meta.name} Anti-Patterns", f"{base}-anti-patterns.md", f"Common mistakes and anti-patterns")
    t3 = (f"{meta.name} Verification Checklist", f"{base}-verification.md", f"Verification and delivery checklist")
    # Make filenames safe
    out = []
    for title, fn, desc in (t1, t2, t3):
        fn = re.sub(r"[^a-z0-9\\-\\.]", "-", fn.lower())
        fn = re.sub(r"-+", "-", fn).strip("-")
        out.append((title, fn, desc))
    return out


def build_knowledge_file(title: str, domain: str) -> str:
    # English technical reference with table + snippet + checklist.
    t = []
    t.append("---")
    t.append(f"last_updated: {today()}")
    t.append("refined_by: cursor")
    t.append("confidence: medium")
    t.append("---")
    t.append("")
    t.append(f"# {title}")
    t.append("")
    t.append("## Best practices")
    t.append(f"- Prefer small, composable steps for {domain}.")
    t.append("- Make failure modes explicit.")
    t.append("- Write down assumptions and verification upfront.")
    t.append("")
    t.append("## Patterns")
    t.append("")
    t.append("| Situation | Recommended pattern | Why |")
    t.append("|----------|----------------------|-----|")
    t.append(f"| Unknown scope | Start with inventory + minimal repro | Avoid premature optimization |")
    t.append(f"| Risky change | Feature-flag / rollback plan | Reduce blast radius |")
    t.append(f"| Repeated tasks | Script the workflow | Consistency and speed |")
    t.append("")
    t.append("### Example snippet")
    t.append("")
    t.append("```bash")
    t.append("# Capture context quickly")
    t.append("git status")
    t.append("git diff")
    t.append("```")
    t.append("")
    t.append("## Anti-patterns")
    t.append("- Changing multiple concerns in one step.")
    t.append("- Skipping verification because it \"looks right\".")
    t.append("- Writing docs that drift from reality.")
    t.append("")
    t.append("## Decision checklist")
    t.append("- [ ] Do we have clear acceptance criteria?")
    t.append("- [ ] What can break and how do we roll back?")
    t.append("- [ ] What is the minimal safe change?")
    t.append("- [ ] How will we verify success?")
    t.append("")
    return "\n".join(t)


def update_index(index_path: Path, topics: list[tuple[str, str, str]]) -> None:
    header = ["---", f"last_updated: {today()}", f"total_topics: {len(topics)}", "---", "", "# Knowledge Index", ""]
    lines = header[:]
    for title, fn, desc in topics:
        lines.append(f"- [{title}]({fn}) — {desc}")
    lines.append("")
    write_text(index_path, "\n".join(lines))


def overhaul_agent(agent_dir: Path, *, dry_run: bool) -> bool:
    rel = f"{agent_dir.parent.name}/{agent_dir.name}"
    if rel in PROTECTED:
        return False
    agent_md = agent_dir / "AGENT.md"
    if not agent_md.exists():
        return False
    txt = read_text(agent_md)
    fm, _ = split_frontmatter(txt)
    if not fm:
        return False

    meta = meta_from_file(agent_md)
    body = build_agent_body(meta)
    new_txt = fm.rstrip() + "\n\n" + body.strip() + "\n"

    # Knowledge files
    kdir = agent_dir / "knowledge"
    topics = knowledge_topics(meta)

    if dry_run:
        print(f"[DRY] overhaul {rel} -> {meta.agent_id}")
        return True

    write_text(agent_md, new_txt)

    for title, fn, _desc in topics:
        kpath = kdir / fn
        if not kpath.exists():
            write_text(kpath, build_knowledge_file(title, domain=meta.name))

    update_index(kdir / "_index.md", topics)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cat_dir = AGENTS_DIR / args.category
    if not cat_dir.exists():
        raise SystemExit(f"Missing category: {args.category}")

    changed = 0
    for agent_dir in sorted([p for p in cat_dir.iterdir() if p.is_dir() and p.name != "_template"]):
        if overhaul_agent(agent_dir, dry_run=args.dry_run):
            changed += 1
    print(f"overhauled_count {changed}")


if __name__ == "__main__":
    main()

