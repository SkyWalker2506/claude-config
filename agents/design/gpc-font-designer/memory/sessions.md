# Sessions — GPC Font Designer

## 2026-04-27 — Agent Oluşturuldu

**Bağlam:** Golf Paper Craft canvas oyunu için font seçim sistemi tasarlanıyor.

**Kararlar:**
- Canvas prototype interceptor pattern seçildi (60+ ctx.font satırını tek tek değiştirmek yerine)
- localStorage key şeması tanımlandı: gpc_font_body, gpc_font_title, gpc_font_c0..c4
- Per-course font sadece level-select başlığı + complete/failed ekranına uygulanacak (HUD'a değil)
- storage event cross-tab reload mekanizması kuruldu
- Tüm Google Fonts adayları knowledge/font-candidates.md'ye kaydedildi

**Mevcut durum:** Knowledge dosyaları hazır. İmplementasyon henüz yapılmadı.
Game.js'e interceptor + per-course helper + storage listener eklenmesi ve fonts.html rewrite gerekiyor.
