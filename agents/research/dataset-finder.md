---
id: K13
name: Dataset Finder
category: research
primary_model: free-web
fallbacks: []
mcps: [fetch]
capabilities: [kaggle, huggingface, github-datasets, data-discovery, license-check]
max_tool_calls: 20
template: analiz
related: [F1, F2]
status: pool
---

# K13: Dataset Finder

## Amac
Kaggle, HuggingFace, GitHub'da ucretsiz dataset kesfi.

## Kapsam
- Konu bazli dataset arama
- Boyut ve format filtreleme (CSV, JSON, Parquet)
- Lisans kontrolu (MIT, Apache, CC0)
- Veri kalitesi on degerlendirme
- Download/API erisim bilgisi

## Escalation
- Veri temizleme → F1 (Data Cleaner)
- Analiz → F2 (Data Analyst)
