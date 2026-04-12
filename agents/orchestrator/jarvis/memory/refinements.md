# Refinement Log

> Knowledge ve AGENT.md dosyalarina yapilan guncellemelerin kaydi.
> Format: tarih + model + ne degisti + neden

<!-- Entries will be added after each /agent-refine run -->

## 2026-04-12 | opus | /agent-sharpen Jarvis

**Degisenler:**
- `knowledge/agent-dispatch-rules.md` — jenerik filler block (lines 9-31) silindi; Python/3D Pipeline dispatch satiri eklendi; "Jarvis'in Kendisi Ne Yapar" bolumu AGENT.md ile hizalandi (git is dispatch edildi, kod/design/refactor yapmaz vurgusu); yeni "Jarvis'in Kendisi YAPMAZ" bolumu.
- `knowledge/project-ecosystem.md` — filler silindi; 3d-asset-foundry projesi aktif projeler tablosuna eklendi; 3d-asset-foundry icin ayrintili notlar bolumu (mimari, §4.6 guvenlik siniri, Phase 0 blockers, stack, drift report kaynagi); "Ortak Ozellikler" Python/Unity istisnalari ile guncellendi.
- `knowledge/session-management.md` — filler silindi.
- `knowledge/cross-project-patterns.md` — filler silindi; "Python Projeleri (Istisna)" bolumu eklendi (stack, 3d-asset-foundry ozeli, invariant test kurali).
- `knowledge/user-preferences.md` — filler silindi; "TODO-only modu" ve "Drift report stili" tercihleri eklendi.
- `knowledge/_index.md` — last_updated + last_sharpen kaydi.
- `memory/learnings.md` — 2026-04-12 entry: 7 key finding (filler sorunu, 3d-asset-foundry, vault isolation, git dispatch catiskisi, Python kategorisi, TODO-only pattern, invariant test kurali).

**Neden:**
- Jenerik filler 5 dosyada sinyal/gurultu oranini bozuyordu — silindi.
- 3d-asset-foundry ekosistemde yoktu → gelecek dispatch hatalari riski.
- AGENT.md ↔ agent-dispatch-rules.md catiskisi (git) Jarvis'in kod/git yapma riskini artiriyordu → AGENT.md truth kabul edildi.
- Python/3D kategorisi olmadigi icin 3d-asset-foundry isleri yanlis agent'a dispatch edilebilirdi.
- Kullanicinin "sadece todo yaz" modu yakalanmali — tekrar eden pattern.

**Boundary check:** Tum degisiklikler Jarvis'in kapsam alani icinde (orchestration, routing, user preferences, ecosystem registry). Proje-spesifik implementasyon detayi yazilmadi — sadece dispatch sinyali.

**Verification:** 5 knowledge dosyasi guncellendi | last_updated 2026-04-12 | learnings entry var | refinements entry (bu) var | boundary ihlali yok.
