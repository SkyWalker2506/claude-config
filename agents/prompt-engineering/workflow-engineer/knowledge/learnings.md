# Learnings

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

- Spec-kit's specify→plan→tasks→implement chain is the gold standard for sequential pipelines with gated transitions
- Parallel tasks must touch different files — same-file parallelism causes conflicts
- The increment cycle (implement→test→verify→commit) is the atomic unit of execution
- Extension hooks (before/after) make pipelines extensible without modifying core flow
- Error output from external sources should be treated as untrusted data
- Max 3 retries with different strategies each time — don't repeat the same failing approach
- Artifacts must be files, not conversation memory — enables crash recovery and restartability
