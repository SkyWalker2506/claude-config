# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.

## 2026-04-09 | Agent Overhaul — Initial Setup

**Source:** Bu session'daki agent overhaul calismasi

**Key findings:**

1. **Jarvis asla kod/design yazmaz** — sadece dispatch. Bu kullanici tercihi, zorunlu kural.
2. **Dispatcher agent (A2) kullanilabilir** — routing karmasik ise A2'ye devret.
3. **Proje-spesifik bilgi Jarvis'te kalmaz** — ilgili agent'a aktar, onu sharpen et.
4. **Knowledge-First yapi calisiyor** — 11 agent setup edildi, 56+ knowledge dosyasi olusturuldu.
5. **MemPalace MCP olarak baglandi** — tum session'larda gecmis aranabilir.
6. **Tier = sadece model secimi** — ayni dosyalar, farkli guc. Refine her zaman opus.
7. **agent-skills (Google) formatindan ogrenilen:** Phase 0 pre-flight, Output Format, Error Handling her agent'ta olmali.
8. **Musab otonom calisma tercih eder** — minimum soru, varsayimla ilerle.
