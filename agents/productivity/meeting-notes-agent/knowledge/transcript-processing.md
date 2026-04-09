---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Transcript Processing

## Quick Reference

**Pipeline:** ham ses → STT (Whisper, Google STT, Azure) → segment zaman damgası → özüt + aksiyon çıkarma. **Formatlar:** VTT, SRT, düz metin + `HH:MM:SS` önekleri.

| Adım | Çıktı |
|------|-------|
| Segment temizleme | Dolgu kelime (`um`) azaltma |
| Konuşmacı diarization | `SPEAKER_01` etiketi |

```text
Özet/aksiyon: transkriptin tamamını değil — karar ve fiil cümlelerini önceliklendir
```

## Patterns & Decision Matrix

| Model | Artı | Eksi |
|-------|------|------|
| Cloud STT | Yüksek doğruluk | Veri çıkışı |
| Whisper lokal | Gizlilik | GPU gerekir |
| İnsan düzeltme | En iyi | Maliyet |

**Gizlilik:** HIPAA/NDA toplantılarında bulut STT politikasına bak.

## Code Examples

**WebVTT kesit:**

```vtt
WEBVTT

00:01:02.000 --> 00:01:08.000
<v Alice>Let's lock the sunset date to September first.

00:01:08.500 --> 00:01:12.000
<v Bob>Approved.
```

**Özet çıkarım prompt iskelesi (metin — dış LLM):**

```text
Given the transcript below, extract:
1) Decisions (bullet, who approved)
2) Action items (owner, due if stated)
3) Open questions
Transcript:
---
{paste}
```

**Python — satır bazlı zaman damgası parse:**

```python
import re
line = "00:12:34 Let's ship it."
m = re.match(r"(\d{2}:\d{2}:\d{2})\s+(.*)", line)
if m:
    ts, text = m.group(1), m.group(2)
```

## Anti-Patterns

- **STT’ye güvenmeden hukuki iddia:** "X dedi" — zaman damgası ile doğrula.
- **Ham transkripti e-posta ile dışarı:** Özet + PII maskele.
- **Çoklu dil karışımı:** Dil tespiti önce; model dil başına seç.
- **Uzun sessizlik segmentlerini tutmak:** Post-process ile kırp.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [OpenAI Whisper](https://github.com/openai/whisper) — açık kaynak STT
- [W3C — WebVTT](https://www.w3.org/TR/webvtt1/) — altyazı formatı
- [Google Cloud — Speech-to-Text](https://cloud.google.com/speech-to-text/docs) — streaming ve dil
