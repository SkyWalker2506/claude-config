# Mega rollout — worker prompt şablonu

Aşağıdaki bloğu Cursor Composer’a yapıştır; `{SCOPE}` ve `{SKIP}` yerlerini tablodan doldur.

---

Sen `~/Projects/claude-config` reposunda çalışıyorsun.

**Scope:** `{SCOPE}` altındaki agent klasörleri (ör. `agents/code-review/lint-format-hook/`).

**Dokunma:** [MEGA_BATCH_MANIFEST.md](../MEGA_BATCH_MANIFEST.md) içindeki “DOKUNMA” listesi — bu path’lere **hiç dokunma**.

**Görev (her agent klasörü için):**
1. `AGENT.md` — YAML `---` **hariç** body’yi mega-prompt’taki formata göre doldur: Identity (gerçek dünya rolü), Always/Never/Bridge (**çift yönlü** — A↔B), Process fazları, Output Format (somut örnek), When to Use/NOT, Red Flags, Verification, Error Handling, Escalation.
2. `knowledge/` — mega-prompt tablosundaki **tam dosya adlarıyla** 4+ markdown oluştur: Quick Reference, Patterns & Decision Matrix, Code Examples (≥2), Anti-Patterns, Deep Dive Sources (≥3 link). `sources:` frontmatter ≥3.
3. `knowledge/_index.md` güncelle: `total_topics`, link listesi.

**Kalite:** Jenerik şablon kopyalama yok; domain’e özel. Bridge’de referans verilen agent’ın kendi `AGENT.md` Bridge’inde karşılık mümkünse ekle.

**Bitince:** `~/Projects/claude-config/bin/mega-rollout.sh verify` çıktısını kontrol et.

---

**Bu worker’ın scope’u:** İlgili `W*.md` dosyasındaki **Scope path** + klasör listesi.

**Atlanacak klasörler:** `{SKIP}` (o `W*.md` içindeki **Skip** ile aynı)
