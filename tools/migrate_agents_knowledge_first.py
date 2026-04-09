#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
TEMPLATE_DIR = AGENTS_DIR / "_template"


def _today_iso() -> str:
    return dt.date.today().isoformat()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value[0] == "[" and value[-1] == "]":
        inner = value[1:-1].strip()
    else:
        inner = value
    if not inner:
        return []
    parts = [p.strip() for p in inner.split(",")]
    out: list[str] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if (p[0] == p[-1]) and p[0] in ("'", '"'):
            p = p[1:-1]
        out.append(p)
    return out


def _parse_frontmatter(md: str) -> tuple[dict[str, Any], str]:
    # Expects optional YAML frontmatter between --- lines.
    lines = md.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, md
    try:
        end_idx = lines[1:].index("---") + 1
    except ValueError:
        return {}, md
    fm_lines = lines[1:end_idx]
    rest = "\n".join(lines[end_idx + 1 :]).lstrip("\n")

    data: dict[str, Any] = {}
    for raw in fm_lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val.lower() in ("true", "false"):
            data[key] = val.lower() == "true"
            continue
        if re.fullmatch(r"-?\d+", val):
            data[key] = int(val)
            continue
        if val.startswith("[") and val.endswith("]"):
            data[key] = _parse_inline_list(val)
            continue
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            data[key] = val[1:-1]
            continue
        data[key] = val
    return data, rest


def _extract_sections(md_body: str) -> dict[str, str]:
    # Normalize Turkish headings (Amac/Amaç).
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in md_body.splitlines():
        m = re.match(r"^##\s+(.*)\s*$", line)
        if m:
            if current:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
            continue
        if current is not None:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf).strip()

    # Alias keys.
    aliases = {
        "Amac": "Amac",
        "Amaç": "Amac",
        "Kapsam": "Kapsam",
        "Escalation": "Escalation",
        "Eskalasyon": "Escalation",
    }
    out: dict[str, str] = {}
    for k, v in sections.items():
        key = aliases.get(k, k)
        out[key] = v
    return out


def _tier_from_primary_model(primary_model: str | None) -> str:
    if not primary_model:
        return "mid"
    m = primary_model.lower()
    if "opus" in m:
        return "senior"
    if "haiku" in m:
        return "junior"
    return "mid"


def _format_yaml_list(items: list[str]) -> str:
    return "[" + ", ".join(items) + "]"


def _format_yaml_flow_seq(items: list[str], *, quote: set[str] | None = None) -> str:
    q = quote or set()
    out: list[str] = []
    for it in items:
        s = str(it)
        if s in q:
            out.append(f"\"{s}\"")
        else:
            out.append(s)
    return "[" + ", ".join(out) + "]"


