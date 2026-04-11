#!/usr/bin/env python3
"""
PostToolUse hook: log agent dispatch events as JSONL.

Reads hook input from stdin (Claude Code hook protocol). Writes one event
line to config/telemetry/events/<YYYY-MM-DD>.jsonl. Never blocks, never
fails the tool call — errors are swallowed.

Agent metadata (id/name/category) is extracted from tool_input when the
parent called the Task tool. For other tools the agent fields are left
as "unknown" — the dashboard treats these as infra noise, not dispatches.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def find_base() -> Path:
    env_base = os.environ.get("CLAUDE_CONFIG_ROOT")
    if env_base and Path(env_base).exists():
        return Path(env_base)
    here = Path(__file__).resolve().parent.parent
    if (here / "config" / "agent-registry.json").exists():
        return here
    return Path.home() / "Projects" / "claude-config"


MODEL_TIER = {
    "opus": "premium",
    "claude-opus-4-6": "premium",
    "claude-opus-4-5": "premium",
    "sonnet": "standard",
    "claude-sonnet-4-6": "standard",
    "claude-sonnet-4-5": "standard",
    "haiku": "economy",
    "claude-haiku-4-5": "economy",
}


def tier_for(model: str) -> str:
    if not model or model == "unknown":
        return "unknown"
    lower = model.lower()
    for key, tier in MODEL_TIER.items():
        if key in lower:
            return tier
    if any(tag in lower for tag in ("free", "openrouter", "groq", "ollama", "local", "qwen", "gemma", "llama")):
        return "free"
    return "unknown"


def extract_agent(hook_input: dict) -> tuple[str, str, str]:
    """Return (agent_id, agent_name, category). Best-effort parse."""
    tool_input = hook_input.get("tool_input") or {}
    desc = tool_input.get("description", "") or ""
    prompt = tool_input.get("prompt", "") or ""
    subagent = tool_input.get("subagent_type", "") or ""

    # Look for "[X## NameOfAgent" pattern from agent-dispatch.md header
    aid = "unknown"
    aname = subagent or "unknown"
    for line in (prompt[:800] + "\n" + desc).splitlines():
        line = line.strip()
        if line.startswith("AGENT:"):
            rest = line.replace("AGENT:", "").strip()
            if "—" in rest:
                left, right = rest.split("—", 1)
                aid = left.strip() or aid
                aname = right.strip() or aname
            else:
                aid = rest or aid
            break

    # Category lookup from registry if we got an id
    category = "unknown"
    if aid != "unknown":
        try:
            base = find_base()
            reg = json.loads((base / "config" / "agent-registry.json").read_text())
            meta = (reg.get("agents") or {}).get(aid) or {}
            category = meta.get("category", "unknown")
            if aname == "unknown":
                aname = meta.get("name", "unknown")
        except Exception:
            pass

    return aid, aname, category


def main() -> None:
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw.strip() else {}
    except Exception:
        return  # silent no-op

    try:
        tool_name = hook_input.get("tool_name", "unknown")
        tool_response = hook_input.get("tool_response") or {}

        # Derive outcome: PostToolUse fires after tool completes.
        # Failure signals: is_error flag or exception text.
        outcome = "success"
        if isinstance(tool_response, dict):
            if tool_response.get("is_error") or tool_response.get("error"):
                outcome = "failed"
        elif isinstance(tool_response, str) and "error" in tool_response.lower()[:100]:
            outcome = "failed"

        agent_id, agent_name, category = extract_agent(hook_input)

        model = os.environ.get("CLAUDE_MODEL") or hook_input.get("model") or "unknown"
        project = os.path.basename(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())

        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "agent_name": agent_name,
            "category": category,
            "model_used": model,
            "model_tier": tier_for(model),
            "project": project,
            "task_type": tool_name,
            "outcome": outcome,
            "duration_seconds": float(hook_input.get("duration", 0) or 0),
            "fallback_used": False,
            "fallback_chain": [],
        }

        base = find_base()
        log_dir = base / "config" / "telemetry" / "events"
        log_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with (log_dir / f"{today}.jsonl").open("a") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        return  # never fail the tool call


if __name__ == "__main__":
    main()
