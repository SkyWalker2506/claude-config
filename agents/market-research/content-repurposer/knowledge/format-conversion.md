---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Format Conversion

## Quick Reference

| Kaynak → Hedef | Dikkat |
|----------------|--------|
| **Metin → video** | Storyboard, B-roll listesi, süre sınırı |
| **Video → metin** | Transkript düzeltme, başlık hiyerarşisi |
| **PDF → web** | HTML yapı, mobil, erişilebilir tablolar |
| **Slayt → blog** | Konuşmacı notlarını genişlet |
| **Veri → görsel** | Ölçek, birim, kaynak dipnotu |

**Erişilebilirlik:** Videoda altyazı; görselde alt metin; tabloda başlık satırı.

## Patterns & Decision Matrix

| Sorun | Çözüm |
|-------|--------|
| Uzun video | Bölüm bölüm chapter işareti |
| Yoğun tablo | Özet grafik + tam tablo linki |
| Çok dil | Çeviri + yerel örnek inceleme |

### Dosya teknikleri

- Markdown → CMS: bileşen ve kısa kod uyumu
- SVG vs. PNG: logo ve ikon için vektör

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| OCR’a körü güvenmek | Yanlış rakamlar |
| 4K video’yu sıkıştırmadan yüklemek | Yavaş yükleme |
| Tabloyu görsele çevirip erişilebilirliği unutmak | Ekran okuyucu dışlar |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [WebAIM — accessibility](https://webaim.org/) — erişilebilir web
- [MDN — HTML table](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table) — semantik tablo
- [BBC — GEL](https://www.bbc.co.uk/gel) — tasarım sistemi (okunabilirlik)
- [FFmpeg documentation](https://ffmpeg.org/documentation.html) — format dönüşümü (teknik)
- [W3C — Media accessibility](https://www.w3.org/WAI/media/av/) — video erişilebilirliği
