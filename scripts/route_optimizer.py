#!/usr/bin/env python3
"""
Route optimizer — challenge agent-registry.json model assignments
using dispatch telemetry.

Scoring: if an alternate model reaches >=95% of current success rate
at lower relative cost and with >=5 samples, recommend a swap.

Reads config/telemetry/events/*.jsonl + config/agent-registry.json.
Writes Reports/routing_recommendations.json.
"""
from __future__ import annotations

import json
import os
from collections import defaultdict
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

# Relative cost weights (opus normalized to 1.0)
MODEL_COST = {
    "opus": 1.0,
    "claude-opus-4-6": 1.0,
    "claude-opus-4-5": 1.0,
    "sonnet": 0.4,
    "claude-sonnet-4-6": 0.4,
    "claude-sonnet-4-5": 0.4,
    "haiku": 0.1,
    "claude-haiku-4-5": 0.1,
}


def cost_for(model: str) -> float:
    if not model:
        return 0.5
    lower = model.lower()
    for key, c in MODEL_COST.items():
        if key in lower:
            return c
    if any(tag in lower for tag in ("free", "openrouter", "groq", "ollama", "local", "qwen", "gemma", "llama")):
        return 0.0
    return 0.5


def load_events(days: int = 60) -> list[dict]:
    events: list[dict] = []
    event_dir = BASE / "config" / "telemetry" / "events"
    if not event_dir.exists():
        return events
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for f in event_dir.glob("*.jsonl"):
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


def analyze() -> list[dict]:
    events = load_events(60)
    if not events:
        return []

    perf: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"total": 0, "success": 0, "duration": 0.0}
    )
    for e in events:
        aid = e.get("agent_id")
        model = e.get("model_used")
        if not aid or aid == "unknown" or not model or model == "unknown":
            continue
        key = (aid, model)
        p = perf[key]
        p["total"] += 1
        if e.get("outcome") == "success":
            p["success"] += 1
        p["duration"] += float(e.get("duration_seconds", 0) or 0)

    agents: dict[str, dict] = defaultdict(dict)
    for (aid, model), stats in perf.items():
        sr = stats["success"] / stats["total"] if stats["total"] > 0 else 0
        agents[aid][model] = {
            "success_rate": sr,
            "avg_duration": stats["duration"] / stats["total"] if stats["total"] > 0 else 0,
            "total": stats["total"],
        }

    registry = json.loads((BASE / "config" / "agent-registry.json").read_text())
    agents_map = registry.get("agents") or {}
    assigned_model = {aid: meta.get("primary_model", "sonnet") for aid, meta in agents_map.items()}

    recs: list[dict] = []
    for aid, models in agents.items():
        current = assigned_model.get(aid, "sonnet")
        # Find the best stats we can match against the registry's current model
        current_stats = None
        for m, s in models.items():
            if current.lower() in m.lower() or m.lower() in current.lower():
                current_stats = s
                break
        if current_stats is None or current_stats["total"] < 3:
            continue

        cur_cost = cost_for(current)
        cur_sr = current_stats["success_rate"]

        for alt_model, alt_stats in models.items():
            if alt_stats["total"] < 5:
                continue
            if current.lower() in alt_model.lower():
                continue
            alt_cost = cost_for(alt_model)
            if alt_cost >= cur_cost:
                continue
            if alt_stats["success_rate"] < cur_sr * 0.95:
                continue
            savings = ((cur_cost - alt_cost) / cur_cost * 100) if cur_cost > 0 else 0
            recs.append({
                "agent_id": aid,
                "current_model": current,
                "recommended_model": alt_model,
                "current_sr": round(cur_sr, 3),
                "alt_sr": round(alt_stats["success_rate"], 3),
                "cost_savings_pct": round(savings, 1),
                "sample_size": alt_stats["total"],
            })

    return recs


def main() -> None:
    recs = analyze()

    print()
    print("Route Optimization Analysis")
    print("=" * 50)

    if recs:
        for r in recs:
            print(f"\n  {r['agent_id']}: {r['current_model']} -> {r['recommended_model']}")
            print(f"    Success: {r['current_sr']*100:.1f}% -> {r['alt_sr']*100:.1f}%")
            print(f"    Cost savings: {r['cost_savings_pct']}%")
            print(f"    Sample: {r['sample_size']} dispatches")
    else:
        print("\nNo routing changes recommended (insufficient data or already optimal).")

    out_dir = BASE / "Reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "routing_recommendations.json"
    out.write_text(json.dumps(recs, indent=2, ensure_ascii=False))
    print(f"\nReport -> Reports/routing_recommendations.json")


if __name__ == "__main__":
    main()
