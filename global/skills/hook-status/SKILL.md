---
name: hook-status
description: SessionStart hook'larinin calisip calismadigini kontrol et — success/fail/skip ozeti goster.
---

## /hook-status

Bu session'da hangi SessionStart hook'larinin calistigini raporla.

## Uygulama

Baska hicbir sey yapma. Sadece bu session'in basinda gelen `system-reminder` mesajlarindan
`SessionStart:resume hook success:` ile baslayanlari listele.

Her satir icin:
- Mesaj geldiyse: ✅ `HOOK_ADI` — cikti (ilk 80 karakter)
- Mesaj gelmediyse: ❌ `HOOK_ADI` — tetiklenmedi

## Beklenen hook'lar (settings.json sirasinda)

1. `JARVIS_MODEL` — model adi ve emoji
2. `AVAILABLE_SECRETS` — secret key listesi
3. `MCP_ACTIVE` — aktif MCP sunucu listesi
4. `PROJECT_INDEX` — proje index guncelleme
5. `REPORTS_CHECK` — bekleyen rapor sinyali
6. `SESSION_SYNC` — claude-config sync
7. `JARVIS_POLICY` — politika mesaji

## Rapor Formati

```
=== SessionStart Hook Durumu ===
✅ JARVIS_MODEL     — claude-sonnet-4-6 🔶
✅ AVAILABLE_SECRETS — GITHUB_TOKEN, GROQ_API_KEY, ...
✅ MCP_ACTIVE       — atlassian, codex, context7, ...
⚠️ PROJECT_INDEX    — cikti gelmedi
⚠️ REPORTS_CHECK   — cikti gelmedi
⚠️ SESSION_SYNC    — cikti gelmedi
✅ JARVIS_POLICY    — Sen implementer degilsin...

7 hook tanimli — 4 ✅  3 ⚠️  0 ❌
```

Ekstra aciklama YAZMA. Sadece tablo + ozet satir.
