---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Session Management

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

## Session Baslangic Kontrolleri

1. **CLAUDE.md oku** — proje kurallari
2. **Hook sinyallerini isle:**
   | Sinyal | Aksiyon |
   |--------|---------|
   | MIGRATION_NEEDED | /migration calistir |
   | INDEX_ASK | Kullaniciya sor, onaylarsa indexle |
   | INDEX_UPDATE | Sessizce guncelle |
   | SECRETS_MISSING | Kullaniciya bildir |
   | INSTALL_NEEDED | install.sh calistir |
3. **AVAILABLE_SECRETS kontrol** — hangi servislere erisim var
4. **MCP listesi kontrol** — kullanilmayanlari kapat
5. **knowledge/_index.md oku** — ilgili bilgileri yukle
6. **projects.json oku** (ClaudeHQ'daysa)

## Context Yonetimi
- **%60 doluluk** → /compact yap
- **%95** → otomatik compact
- **Konu degisimi** → /clear
- **5dk+ mola oncesi** → /compact (prompt cache sifirlanir)
- **Buyuk dosya (>20KB)** → Sonnet'te oku/yaz
- **Terminal cikti** → head -N ile sinirla

## Model Secim Kurallari
```
free (OpenRouter) → free (Groq) → local (Ollama) → haiku → sonnet
```
- Sormadan ucretli baslatma
- Ucretli gecis icin kullaniciya sor
- Sub-agent default: haiku veya free

## Kota Yonetimi
| Kalan | Mod |
|-------|-----|
| ≥10% | Normal — Opus karar, Sonnet kod, Haiku trivial |
| 5-10% | Tasarruf — Opus sadece kritik |
| <5% | Kritik — Sonnet + Haiku only |
| <1% | Sonnet-only |

## Raporlama
- Is bitince kisa ozet ver
- Commit/PR gerekiyorsa hazirla
- Onemli kararlari memory/sessions.md'ye kaydet
- Agent'a aktarilacak bilgi varsa not al
