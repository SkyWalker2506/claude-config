# Reports Summary

> Her rapor işlenince buraya özet eklenir. İşlenen dosya `Processed/` klasörüne taşınır.

## Sistem

- `Reports/` → İşlenmemiş raporlar burada bekler
- `Reports/Processed/` → İşlenen raporlar buraya taşınır
- `Reports/TEMPLATE.md` → Yeni rapor şablonu
- `REPORTS_SUMMARY.md` → Bu dosya, tüm raporların özeti
- `config/reports_check.sh` → SessionStart hook'u — rapor tespiti

## Rapor Yaşam Döngüsü

```
UNPROCESSED → IN_PROGRESS → DONE → Processed/
```

1. Rapor `.md` olarak `Reports/` klasörüne konur (`Status: UNPROCESSED`)
2. Oturum başında hook tespit eder → `REPORTS_PENDING` sinyali
3. Claude raporu okur → `Status: IN_PROGRESS`
4. Aksiyonlar uygulanır
5. `Status: DONE` → özet buraya eklenir → dosya `Processed/`'a taşınır

## Startup Kuralı (Claude için)

Her oturum başında:
1. `REPORTS_PENDING` sinyali var mı? (hook otomatik üretir)
2. Varsa → CLAUDE.md §8h protokolünü izle
3. Yoksa → devam et

---

## İşlenen Raporlar

| # | Dosya | Tarih | Öncelik | Özet |
|---|-------|-------|---------|------|
| 1 | 001_project_analysis_system_gaps.md | 2026-04-07 | HIGH | Lead "dispatches" belirsizliği giderildi; §4'e model mapping eklendi; D1 → free-gemini; gemini-call.sh wrapper oluşturuldu; SKILL.md'ye §2/§4/§5 okuma zorunluluğu eklendi |
| 2 | 002_free_model_openrouter_routing.md | 2026-04-07 | CRITICAL | Claude Code artık custom model ID kabul ediyor — rapordaki sorun çözülmüş. `_claude-env` zaten silinmiş, `bin/claude` temiz, `.zshrc` routing düzgün çalışıyor. Ek aksiyon gerekmedi. |
