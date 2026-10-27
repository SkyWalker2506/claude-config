# LLM input-size price thresholds (long-context tiers)

Checked: 2026-10-26. Primary sources (official, trusted over any model's own answer):
- Claude: https://platform.claude.com/docs/en/about-claude/pricing.md (section "Long context pricing" + model table)
- Gemini: https://ai.google.dev/gemini-api/docs/pricing

## Short answer (the "117K" question)
Haiku 5.5 is billed per REQUEST, by that request's prompt length. A 117K-token prompt is billed ENTIRELY at the higher rate
(all 117K input tokens, plus output, cache write and cache read at the higher rates). It is NOT "100K cheap + 17K expensive".
Official wording: "a request whose prompt is over 100,000 tokens pays higher prices." The price table has two full rows
("for prompts up to 100,000 tokens" / "for prompts over 100,000 tokens"), i.e. no marginal split.

## Claude (USD per MTok: input / output / cache read)
| Model | Threshold | Below | Above | Notes |
|---|---|---|---|---|
| Haiku 5.5 | 100,000 prompt tokens | 0.10 / 0.50 / 0.01 | 0.50 / 2.50 / 0.05 (5x, output too) | cache write 5m 0.125 -> 0.625, 1h 0.20 -> 1.00 |
| Sonnet 5.5 | none | 2 / 10 / 0.10 | same | full 1M context at standard price |
| Opus 5.5 | none | 4 / 20 / 0.20 | same | full 1M context at standard price |
| Fable 5.1 | none | 10 / 50 / 0.25 | same | full 1M context at standard price |

Exact wording (Claude pricing page):
- "Claude 4.6 and later models (except Claude Haiku 5.5) and Claude Mythos Preview include the full 1M token context window at standard pricing. (A 900k-token request is billed at the same per-token rate as a 9k-token request.)"
- "Claude Haiku 5.5 is priced by prompt length: a request whose prompt is over 100,000 tokens pays higher prices. A request's prompt length counts all of its input tokens, including cache reads and cache writes. Each request is priced on its own: a request over the threshold pays the higher prices even when part of its prompt is a cache hit, and earlier requests keep the prices they were billed at."
- US-only inference (1.1x) also applies to Haiku's higher >100K prices.

Owner hypothesis "only Haiku has this threshold": CONFIRMED for the Claude 4.6+ lineup listed above (Haiku 5.5 is the only listed exception).
(The Fast mode paragraph mentions "requests over 200k input tokens" for Opus, but states fast-mode pricing applies across the full context; no 200K surcharge tier is stated for standard Opus/Sonnet/Fable.)

## Gemini (USD per 1M tokens)
| Model | Threshold | <= | > | Notes |
|---|---|---|---|---|
| 3.1 Pro Preview | 200k prompt tokens | in 2.00 / out 12.00 (incl. thinking) / cache 0.20 | in 4.00 / out 18.00 / cache 0.40 | cache storage 4.50 per 1M tokens/hour, no tier split |
| 3.8 Flash | none stated, flat | in 0.75 / out 3.75 / cache 0.075 through 2026-12-31 | from 2027-01-01: 1.50 / 7.50 / 0.15 | storage 0.50/h, then 1.00 |
| (2.5 Pro, for reference) | 200k | 1.25 / 10 / 0.125 | 2.50 / 15 / 0.25 | |

Gemini page labels tiers "prompts <= 200k tokens" / "prompts > 200k tokens". No 100K threshold exists on the page.
Whole-prompt vs excess for Gemini: not stated on the page text we retrieved (WebFetch summary); the same row-per-prompt-size layout
suggests whole prompt, but treat as unverified.

## Cross-check with Gemini's own answer (agy, gemini-3.8-flash, 2026-10-26)
Gemini said: Gemini threshold 128K, whole request, output ~2x; Claude: no threshold anywhere, flat. It also called the 5.5 series
"hypothetical". Official pages disagree on: Gemini threshold is 200K (not 128K) and 3.8 Flash has none; Claude Haiku 5.5 DOES have
a 100K tier. Trust the official pages; Gemini's answer was from training data, not live pricing.

## Per-request, not per-session (agent sessions)
Thresholds are measured on each API request's own prompt (all input tokens incl. cache reads/writes), never on cumulative session tokens.
In Claude Code every tool call is a new request that re-sends the whole context, so a Haiku session whose context grows past 100K
bills EVERY following request at the 5x rate (even cache hits at 0.05 instead of 0.01), until context is compacted/cleared below 100K.
Practical rule: keep Haiku 5.5 runs under ~100K context (compact early / short sub-agent tasks); above it, Sonnet 5.5 (2/10, no tier) is
only 4x Haiku-high-tier input but 4x output; Haiku >100K (0.50/2.50) is still ~4x cheaper than Sonnet.
