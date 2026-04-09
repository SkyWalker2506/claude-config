# Mega workers — paralel Composer oturumları

1. [MEGA_BATCH_MANIFEST.md](../MEGA_BATCH_MANIFEST.md) — tüm batch ve skip listesi
2. [WORKER_PROMPT.md](WORKER_PROMPT.md) — kopyala-yapıştır şablon
3. Worker scope dosyaları:

| Worker | Dosya |
|--------|--------|
| W1 | [W1-orchestrator.md](W1-orchestrator.md) |
| W2 | [W2-code-review.md](W2-code-review.md) |
| W3 | [W3-design.md](W3-design.md) |
| W4 | [W4-devops.md](W4-devops.md) |
| W5 | [W5-data-analytics.md](W5-data-analytics.md) |
| W6 | [W6-ai-ops.md](W6-ai-ops.md) |
| W7 | [W7-jira-pm.md](W7-jira-pm.md) |
| W8 | [W8-research.md](W8-research.md) |
| W9 | [W9-market-research.md](W9-market-research.md) |
| W10 | [W10-marketing-engine.md](W10-marketing-engine.md) |
| W11 | [W11-productivity.md](W11-productivity.md) |
| W12 | [W12-agent-builder.md](W12-agent-builder.md) |
| W13 | [W13-sales-bizdev.md](W13-sales-bizdev.md) |
| W14 | [W14-3d-cad.md](W14-3d-cad.md) |
| W15 | [W15-unity-backend-skeleton.md](W15-unity-backend-skeleton.md) |

## Nasıl çalıştırılır

- **15 paralel pencere (veya 5’li gruplar):** Her `W*` için ayrı Composer oturumu; aynı `W*`’ı iki kez açma (çakışma).
- Her pencerede: [WORKER_PROMPT.md](WORKER_PROMPT.md) + ilgili `W*.md` içindeki **Scope / Skip** değerlerini doldur.
- Manifest: [MEGA_BATCH_MANIFEST.md](../MEGA_BATCH_MANIFEST.md)

## Durum

```bash
./bin/mega-rollout.sh verify
```