def _safe_slug(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "topic"


@dataclass(frozen=True)
class AgentOld:
    path: Path
    fm: dict[str, Any]
    sections: dict[str, str]

    @property
    def category(self) -> str:
        return str(self.fm.get("category") or self.path.parent.name)

    @property
    def id(self) -> str:
        return str(self.fm.get("id") or "").strip()

    @property
    def name(self) -> str:
        n = self.fm.get("name")
        if n:
            return str(n).strip()
        # Fallback: title line.
        m = re.search(r"^#\s+(.+)$", _read_text(self.path), flags=re.M)
        if m:
            return m.group(1).strip()
        return self.path.stem

    @property
    def related(self) -> list[str]:
        val = self.fm.get("related")
        if isinstance(val, list):
            return [str(x) for x in val]
        if isinstance(val, str):
            return _parse_inline_list(val)
        return []


def _agent_new_dir(old_path: Path) -> Path:
    return old_path.with_suffix("")  # agents/{category}/{agent}


def _build_agent_md(old: AgentOld) -> str:
    purpose = old.sections.get("Amac", "").strip()
    scope = old.sections.get("Kapsam", "").strip()
    escalation = old.sections.get("Escalation", "").strip()

    primary_model = old.fm.get("primary_model")
    tier = _tier_from_primary_model(str(primary_model) if primary_model else None)

    # New frontmatter follows agents/_template/AGENT.md.
    fm_lines: list[str] = [
        "---",
        f"id: {old.id}" if old.id else "id: {ID}",
        f"name: {old.name}",
        f"category: {old.category}",
        f"tier: {tier}",
        "models:",
        "  senior: opus",
        "  mid: sonnet",
        "  junior: haiku",
        "refine_model: opus",
    ]

    mcps = old.fm.get("mcps")
    if isinstance(mcps, list):
        fm_lines.append(f"mcps: {_format_yaml_flow_seq([str(x) for x in mcps], quote={'*'})}")
    elif isinstance(mcps, str):
        fm_lines.append(f"mcps: {_format_yaml_flow_seq(_parse_inline_list(mcps), quote={'*'})}")
    else:
        fm_lines.append("mcps: []")

    capabilities = old.fm.get("capabilities")
    if isinstance(capabilities, list):
        fm_lines.append(f"capabilities: {_format_yaml_list([str(x) for x in capabilities])}")
    elif isinstance(capabilities, str):
        fm_lines.append(f"capabilities: {_format_yaml_list(_parse_inline_list(capabilities))}")
    else:
        fm_lines.append("capabilities: []")

    max_tool_calls = old.fm.get("max_tool_calls")
    if isinstance(max_tool_calls, int):
        fm_lines.append(f"max_tool_calls: {max_tool_calls}")

    if old.related:
        fm_lines.append(f"related: {_format_yaml_list(old.related)}")

    status = old.fm.get("status")
    if status:
        fm_lines.append(f"status: {status}")
    else:
        fm_lines.append("status: pool")
    fm_lines.append("---")

    always = [
        "Gorev oncesi `knowledge/_index.md` oku, ilgili dosyalari yukle",
        "Is bittikten sonra onemli kararlari `memory/sessions.md`'ye yaz",
        "Yeni ogrenilenler varsa `memory/learnings.md`'ye kaydet",
    ]
    if scope:
        for sline in scope.splitlines():
            sline = sline.strip()
            if sline.startswith("-"):
                always.append(sline[1:].strip())

    never = [
        "Kendi alani disinda knowledge dosyasi yazma/guncelleme",
        "Baska agent'in sorumlulugundaki kararlari alma",
        "Dogrulanmamis bilgiyi knowledge dosyasina yazma",
    ]

    out = "\n".join(fm_lines) + "\n\n"
    out += f"# {old.name}\n\n"
    out += "## Identity\n"
    out += (purpose + "\n") if purpose else "{1-3 cumle — ben kimim, ne yaparim, neden varim.}\n"
    out += "\n## Boundaries\n\n### Always\n"
    out += "\n".join([f"- {x}" for x in always]) + "\n\n### Never\n"
    out += "\n".join([f"- {x}" for x in never]) + "\n\n### Bridge\n"
    out += "{Hangi alanlarla, hangi noktada kesisim var}\n\n"
    out += "## Process\n\n### Phase 0 — Pre-flight\n"
    out += "- Gerekli dosyalar mevcut mu kontrol et (AGENT.md, knowledge/_index.md)\n"
    out += "- Varsayimlarini listele — sessizce yanlis yola girme\n"
    out += "- Eksik veri varsa dur, sor\n\n"
    out += "### Phase 1-N — Execution\n"
    out += "1. Gorevi anla — ne isteniyor, kabul kriterleri ne\n"
    out += "2. `knowledge/_index.md` oku — sadece ilgili dosyalari yukle (lazy-load)\n"
    out += "3. Eksik bilgi varsa arastir (web, kod, dokumantasyon)\n"
    out += "4. **Gate:** Yeterli bilgi var mi? Yoksa dur, sor.\n"
    out += "5. Gorevi uygula\n"
    out += "6. **Gate:** Sonucu dogrula (Verification'a gore)\n"
    out += "7. Onemli kararlari/ogrenimleri memory'ye kaydet\n\n"
    out += "## Output Format\n"
    out += "{Ciktinin formati — dosya/commit/PR/test raporu.}\n\n"
    out += "## When to Use\n"
    if scope:
        bullets = [ln.strip() for ln in scope.splitlines() if ln.strip().startswith("-")]
        if bullets:
            out += "\n".join([f"- {b[1:].strip()}" for b in bullets[:8]]) + "\n"
        else:
            out += "- {Bu agent ne zaman cagrilmali}\n"
    else:
        out += "- {Bu agent ne zaman cagrilmali}\n"
    out += "\n## When NOT to Use\n"
    out += "- Gorev scope disindaysa → Escalation'a gore dogru agenta yonlendir\n\n"
    out += "## Red Flags\n"
    out += "- Scope belirsizligi varsa — dur, netlestir\n"
    out += "- Knowledge yoksa — uydurma bilgi uretme\n\n"
    out += "## Verification\n"
    out += "- [ ] Cikti beklenen formatta\n"
    out += "- [ ] Scope disina cikilmadi\n"
    out += "- [ ] Gerekli dogrulama yapildi\n\n"
    out += "## Error Handling\n"
    out += "- Parse/implement sorununda → minimal teslim et, blocker'i raporla\n"
    out += "- 3 basarisiz deneme → escalate et\n\n"
    out += "## Escalation\n"
    out += (escalation + "\n") if escalation else "- {Kime, ne zaman}\n"
    out += "\n## Knowledge Index\n"
    out += "> `knowledge/_index.md` dosyasina bak — ihtiyacin olan konuyu yukle\n"
    return out


def _build_knowledge_index(old: AgentOld) -> str:
    tmpl = _read_text(TEMPLATE_DIR / "knowledge" / "_index.md")
    content = tmpl.replace("{DATE}", _today_iso())

    topics: list[str] = []
    caps = old.fm.get("capabilities")
    if isinstance(caps, list):
        topics = [str(x) for x in caps[:5]]
    elif isinstance(caps, str):
        topics = _parse_inline_list(caps)[:5]

    if not topics:
        topics = ["overview", "workflow", "verification"]

    lines = content.splitlines()
    out_lines: list[str] = []
    inserted = False
    for ln in lines:
        out_lines.append(ln)
        if ln.strip().startswith("<!-- Format:"):
            continue
    # Append planned topics at end.
    out_lines.append("")
    out_lines.append("<!-- Planned topics -->")
    for t in topics[:5]:
        out_lines.append(f"- (planned) {t} — {_safe_slug(t)}.md")
    return "\n".join(out_lines).rstrip() + "\n"


def _copy_memory_templates(dst_dir: Path) -> None:
    mem_tmpl = TEMPLATE_DIR / "memory"
    for name in ("sessions.md", "learnings.md", "refinements.md"):
        src = mem_tmpl / name
        if src.exists():
            _write_text(dst_dir / "memory" / name, _read_text(src))


def migrate_category(category: str, *, dry_run: bool) -> int:
    cat_dir = AGENTS_DIR / category
    if not cat_dir.exists() or not cat_dir.is_dir():
        raise SystemExit(f"Category not found: {category}")

    old_paths = sorted(
        p
        for p in cat_dir.glob("*.md")
        if p.name.lower() != "readme.md" and p.name.lower() != "agent.md"
    )

    changed = 0
    for old_path in old_paths:
        md = _read_text(old_path)
        fm, body = _parse_frontmatter(md)
        sections = _extract_sections(body)
        old = AgentOld(path=old_path, fm=fm, sections=sections)

        new_dir = _agent_new_dir(old_path)
        agent_md = new_dir / "AGENT.md"
        if agent_md.exists():
            # Already migrated.
            continue

        if dry_run:
            print(f"[DRY] {old_path} -> {agent_md}")
            changed += 1
            continue

        # Create files.
        _write_text(agent_md, _build_agent_md(old))
        _write_text(new_dir / "knowledge" / "_index.md", _build_knowledge_index(old))
        _copy_memory_templates(new_dir)

        # Remove old file.
        old_path.unlink()
        changed += 1

    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True, help="agents/<category> (e.g. backend)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    n = migrate_category(args.category, dry_run=args.dry_run)
    print(f"migrated_count {n}")


if __name__ == "__main__":
    main()

