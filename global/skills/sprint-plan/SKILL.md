# /sprint-plan — Analiz Raporlarından Sprint Planı + Jira Girişi

## Açıklama

Proje analiz raporlarını (`analysis/` klasörü) okuyarak sprint planı oluşturur ve Jira'ya task olarak girer.

## Kullanım

```
/sprint-plan                    # Tam akış: plan oluştur + Jira'ya gir
/sprint-plan plan-only          # Sadece plan oluştur (Jira girişi yok)
/sprint-plan jira-only          # Mevcut planı Jira'ya gir
/sprint-plan sync               # Jira'daki mevcut task'ları planla senkronize et
```

## Ön koşul

- `analysis/` klasöründe en az 1 analiz raporu olmalı
- `analysis/MASTER_ANALYSIS.md` varsa öncelikli kaynak
- Jira girişi için Atlassian MCP aktif olmalı

## Akış

### 1. Proje bilgilerini tespit et

CLAUDE.md veya mevcut Jira task'larından proje anahtarını bul (örn: AC, VOC, vb.).
Bulamazsan kullanıcıya sor: "Jira proje anahtarı nedir? (örn: AC, VOC)"

### 2. Analiz Raporlarını Oku

```
analysis/*.md dosyalarını oku (MASTER_ANALYSIS.md dahil)
Her rapordan:
  - "Kesin Olmalı" / "Kritik Eksikler" → P0/P1
  - "İyileştirme Önerileri" / "Kesin Değişmeli" → P1/P2
  - "Nice-to-Have" → P2/P3
  - Etki (High/Med/Low) ve Efor (S/M/L/XL) bilgilerini çıkar
```

### 3. Task Çıkarımı

Her bulgu/öneri için:
- **Kısa başlık** (Jira summary — max 80 karakter, İngilizce)
- **Açıklama** (Türkçe — ne/neden/nasıl + kabul kriterleri checkbox listesi)
- **Label** (security, perf, arch, ui, growth, analytics, data, content, monetization, a11y, seo)
- **Öncelik** (P0/P1/P2/P3)
- **Efor** S=1, M=2, L=3, XL=5 story point

### 4. Sprint Organizasyonu

| Sprint | Odak | SP Kapasitesi |
|--------|------|---------------|
| 1 | Security & Critical Fixes | 25-35 |
| 2 | Performance & Architecture | 25-35 |
| 3 | UX & Accessibility | 25-35 |
| 4 | Analytics & Growth | 25-35 |
| 5 | Monetization & ASO | 25-35 |

**Kurallar:**
- Sprint 1 daima güvenlik + acil P0 düzeltmelerle başlar
- P0 task'lar atandığı sprint'te kesinlikle yer alır
- Her sprint 2 haftalık

### 5. Doküman Oluştur

Çıktı: `analysis/SPRINT_PLAN.md`

### 6. Jira Girişi

1. Her sprint için **Epic** oluştur: `[Sprint N] Odak Alanı`
2. Her task için issue oluştur (proje anahtarı: tespit edilen değer)
   - Summary: İngilizce (max 80 karakter)
   - Description: Türkçe (ne/neden/nasıl + kabul kriterleri)
   - Priority: P0→Highest, P1→High, P2→Medium, P3→Low
   - Labels + Story Points

**Paralel çalışma:** 5 sprint → 5 agent paralel Jira girişi yapabilir.

## Notlar

- Task başlık: **İngilizce**
- Task açıklama + kullanıcı iletişim: **Türkçe**
- Kaynak: `__PROJECTS_ROOT__/football-ai-platform/.claude/skills/sprint-plan/SKILL.md`
