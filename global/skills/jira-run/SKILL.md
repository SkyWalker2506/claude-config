---
name: jira-run
description: Jira wait-and-check döngüsü. Proje anahtarini docs/CLAUDE_JIRA.md'den okur. Tur sayısı + tur arası bekleme (örn. 50 1s). Durdurma /jira-cancel.
argument-hint: "[tur] [aralık] — örn. 50 1s | 10 | 10_1m | boş → 10 tur 1dk"
disable-model-invocation: true
---

## Tetikleme

`/jira-run`, `/JIRA-RUN`, `JiraRun 50 1s` — hepsi bu skill.

## Çalıştırma modu

| Ortam | Kural |
|-------|-------|
| **Claude Code** | Ana oturum: (1) `rm -f .jira-state/jira-run.stop` (2) IP task varsa → Implementation agent `Agent(run_in_background=true)` (3) jira-run agent `Agent(run_in_background=true)`. İkisi paralel çalışır. |
| **Cursor** | Tam döngü mevcut sohbette çalışır — arka plan zorunlu değil. |

**Claude Code kısıtı:** Sub-agent'lar `Agent` aracını çağıramaz. Implementation agent'ı **yalnızca ana oturum** başlatır.

## Başlatma (her zaman ilk komut)

```bash
rm -f .jira-state/jira-run.stop
```

Repo kökünde çalıştır: `cd "$(git rev-parse --show-toplevel)"` gerekirse.

## Bilgilendirme

**A) Başlarken** (Claude Code arka planda değil, Cursor'da bu sohbette):
```
[JiraRun] Başladı — Tur: <N>, Aralık: <T>, İptal: /jira-cancel
```

**B) Normal bitiş:**
```
[JiraRun] Bitti — <N> tur tamamlandı (iptal yok).
```

**C) İptal:**
```
[JiraRun] İptal (jira-cancel / stop dosyası).
```

## Argüman çözme (`$ARGUMENTS`)

| Girdi | Tur | Aralık |
|-------|-----|--------|
| boş | 10 | 1m |
| `10` | 10 | 1m |
| `50 1s` / `50_1s` | 50 | 1s |
| `10 1m` / `10_1m` | 10 | 60s |
| `1h30m` bileşik | — | 5400s |
| geçersiz | uyarı | varsayılan |

Birimler: `s`=saniye, `m`=dakika, `h`=saat (ondalık destekli: `0.5h`=1800s).

## Otomatik çıkış koşulları

1. **MCP yok (1. tur)** → `docs/jira_loop_log.md` güncelle + cancel + çık
2. **2 ardışık boş tur** → log + cancel + çık
3. **Stop dosyası** → her tur başında kontrol; varsa sil + iptal mesajı + çık

## Döngü (her tur sırası)

1. `.jira-state/jira-run.stop` kontrol → varsa çık
2. `/tmp/jira_run_status.json` güncelle (watchdog)
3. (1. tursa) MCP erişim kontrol → yoksa çık
4. `docs/CLAUDE_JIRA.md` protokolünü çalıştır → tur özeti
5. Boş tur sayacını güncelle → 2 ardışıksa çık
6. Son tur değilse: `sleep(interval)`

**Yasak:** toplu sleep ile N tur taklidi; protokolsüz "N tur bitti" iddiası; Claude Code'da ön planda tam döngü.

## Implementation Agent şablonu

→ `docs/agent-template.md` — kelimesi kelimesine kullan, `[...]` kısımlarını doldur.

## Lock sistemi

→ `docs/LOCK_SYSTEM.md`

## Log

`docs/jira_loop_log.md` — en yeni üstte. Otomatik çıkışlarda güncellenir.

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
