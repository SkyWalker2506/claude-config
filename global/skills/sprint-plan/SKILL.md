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
- **Verify kriteri** (mekanik doğrulama komutu — test, curl, dosya varlığı kontrolü, lint)

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

### 4b. Wave Dependency Graph

Sprint içindeki task'lar wave'lere ayrılır:
- Her task'a `depends_on: [KEY-xxx, KEY-yyy]` alanı eklenir
- Bağımlılığı olmayan task'lar Wave 1'e gider
- Bağımlılığı olan task'lar, bağımlılıkları tamamlanınca sonraki wave'e girer
- Wave içi task'lar paralel çalışır, wave'ler sıralı

Örnek:
```
Wave 1 (paralel): KEY-101, KEY-102, KEY-103
Wave 2 (paralel): KEY-104 (depends: 101), KEY-105 (depends: 102)
Wave 3: KEY-106 (depends: 104, 105)
```

SPRINT_PLAN.md'de her task'ın formatı:
```markdown
### KEY-101: Add rate limiting
- Priority: P1
- Effort: M (2 SP)
- Labels: security, backend
- Verify: `curl -w '%{http_code}' localhost:3000/api/test | grep 429`
- Depends: []
- Wave: 1
```

### 5. Doküman Oluştur

Çıktı: `analysis/SPRINT_PLAN.md`

Her task `verify:` alanını içermelidir — mekanik doğrulama komutu (test, curl, dosya varlığı kontrolü, lint). Verify eksik task SPRINT_PLAN.md'ye alınmaz.

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

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
