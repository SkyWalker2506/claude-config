# Feature Requests & Improvement Backlog

> Kullanıcı taleplerini ve ekosistem iyileştirme önerilerini buraya ekle.
> Durum: `Open` | `In Progress` | `Done` | `Deferred`

---

## [2026-04-06] OpenRouter Multi-Provider Agent Desteği

**Status:** `Open`

**Talep:** Agent registry'sine Gemini ve GPT modellerini OpenRouter üzerinden ekle.

**Bağlam:**
- Sistemde `OPENROUTER_API_KEY` secret'ı mevcut
- Tüm worker agent'lar şu an Claude-only (Opus/Sonnet/Haiku)
- Gemini Flash → çok ucuz tarama/içerik görevleri için ideal (şu an Haiku'nun yaptığı işler)
- GPT-4o → bazı kullanıcıların tercih ettiği alternatif reasoning

**Öneri:**
1. OpenRouter wrapper agent tanımla (örn: `R1 OpenRouter Proxy`)
2. Agent registry'de `provider: openrouter` alanı ekle
3. Model mapping: `gemini-flash` → tarama/içerik (H8, H5 gibi Haiku görevler), `gpt-4o` → opsiyonel alternatif
4. `/project-analysis` mod seçimine "4) Karma (Gemini/GPT maliyet optimizasyonu)" ekle

**Kaynak:** transcriptr project-analysis oturumunda kullanıcı talebi.
