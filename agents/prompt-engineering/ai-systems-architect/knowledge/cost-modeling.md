---
last_updated: 2026-04-09
refined_by: opus
confidence: medium
---

# Cost Modeling

## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---

## Token Cost Reference (April 2026)

| Model | Input (per 1M) | Output (per 1M) | Context | Notes |
|-------|----------------|-----------------|---------|-------|
| Claude Opus 4 | $15 | $75 | 200K | Heavy reasoning, architecture |
| Claude Sonnet 4 | $3 | $15 | 200K | Best price/performance for coding |
| Claude Haiku 3.5 | $0.80 | $4 | 200K | Classification, simple tasks |
| GPT-4o | $2.50 | $10 | 128K | General purpose |
| Qwen 3 (Groq) | Free | Free | 32K | Rate-limited, good for triage |

## Cost Calculation Formula

```
Cost = (input_tokens * input_price) + (output_tokens * output_price)

Example: Sonnet reviewing a 5K token file, producing 2K output
= (5000 * $3/1M) + (2000 * $15/1M)
= $0.015 + $0.030 = $0.045 per review
```

## Multi-Agent Cost Multipliers

| Pattern | Multiplier | Why |
|---------|-----------|-----|
| Single agent | 1x | Baseline |
| Pipeline (3 stages) | 3x | Each stage = full LLM call |
| Fan-out (5 parallel) | 5x | Independent calls |
| AutoGen debate (4 agents, 5 rounds) | 20x | Every turn = LLM call with growing context |
| Router + specialist | 1.2x | Router is cheap (Haiku), specialist does work |

## Tier Strategy

### Tier 1: Free/Local (zero cost)
- **Models**: Qwen 3 via Groq, Ollama local models
- **Use for**: Triage, classification, simple formatting, health checks
- **Limit**: Rate limits, smaller context, lower quality

### Tier 2: Fast/Cheap (Haiku, GPT-4o-mini)
- **Use for**: Routing decisions, code formatting, simple generation
- **Budget**: ~$0.01-0.05 per task

### Tier 3: Balanced (Sonnet, GPT-4o)
- **Use for**: Code generation, review, planning
- **Budget**: ~$0.05-0.50 per task

### Tier 4: Premium (Opus)
- **Use for**: Architecture decisions, complex debugging, final review
- **Budget**: ~$0.50-5.00 per task

## Cost Optimization Strategies

1. **Route cheap tasks to cheap models** — use Haiku for classification, Opus for architecture
2. **Cache aggressively** — prompt caching reduces input cost by 90%
3. **Minimize context** — every extra file loaded costs tokens
4. **Avoid debate patterns** — fan-out + merge cheaper than multi-round discussion
5. **Batch similar tasks** — amortize system prompt cost across multiple items
6. **Use sub-agents wisely** — each spawned agent pays full context cost

## Budget Tracking

```
Daily budget = $X
Per-task estimate = tokens * price
Running total = sum(task costs)
Alert at 80% budget
```

## Free Model Usage (Freemium Philosophy)

Per project philosophy: never spend money before earning it.

- Start with free tier (Groq/Qwen) for development
- Upgrade to paid only when free models demonstrably fail
- Track which tasks succeed on free vs paid models
- `/hi-test` skill validates free model availability
