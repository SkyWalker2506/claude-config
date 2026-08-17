# Session Notes

> Onemli kararlar, reasoning ve sonuclar burada kayit altina alinir.
> Format: tarih + karar + neden + sonuc

<!-- Entries will be added by the agent after each significant session -->

## 2026-08-13 — animation-creator timing controls

- Traced the user-facing “web’de aç” path to the hosted Vercel review UI
  (`vercel/index.html`), while `web/app.html` is a separate local Flask studio.
- Added accessible FPS, duration and output-mode controls to the hosted new-job
  form, preserving the shared 49/192-frame budget and explicit queue payload.
- Verified the local studio on `127.0.0.1:7860`; the hosted deployment still
  needs an authorized Vercel deploy before the source change becomes visible.
