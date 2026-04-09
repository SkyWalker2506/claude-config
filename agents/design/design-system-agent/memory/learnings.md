# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 | VocabApp Theme Analysis | opus
- VocabApp theme: `AppTheme` class with `light(Color)` / `dark(Color)` using `ColorScheme.fromSeed`
- Custom semantic colors in `AppColors`: successForeground, successContainer, amberStar — all brightness-adaptive
- Component overrides: AppBar (surface bg, no elevation), Card (clip, elevation 1), Input (outlined, filled), SnackBar (floating)
- Missing tokens: spacing system, motion tokens, typography extensions — need to create
- M3 surface variants (surfaceContainer hierarchy) not yet utilized in theme
