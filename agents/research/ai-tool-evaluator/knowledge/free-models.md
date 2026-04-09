---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Free Model Evaluation

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

## Free Tier Providers (April 2026)

### OpenRouter Free Tier
- Aggregates multiple free models from various providers
- Models rotate — availability changes frequently
- Rate limits vary per model (typically 10-60 RPM)
- Best for: model diversity, testing different architectures
- Current active: qwen3.6-plus:free (our primary free model)

### Groq
- Extremely fast inference (LPU hardware)
- Free tier with generous limits
- Limited model selection (Llama, Mixtral families)
- Best for: speed-critical tasks, real-time applications
- Weakness: model selection narrower than OpenRouter

### HuggingFace Inference API
- Free tier for open-source models
- Serverless inference endpoints
- Rate-limited, cold starts common
- Best for: experimenting with niche/specialized models
- Weakness: latency, reliability for production use

## Evaluation Methodology

### Hi-Test Protocol
Our standard test: send a greeting in Turkish, evaluate response quality.

Scoring:
- **Response quality** (0-10): coherence, language accuracy
- **Latency** (ms): time to first token
- **Availability** (uptime %): can we reach it right now

### Current Status (from hi-test results)
- Active: qwen3.6-plus via Groq
- Offline: Ollama local models (when machine has resources)
- Missing: GOOGLE_API_KEY for Gemini free tier

## Free Model Selection Strategy

```
Fallback chain (our standard):
free (OpenRouter) → free (Groq) → local (Ollama) → haiku → sonnet
```

Rules:
1. Always start with free — never use paid without reason
2. Test before committing — models degrade or disappear
3. Track availability — run hi-test periodically
4. Document which tasks each free model handles well

## Cost-Quality Trade-off Matrix

| Task Type | Minimum Model | Recommended |
|-----------|--------------|-------------|
| Simple file ops, formatting | Any free model | qwen3.6-plus:free |
| Code generation (simple) | Free mid-tier | qwen3.6-plus:free |
| Code generation (complex) | Haiku minimum | Sonnet |
| Architecture/design | Sonnet minimum | Opus |
| Security review | Sonnet minimum | Opus |

## Anti-Patterns

- Using Opus for simple tasks (wasteful)
- Not testing free models before dismissing them
- Hardcoding a specific free model (they rotate)
- Ignoring latency in free model evaluation
