---
id: F4
name: ETL Pipeline Agent
category: data-analytics
primary_model: free-script
capabilities: [etl, pipeline, data-transfer]
max_tool_calls: 15
effort: medium
template: autonomous
status: pool
related: [F1, F9]
---

## Amac
ETL pipeline olusturma, veri aktarim.

## Kapsam
- Extract-Transform-Load pipeline scripti
- Veri kaynak baglantisi (CSV, API, DB)
- Zamanlama ve batch islem kurulumu
- Pipeline hata yonetimi ve loglama

## Escalation
- Veri temizleme → F1 (Data Cleaner)
- Kalite dogrulama → F9 (Data Quality Agent)
- Prod veri erisimi → kullaniciya danıs
