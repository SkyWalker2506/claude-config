---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# Newsletter Design Patterns

## Quick Reference

| Bölüm | Amaç |
|-------|------|
| **Preheader** | Konu satırını tamamlar — açılış oranı |
| **Üst blok** | Tek ana mesaj veya editör notu |
| **Gövde** | 2–4 blok; her biri tek CTA |
| **Alt bilgi** | Abonelik yönetimi, adres, sosyal |

**Mobil öncelik:** Tek sütun, 16px+ font, dokunmatik hedefler 44px.

## Patterns & Decision Matrix

| Newsletter tipi | Yapı |
|-------------------|------|
| **Kürasyon** | Giriş paragraf + 3 bağlantı + özet |
| **Ürün güncellemesi** | Özellik → fayda → öğrenme kaynağı |
| **Eğitim** | Adım adım; görsel veya kod bloğu |

### Tasarım sistemi

- Marka renkleri — WCAG kontrast 4.5:1 (metin)
- Tek tip başlık hiyerarşisi (H1 yok; e-posta istemcileri değişken)

## Code Examples

**Tek sütun HTML iskelet (inline CSS — Litmus uyumlu minimal):**

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
  <tr><td align="center" style="padding:24px;">
    <table role="presentation" width="600" style="max-width:600px;font-family:system-ui,sans-serif;">
      <tr><td style="font-size:16px;line-height:1.5;color:#111;">
        <p style="margin:0 0 16px;">Merhaba {{first_name}},</p>
        <p style="margin:0 0 16px;">Tek mesaj: yeni sürüm canlı.</p>
        <a href="{{cta_url}}" style="display:inline-block;padding:12px 20px;background:#111;color:#fff;text-decoration:none;border-radius:6px;">Detayı gör</a>
      </td></tr>
    </table>
  </td></tr>
</table>
```

**MJML parça (derleme → HTML):**

```xml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">Özet başlık</mj-text>
        <mj-button href="{{cta}}">Tek CTA</mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Çok CTA | Tıklama dağılır |
| Sadece görsel — metin yok | Görüntü kapalı istemcilerde boş |
| Ağır görsel | Yavaş yükleme, spam skoru |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Litmus — email design](https://www.litmus.com/resources/) — istemci uyumu
- [Really Good Emails](https://reallygoodemails.com/) — örnek galeri
- [CAN-SPAM compliance](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) — ABD kuralları
- [WCAG — contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) — kontrast
