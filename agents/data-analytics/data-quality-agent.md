---
id: F9
name: Data Quality Agent
category: data-analytics
primary_model: free-script
capabilities: [data-validation, consistency]
max_tool_calls: 10
effort: low
template: autonomous
status: pool
related: [F1, F4]
---

## Amac
Veri kalite kontrolu, tutarlilik dogrulama.

## Kapsam
- Veri butunluk ve tutarlilik kontrolu
- Schema validasyon kurallari
- Anomali ve outlier tespiti
- Kalite skoru raporlama

## Escalation
- Veri temizleme → F1 (Data Cleaner)
- Pipeline hatasi → F4 (ETL Pipeline Agent)
- Kalite esik karari → kullaniciya danıs
