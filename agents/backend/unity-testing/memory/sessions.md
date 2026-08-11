# Session Notes

> Onemli kararlar, reasoning ve sonuclar burada kayit altina alinir.
> Format: tarih + karar + neden + sonuc

<!-- Entries will be added by the agent after each significant session -->

## 2026-07-28 — bm-sandbox evidence gates

- Temporal mesh drift and anatomical attachment are separate gate signals.
- Combined footwear must not use a single renderer AABB centre; use baked-vertex proximity per foot.
- Probe evidence fails closed when missing, malformed, empty, timestamp-less, or from a different runId.
- Orphan skin bones require name, category, and explicit manual-driver evidence; counts alone cannot pass.
- Unity execution was intentionally deferred; Python synthetic clean/bad fixtures passed.
