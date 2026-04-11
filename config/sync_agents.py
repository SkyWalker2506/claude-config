#!/usr/bin/env python3
"""
sync_agents.py — Agent frontmatter ↔ agent-registry.json drift kontrolu.

Kullanim:
  python3 config/sync_agents.py --check        # uyumsuzluklari raporla
  python3 config/sync_agents.py --fix          # guvenli alanlari registry'ye senkronize et
  python3 config/sync_agents.py --stats        # ozet istatistik
"""

import json
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = REPO_ROOT / "config" / "agent-registry.json"
AGENTS_DIR = REPO_ROOT / "agents"

REQUIRED_FRONTMATTER_KEYS = [
    "id",
    "name",
    "category",
    "tier",
    "models",
    "refine_model",
    "mcps",
    "capabilities",
    "max_tool_calls",
    "status",
]
LIST_KEYS = {"mcps", "capabilities", "related", "fallbacks", "languages"}
SAFE_FIX_KEYS = {"name", "category", "status", "mcps", "capabilities", "max_tool_calls"}


def parse_inline_list(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1].strip()
    if not raw:
        return []
    parts = [part.strip() for part in raw.split(",")]
    return [part.strip("'\"") for part in parts if part]


def parse_scalar(key: str, raw: str):
    raw = raw.strip()
    if key in LIST_KEYS:
        return parse_inline_list(raw)
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def parse_frontmatter(filepath):
    """Parse top-level frontmatter keys from an AGENT.md file."""
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return None
    match = re.match(r"^---\n(.*?)\n---", content, re.S)
    if not match:
        return None
    fm_text = match.group(1)
    data = {}
    for line in fm_text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        data[key] = parse_scalar(key, raw)
    return data


def comparable_value(key, value):
    if key in LIST_KEYS:
        if isinstance(value, list):
            return sorted(str(v) for v in value)
        if value in (None, ""):
            return []
        return sorted(parse_inline_list(str(value)))
    if key == "max_tool_calls":
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    return "" if value is None else str(value).strip()


def fmt_value(value):
    if isinstance(value, list):
        return "[" + ", ".join(str(v) for v in value) + "]"
    return str(value)


def derive_legacy_primary_model(tier: str) -> str:
    tier = (tier or "mid").strip().lower()
    if tier == "junior":
        return "haiku"
    if tier == "senior":
        return "opus"
    return "sonnet"


def default_execution_backend(tier: str) -> dict:
    """Default execution backend for new agents (safe, no extra billing)."""
    # Routing is driven by execution_backends; keep new agents on Claude by default.
    # Can be manually upgraded to openai-codex-cli later.
    return {
        "execution_backends": {"primary": "claude", "fallback": ["local-free"]},
        "execution_mode": "claude_native",
        "billing_mode": "plan_included",
        "interaction_mode": "automated",
    }


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def save_registry(registry):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
        f.write("\n")


def collect_agent_files():
    """Return list of (path, frontmatter) for real agent files."""
    results = []
    for md_file in AGENTS_DIR.glob("*/*/AGENT.md"):
        if "_template" in str(md_file):
            continue
        fm = parse_frontmatter(md_file)
        if fm and "id" in fm:
            results.append((md_file, fm))
    return results


