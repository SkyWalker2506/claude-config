#!/usr/bin/env bash
# PreToolUse on Agent|Task. Refuses to dispatch a subagent whose prompt does not carry the
# routing line, so every subagent starts with the same model/effort rules the parent has.
#
# Why a BLOCK and not a reminder: the parent forgetting is exactly the failure this exists to
# stop. A reminder depends on the thing that already fails. exit 2 does not.
# Written 2026-10-27.
P=$(printf '%s' "$CLAUDE_TOOL_INPUT" | python3 -c \
  "import sys,json
try: print(json.load(sys.stdin).get('prompt',''))
except Exception: print('')" 2>/dev/null)

# Empty input: never block on our own parsing failure.
[ -z "$P" ] && exit 0

case "$P" in
  *"[YONLENDIRME]"*) exit 0 ;;
esac

cat >&2 <<'TXT'
BLOCKED: this subagent prompt is missing the routing line.

Add this line verbatim to the prompt (one line, ~40 tokens), then dispatch again:

[YONLENDIRME] Uretimi sen yapma, ucuzdan basla: $200 API kredisi -> Gemini 3.8 Flash (agy)
-> Codex/GPT orta kademe -> Claude en son. Kod/sprite/toplu tarama/gorsel inceleme = Gemini
veya GPT. Sende kalan: olcum, teshis, kabul/red karari. Model+effort'u ise gore sec.

Also check you picked the cheapest model that can do this job (`model:` on the Agent call).
TXT
exit 2
