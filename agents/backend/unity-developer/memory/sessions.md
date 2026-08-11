# Session Notes

> Onemli kararlar, reasoning ve sonuclar burada kayit altina alinir.
> Format: tarih + karar + neden + sonuc

<!-- Entries will be added by the agent after each significant session -->

## 2026-07-28 — bm-sandbox reproducible evidence package

- `docs/DURUM.md` is the current truth; `docs/DERSLER.md` is explicitly historical.
- Evidence ZIP generation fails closed unless all probe JSONs share the frame manifest runId.
- Bundle provenance records UTC, commit, dirty fingerprint, project/packages, scene references,
  commands, seed, raw/graded artifact SHA-256, and ZIP checksum.
- Exposure evidence must name sampled frames and retain its full 256-bin histogram.
- Unity was not run; existing legacy outputs correctly fail the new runId requirement.
