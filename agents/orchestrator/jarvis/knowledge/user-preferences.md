---
last_updated: 2026-04-12
refined_by: opus
confidence: high
---

# User Preferences — Musab Kara

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
- **TODO-only modu:** "kod yazma, sadece todo olarak yaz aciklama" dediginde → drift analizi yap + bullet TODO listesi + P0/P1/P2 oncelik + implementer agent onerisi, kod asla yazilmaz
- **Drift report stili:** Missing / Misaligned / Incomplete / Extra / Version-mismatch kategorilerinde grupla

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
