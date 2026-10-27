#!/usr/bin/env bash
# Lane availability tracker. Stops us hammering a lane whose quota is spent, without
# forgetting it forever. Written 2026-10-27.
#
#   lane.sh status                      one line per lane, for the prompt hook
#   lane.sh cool <lane> [min] [reason]  mark unusable for N minutes (default 30)
#   lane.sh block <lane> [until] [why]  mark unusable until an ISO date, or forever ("manual")
#   lane.sh clear <lane>                mark usable again
#
# Cooldowns EXPIRE BY THEMSELVES. That is the point: a spent quota usually comes back, so we
# stop asking for half an hour and then try once, rather than either hammering it or writing
# it off for the day.
F="${LANE_STATE_FILE:-$HOME/.claude/lane-state.json}"
python3 - "$F" "$@" <<'PY'
import json, sys, datetime as dt, pathlib
f = pathlib.Path(sys.argv[1]); cmd = sys.argv[2] if len(sys.argv) > 2 else "status"
LANES = ["api_credit", "gemini", "codex", "claude"]
LABEL = {"api_credit": "$200 API kredisi", "gemini": "Gemini 3.8 Flash (agy)",
         "codex": "Codex/GPT", "claude": "Claude abonelik"}
now = dt.datetime.now()
try: st = json.loads(f.read_text())
except Exception: st = {}

def until(name):
    """Returns (blocked, until_dt_or_None, reason). Expired cooldowns clear themselves."""
    e = st.get(name)
    if not e: return False, None, ""
    u = e.get("until")
    if u == "manual": return True, None, e.get("why", "")
    if not u: return False, None, ""
    try: d = dt.datetime.fromisoformat(u)
    except Exception: return False, None, ""
    if d <= now:
        st.pop(name, None); return False, None, ""
    return True, d, e.get("why", "")

if cmd == "status":
    out = []
    for n in LANES:
        b, d, why = until(n)
        if not b: out.append(f"{LABEL[n]}: ACIK")
        elif d is None: out.append(f"{LABEL[n]}: KAPALI (elle acilmali) {why}".rstrip())
        else: out.append(f"{LABEL[n]}: {d.strftime('%H:%M')}'e kadar kapali ({why})".rstrip())
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(st, indent=1))
    print("[SERITLER] " + " | ".join(out))
elif cmd in ("cool", "block", "clear"):
    name = sys.argv[3]
    if name not in LANES: sys.exit(f"bilinmeyen serit: {name} (gecerli: {', '.join(LANES)})")
    if cmd == "clear":
        st.pop(name, None); print(f"{LABEL[name]} tekrar acik")
    elif cmd == "cool":
        mins = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        why = " ".join(sys.argv[5:]) or "kota"
        d = now + dt.timedelta(minutes=mins)
        st[name] = {"until": d.isoformat(timespec="minutes"), "why": why}
        print(f"{LABEL[name]} {d.strftime('%H:%M')}'e kadar kapali ({why})")
    else:
        u = sys.argv[4] if len(sys.argv) > 4 else "manual"
        why = " ".join(sys.argv[5:]) or "kota bitti"
        st[name] = {"until": u, "why": why}
        print(f"{LABEL[name]} kapali: {u} ({why})")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(st, indent=1))
else:
    sys.exit("kullanim: lane.sh status|cool|block|clear ...")
PY
