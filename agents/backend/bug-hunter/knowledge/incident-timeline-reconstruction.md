---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Incident Timeline Reconstruction

## Quick Reference

| Veri kaynağı | Ne zaman kullanılır |
|--------------|---------------------|
| **Deploy / CI log** | Commit SHA, image tag, rollout zamanı |
| **Feature flag** (LaunchDarkly, Unleash, env) | Ani davranış değişimi — kullanıcı yüzdesi |
| **DB migration** | `flyway_schema_history`, Prisma `_prisma_migrations`, Alembic version |
| **APM / trace** | İlk hata zamanı, downstream çağrı sırası |
| **Infra** | K8s event, pod restart, node drain |

**Hedef:** Tek bir “incident window” — `T0` (ilk anomali) ile `T_deploy` / `T_flag` / `T_migrate` arasındaki nedensellik zinciri.

**2025–2026:** OpenTelemetry traceId ile log birleştirme; GitHub Deployments API ile ortam başına SHA.

## Patterns & Decision Matrix

| Belirti | Önce bak |
|---------|----------|
| Tam deploy sonrası | Yeni binary + migration sırası |
| Kademeli artış | Canary / flag yüzdesi vs zaman |
| Sadece bir bölge | Bölgesel outage veya partial flag |
| Veri şekli bozuk | Migration veya cache invalidation |

### Zaman çizelgesi şablonu

| UTC zaman | Olay | Kaynak |
|-----------|------|--------|
| 14:02:10 | p99 latency ↑ | Grafana |
| 14:05:00 | Deploy #4821 tamamlandı | GitHub Actions |
| 14:05:30 | `orders` migration uygulandı | migrate log |
| 14:06:00 | İlk 500 `/checkout` | APM |

## Code Examples

**Git ile deploy commit sınırı (yerel / CI artifact).**

```bash
git log --oneline -20 --first-parent main
# veya release tag: git show v2.4.1 --no-patch
```

**Feature flag geçmişi (örnek: LaunchDarkly API — kavramsal).**

```text
GET /api/v2/flags/default/my-flag
→ variations, rules, lastModified
→ “%50 true @ 14:04 UTC” ile incident hizala
```

**Migration sırası (PostgreSQL — Prisma).**

```sql
select migration_name, finished_at
from "_prisma_migrations"
order by finished_at desc
limit 10;
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sadece “son deploy” suçlusu | Aynı anda flag veya cron tetiklenmiş olabilir |
| Timezone karışıklığı | UTC’de tek çizelge; istemci saati kullanma |
| Log retention kısa | Kök neden için kritik satırlar silinmiş |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google SRE — Postmortem culture](https://sre.google/sre-book/postmortem-culture/) — zaman çizelgesi ve kök neden
- [OpenTelemetry — Trace context](https://opentelemetry.io/docs/concepts/signals/traces/) — traceId ile korelasyon
- [Martin Fowler — Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) — flag ve release ilişkisi
- [PostgreSQL — pg_stat_activity / migration history](https://www.postgresql.org/docs/current/catalogs.html) — şema geçmişi proje aracına göre (`_prisma_migrations`, `flyway_schema_history`)
