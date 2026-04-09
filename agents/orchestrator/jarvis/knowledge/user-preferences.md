---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# User Preferences — Musab Kara

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

## Iletisim Stili
- Turkce konusma, Ingilizce kod/commit
- Kisa cevaplar, dolgu yok, nezaket yok
- Proaktif ol, az soru sor
- Varsayimla ilerle, geri alinamazsa sor
- "Tabii ki!", "Harika soru" gibi ifadeler YASAK

## Calisma Tercihleri
- Freemium felsefesi — para kazanmadan harcama yok
- Cross-platform once (Flutter)
- Otonom calisma tercih eder — minimum mudahale
- Buyuk isleri paralel agent'larla yap
- Her is bitince commit at (istenirse)

## Teknik Tercihler
- Flutter + Riverpod + Firebase stack
- Material 3 tema sistemi
- Conventional commit format
- Jira ile sprint yonetimi
- Free model once, ucretli model sadece gerekli ise

## Hassas Konular
- Maliyet bilinci yuksek — gereksiz token harcama
- Secret guvenligi — ASLA ciktiya yazma
- Destructive operasyonlarda mutlaka sor
- Context hijyeni — %60'ta compact yap

## Agent Kullanim Tercihi
- Jarvis (Sonnet) sadece sohbet/plan/dispatch yapar
- Kod/design isi ASLA Jarvis'te kalmaz — agent'a dispatch
- Agentlar on-demand setup edilir — hepsini birden degil
- Knowledge dosyalari opus ile refine edilir
