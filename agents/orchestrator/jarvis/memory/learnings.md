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

## 2026-04-12 | Sharpening — 3d-asset-foundry + Filler Strip

**Source:** Bu session — ARCHITECTURE.md/STRUCTURE.md drift analizi + knowledge audit

**Key findings:**

1. **5 knowledge dosyasinda ozdes jenerik filler block vardi** (Quick Reference/Patterns/Code Examples/Anti-Patterns/Deep Dive Sources — hepsi "Bu dosyanin devamindaki" dolgu metni). Sinyali zayiflatiyordu, hepsi silindi. Sonraki sharpen'de benzer auto-generated stub olup olmadigini kontrol et.

2. **3d-asset-foundry projesi ecosystem'de eksikti.** Python tabanli, Blender subprocess, multi-LLM refinement loop, ARCHITECTURE v0.10 + STRUCTURE v0.10. Phase 0 scaffold asamasinda; 5 blocker modul (vault_token, aggregator, vault_reader, escalation, schema_repair) ve 7 invariant test eksik.

3. **§4.6 reference_vault isolation kritik commercial boundary.** Sadece `comparison/vault_reader.py` erisebilir; AST tabanli purity testi (test_comparison_purity.py) bu kurali enforce eder. Bu projede vault-related kod review'i B13 Security Auditor'a gitmeli.

4. **agent-dispatch-rules'da catiskisi vardi:** AGENT.md "git isini dispatch et" diyor, dispatch-rules.md "Jarvis kendi yapar" diyordu. AGENT.md truth kabul edildi, dispatch-rules duzeltildi.

5. **Python/3D kategorisi dispatch tablosunda yoktu** — Flutter-agirlikli ekosistem varsayimi. Yeni satir eklendi: Python impl → B2, mimari → B1, Blender → B2+context7, security → B13, 3D spec → C1.

6. **Yeni kullanici pattern'i: "kod yazma, sadece todo olarak yaz aciklama"** — drift/gap analizi + kategorize edilmis P0/P1/P2 bullet TODO listesi + implementer agent onerisi beklentisi. Kod uretimi kesinlikle yok. Bu mod user-preferences'a eklendi.

7. **Invariant testler asla skip/xfail yapilmamali** (STRUCTURE.md kurali) — cross-project-patterns'a Python projeleri bolumune not edildi. CI gate commercial story'yi korur.
