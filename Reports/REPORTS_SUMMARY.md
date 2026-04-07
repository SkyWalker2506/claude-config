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
