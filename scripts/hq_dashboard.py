#!/usr/bin/env python3
"""
hq dashboard — unified system state aggregator.

Sources merged:
  - config/telemetry/events/*.jsonl   (dispatch logs)
  - config/agent-registry.json         (source of truth: 196 agents)
  - Reports/*.json                     (optional audit outputs)
  - agents/AGENT_COVERAGE_AUDIT.md     (fallback, parsed for p0/p1 counts)

Writes config/telemetry/aggregated/dashboard.json and prints a short summary.
Flags: --json (json only), --watch (refresh every 60s).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


def find_base() -> Path:
    env_base = os.environ.get("CLAUDE_CONFIG_ROOT")
    if env_base and Path(env_base).exists():
        return Path(env_base)
    here = Path(__file__).resolve().parent.parent
    if (here / "config" / "agent-registry.json").exists():
        return here
    return Path.home() / "Projects" / "claude-config"


BASE = find_base()


def load_json(rel: str) -> dict:
    p = BASE / rel
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def load_events(days: int = 30) -> list[dict]:
    events: list[dict] = []
    event_dir = BASE / "config" / "telemetry" / "events"
    if not event_dir.exists():
        return events
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for f in sorted(event_dir.glob("*.jsonl")):
        try:
            for line in f.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                    ts = datetime.fromisoformat(ev["timestamp"])
                    if ts >= cutoff:
                        events.append(ev)
                except Exception:
                    continue
        except Exception:
            continue
    return events


def parse_coverage_md() -> dict:
    """Fallback: parse agents/AGENT_COVERAGE_AUDIT.md for P0/P1 counts."""
    p = BASE / "agents" / "AGENT_COVERAGE_AUDIT.md"
    if not p.exists():
        return {}
    try:
        body = p.read_text()
        out = {}
        for tier in ("P0", "P1", "P2", "OK"):
            m = re.search(rf"{tier}\s*[=:]\s*(\d+)", body)
            if m:
                out[f"tier_{tier.lower()}"] = int(m.group(1))
        return out
    except Exception:
        return {}


def parse_quality_md() -> dict:
    p = BASE / "agents" / "KNOWLEDGE_QUALITY_AUDIT.md"
    if not p.exists():
        return {}
    try:
        body = p.read_text()
        out = {}
        m = re.search(r"complete\s*=\s*(\d+)\s*/\s*(\d+)", body)
        if m:
            out["complete"] = int(m.group(1))
            out["total"] = int(m.group(2))
        return out
    except Exception:
        return {}


def build_dashboard() -> dict:
    registry = load_json("config/agent-registry.json")
    agents_map = registry.get("agents") or {}

    active_ids = [aid for aid, meta in agents_map.items() if meta.get("status") == "active"]
    pool_ids = [aid for aid, meta in agents_map.items() if meta.get("status") == "pool"]

    events = load_events(30)

    agent_usage = Counter(e.get("agent_id", "unknown") for e in events if e.get("agent_id") and e.get("agent_id") != "unknown")
    model_usage = Counter(e.get("model_used", "unknown") for e in events)
    project_usage = Counter(e.get("project", "unknown") for e in events)
    outcome_counts = Counter(e.get("outcome", "unknown") for e in events)
    category_usage = Counter(e.get("category", "unknown") for e in events if e.get("category") and e.get("category") != "unknown")
    tier_counts = Counter(e.get("model_tier", "unknown") for e in events)

    total = len(events)
    success = outcome_counts.get("success", 0)
    success_rate = (success / total) if total > 0 else 0.0

    used_ids = set(agent_usage.keys())
    never_used_active = [aid for aid in active_ids if aid not in used_ids]

    top_agents = agent_usage.most_common(10)

    daily: dict[str, int] = defaultdict(int)
    for e in events:
        day = str(e.get("timestamp", ""))[:10]
        if day:
            daily[day] += 1

    free_local = tier_counts.get("free", 0) + tier_counts.get("economy", 0)
    free_local_pct = round((free_local / total * 100), 1) if total > 0 else 0.0

    # Knowledge: prefer Reports/*.json, fall back to MD parsing
    knowledge_report = load_json("Reports/knowledge_quality.json") or parse_quality_md()
    coverage_report = load_json("Reports/agent_coverage.json") or parse_coverage_md()

    status = "healthy"
    if total > 0 and success_rate < 0.5:
        status = "critical"
    elif total > 0 and success_rate < 0.7:
        status = "degraded"
    elif total == 0:
        status = "unknown"

    dashboard = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period_days": 30,
        "base_path": str(BASE),
        "system_health": {
            "status": status,
            "success_rate": round(success_rate, 3),
            "total_dispatches": total,
        },
        "agents": {
            "registered": len(agents_map),
            "active": len(active_ids),
            "pool": len(pool_ids),
            "used_last_30d": len(used_ids),
            "never_used_active": never_used_active,
            "top_10": [{"id": aid, "dispatches": cnt} for aid, cnt in top_agents],
        },
        "models": {
            "usage": dict(model_usage),
            "tier_distribution": dict(tier_counts),
            "free_local_pct": free_local_pct,
        },
        "projects": {
            "active_projects": len(project_usage),
            "distribution": dict(project_usage.most_common(10)),
        },
        "categories": dict(category_usage.most_common()),
        "outcomes": dict(outcome_counts),
        "knowledge": {
            "quality": knowledge_report,
            "coverage": coverage_report,
        },
        "daily_trend": dict(sorted(daily.items())[-7:]),
    }

    out_dir = BASE / "config" / "telemetry" / "aggregated"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "dashboard.json").write_text(json.dumps(dashboard, indent=2, ensure_ascii=False))

    return dashboard


def print_summary(d: dict) -> None:
    h = d["system_health"]
    a = d["agents"]
    m = d["models"]

    icon = {"healthy": "OK", "degraded": "WARN", "critical": "CRIT", "unknown": "----"}
    print()
    print(f"[{icon.get(h['status'], '?')}] System: {h['status'].upper()} | "
          f"Success: {h['success_rate']*100:.1f}% | "
          f"Dispatches: {h['total_dispatches']}")
    print(f"Agents: {a['active']} active / {a['registered']} total | "
          f"{a['used_last_30d']} used (30d)")
    print(f"Models: {m.get('free_local_pct', 0)}% free/economy")

    if a["never_used_active"]:
        sample = ", ".join(a["never_used_active"][:5])
        more = f" (+{len(a['never_used_active'])-5} more)" if len(a["never_used_active"]) > 5 else ""
        print(f"Never-used active agents: {sample}{more}")

    if a["top_10"]:
        top = a["top_10"][0]
        print(f"Top agent: {top['id']} ({top['dispatches']} dispatches)")

    print()
    print(f"Dashboard -> config/telemetry/aggregated/dashboard.json")


def main() -> None:
    json_only = "--json" in sys.argv
    watch = "--watch" in sys.argv

    def once() -> None:
        d = build_dashboard()
        if json_only:
            print(json.dumps(d, indent=2, ensure_ascii=False))
        else:
            print_summary(d)

    if watch:
        try:
            while True:
                os.system("clear" if os.name != "nt" else "cls")
                once()
                time.sleep(60)
        except KeyboardInterrupt:
            pass
    else:
        once()


if __name__ == "__main__":
    main()
