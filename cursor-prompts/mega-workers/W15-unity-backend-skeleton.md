# Worker W15 — Unity backend (iskelet) + diğer backend unity-*

**Scope path:** `agents/backend/` içinde **yalnızca** `unity-*/` alt klasörler.

**Skip (dokunma):** `frontend-coder/` (B3), `mobile-dev-agent/` (B15), `unity-shader-developer/` (B22), `unity-multiplayer/` (B23)

**İş kuralı:** Bu worker sadece `agents/backend/unity-*` altındaki agent’ları işler; yukarıdaki dört path’e **girme**. Kalan tüm `unity-*` klasörleri (ör. `unity-developer`, `unity-testing`, `unity-input-system`, …) mega-prompt Backend (Unity) tablosuna göre doldurulur.

**Knowledge:** mega-prompt Unity backend bölümü — her satırdaki dosya adlarıyla eşleştir.

[WORKER_PROMPT.md](WORKER_PROMPT.md) — `{SCOPE}` = `agents/backend/unity-*/` (tek tek klasör seçerek de bitebilir); `{SKIP}` = dört path.