def check(fix=False):
    registry = load_registry()
    agents_reg = registry.get("agents", {})
    agent_files = collect_agent_files()

    errors = []
    warnings = []
    fixed = []

    # Build a map of id -> (path, frontmatter) from .md files
    md_map = {}
    for path, fm in agent_files:
        agent_id = fm["id"]
        if agent_id in md_map:
            errors.append(f"DUPLICATE ID: {agent_id} in {path} and {md_map[agent_id][0]}")
        md_map[agent_id] = (path, fm)

    # Check required frontmatter keys
    for agent_id, (path, fm) in md_map.items():
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in fm:
                errors.append(f"MISSING KEY '{key}' in {path.relative_to(REPO_ROOT)}")

    # Check .md files vs registry
    for agent_id, (path, fm) in md_map.items():
        if agent_id not in agents_reg:
            warnings.append(f"UNREGISTERED: {agent_id} ({fm.get('name', '?')}) in {path.relative_to(REPO_ROOT)}")
            if fix:
                agents_reg[agent_id] = {
                    "version": "1.0",
                    "name": fm.get("name", agent_id),
                    "category": fm.get("category", "unknown"),
                    # Legacy compat only; routing uses execution_backends.
                    "primary_model": derive_legacy_primary_model(fm.get("tier", "mid")),
                    "fallbacks": fm.get("fallbacks", []),
                    "mcps": fm.get("mcps", []),
                    "capabilities": fm.get("capabilities", []),
                    "max_tool_calls": int(fm.get("max_tool_calls", 10)),
                    "status": fm.get("status", "pool"),
                    "related": fm.get("related", []),
                    "tier": fm.get("tier", "mid"),
                    **default_execution_backend(fm.get("tier", "mid")),
                }
                fixed.append(f"ADDED to registry: {agent_id}")
        else:
            reg_entry = agents_reg[agent_id]
            for key in ("name", "category", "status", "tier", "mcps", "capabilities", "max_tool_calls"):
                reg_value = comparable_value(key, reg_entry.get(key))
                md_value = comparable_value(key, fm.get(key))
                if reg_value == md_value:
                    continue
                warnings.append(
                    f"{key.upper()} MISMATCH: {agent_id} "
                    f"registry='{fmt_value(reg_entry.get(key))}' md='{fmt_value(fm.get(key))}'"
                )
                if fix and key in SAFE_FIX_KEYS:
                    reg_entry[key] = fm.get(key)
                    fixed.append(f"FIXED {key} for {agent_id}")

            if "/" in str(fm.get("category", "")):
                warnings.append(
                    f"NON-CANONICAL CATEGORY: {agent_id} md='{fm.get('category')}' "
                    f"(top-level category expected)"
                )
            if "/" in str(reg_entry.get("category", "")):
                warnings.append(
                    f"NON-CANONICAL REGISTRY CATEGORY: {agent_id} registry='{reg_entry.get('category')}'"
                )

    # Check registry entries without .md files
    for agent_id in agents_reg:
        if agent_id not in md_map:
            warnings.append(f"REGISTRY ONLY (no .md): {agent_id} ({agents_reg[agent_id].get('name', '?')})")

    if fix and fixed:
        registry["agents"] = agents_reg
        save_registry(registry)

    return errors, warnings, fixed


def stats():
    registry = load_registry()
    agents_reg = registry.get("agents", {})
    agent_files = collect_agent_files()

    total_reg = len(agents_reg)
    total_md = len(agent_files)
    active = sum(1 for a in agents_reg.values() if a.get("status") == "active")
    pool = sum(1 for a in agents_reg.values() if a.get("status") == "pool")
    slash_categories = sum(1 for a in agents_reg.values() if "/" in str(a.get("category", "")))

    by_category = {}
    for a in agents_reg.values():
        cat = a.get("category", "unknown")
        by_category[cat] = by_category.get(cat, 0) + 1

    print(f"\n=== Agent Registry Stats ===")
    print(f"Registry entries : {total_reg}")
    print(f"Agent .md files  : {total_md}")
    print(f"Active           : {active}")
    print(f"Pool             : {pool}")
    print(f"Slash categories : {slash_categories}")
    print(f"\nBy category:")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat:<20} {count}")


def main():
    mode = "--check"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == "--stats":
        stats()
        return

    fix = mode == "--fix"
    errors, warnings, fixed = check(fix=fix)

    if errors:
        print("\n[ERRORS]")
        for e in errors:
            print(f"  ✗ {e}")

    if warnings:
        print("\n[WARNINGS]")
        for w in warnings:
            print(f"  ⚠ {w}")

    if fixed:
        print("\n[FIXED]")
        for f in fixed:
            print(f"  ✓ {f}")

    if not errors and not warnings:
        print("✓ Registry and agent files are in sync.")
    elif not errors and not fix:
        print(f"\n{len(warnings)} warning(s). Run with --fix to sync safe fields.")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
