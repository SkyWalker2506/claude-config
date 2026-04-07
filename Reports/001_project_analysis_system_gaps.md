# Report 001 — Project Analysis System: Gaps & Required Actions

> Date: 2026-04-07  
> Source: User feedback during ArtLift /project-analysis session  
> Status: UNPROCESSED  
> Priority: High

---

## Context

Kullanıcı `/project-analysis` skill'ini ArtLift projesinde çalıştırırken sistemdeki eksiklikleri tespit etti ve iletti.

---

## Identified Gaps

### 1. Lead Agent Role Ambiguity (PROJECT_ANALYSIS.md §2 + §5)

**Sorun:** §2'deki "dispatches" ifadesi ve §5'teki Lead prompt şablonu çelişiyor.

- §2: `A9 ArtLead → dispatches: B3, D1, D2, D8, H8` → Lead ayrı worker'lara iş devrediyor izlenimi veriyor
- §5: Lead prompt şablonu Lead'in kendisinin araştırma + rapor yazdığını gösteriyor
- Claude bu belirsizlik yüzünden Lead'e "worker dispatcher" promptu yazmak üzereydi — kullanıcı uyarmadan bu hata gerçekleşecekti

**Aksiyon:** `PROJECT_ANALYSIS.md §2`'ye açıklayıcı not ekle:
```
> NOT: "dispatches" ifadesi ayrı process başlatmayı değil, 
> Lead'in o worker rolünün bakış açısıyla analiz yapmasını ifade eder. 
> Her Lead kendi kategorilerini §5 şablonuna göre BİZZAT analiz eder.
```

---

### 2. Free/Local Agent Model Mapping Eksik (PROJECT_ANALYSIS.md §4)

**Sorun:** Registry'de `free-web`, `free-script`, `local-qwen-9b` model tipleri var ama Claude Code Agent tool bu tipleri tanımıyor. Hangi Claude modeline map edileceği belirsiz.

**Aksiyon:** §4 tablosuna `Claude Code Model` kolonu ekle:

| Registry Model | Claude Code Model | Notlar |
|---|---|---|
| `free-web` | `haiku` | Sadece fetch/search — en ucuz model yeterli |
| `free-script` | `haiku` | Bash çalıştırır — model çok önemli değil |
| `local-qwen-9b` | `haiku` veya OpenRouter | Ollama varsa skip, yoksa haiku fallback |
| `free-gemini` | OpenRouter curl | `$OPENROUTER_API_KEY` ile çağır |

---

### 3. Gemini Desteği Eksik

**Sorun:** Kullanıcı UI/UX analizi için Gemini tercih ediyor. Sistemde `free-gemini` model tipi tanımlı değil, Lead prompt şablonunda bu tip için dispatch kuralı yok.

**Aksiyon:**
1. Agent registry'e `free-gemini` tipi ekle
2. `scripts/gemini-call.sh` wrapper oluştur (OpenRouter üzerinden)
3. §5 Lead prompt şablonuna ekle: `model: free-gemini → Bash ile OpenRouter çağrısı`
4. D1 (UI/UX Researcher) agent'ının `primary_model`'ini `free-gemini` olarak güncelle

---

### 4. Startup Hook: Unprocessed Reports Kontrolü Eksik

**Sorun:** `Reports/` klasöründe bekleyen raporlar var ama startup hook bunu kontrol etmiyor. Raporlar okunmadan kalıyor.

**Aksiyon:** `migration_check.sh` veya ayrı bir `reports_check.sh` hook'una şu mantığı ekle:
```bash
UNPROCESSED=$(ls ~/Projects/claude-config/Reports/*.md 2>/dev/null | grep -v REPORTS_SUMMARY.md)
if [ -n "$UNPROCESSED" ]; then
  echo "📋 REPORTS_PENDING: $(echo "$UNPROCESSED" | wc -l | tr -d ' ') işlenmemiş rapor var."
  echo "   Aksiyon: Raporları oku ve uygula → Processed/ klasörüne taşı"
fi
```

---

### 5. PROJECT_ANALYSIS.md Skill Entegrasyonu: Startup'ta Okunmuyor

**Sorun:** `/project-analysis` skill'i `PROJECT_ANALYSIS.md`'yi okumadan Lead'leri başlatmak üzere. Skill başlamadan önce §5 şablonunu okuma zorunluluğu skill tanımında yok.

**Aksiyon:** `/project-analysis` skill SKILL.md'sine ekle:
```
## Başlamadan Önce ZORUNLU Oku
- `__PROJECTS_ROOT__/PROJECT_ANALYSIS.md` §2, §4, §5
- §5 şablonunu Lead prompt'larına birebir uygula
- §4'teki model mapping'i kullan
```

---

## Required Actions Summary

| # | Dosya | Değişiklik | Öncelik |
|---|-------|-----------|---------|
| 1 | `projects/PROJECT_ANALYSIS.md §2` | "dispatches" belirsizliğine açıklayıcı not | High |
| 2 | `projects/PROJECT_ANALYSIS.md §4` | `Claude Code Model` kolonu ekle | High |
| 3 | `agents/design/ui-ux-researcher.md` | `primary_model: free-gemini` | Medium |
| 4 | `scripts/gemini-call.sh` | OpenRouter Gemini wrapper oluştur | Medium |
| 5 | `projects/PROJECT_ANALYSIS.md §5` | `free-gemini` dispatch kuralı ekle | Medium |
| 6 | `config/reports_check.sh` | Unprocessed reports hook'u | High |
| 7 | `global/skills/project-analysis/SKILL.md` | §2/§4/§5 okuma zorunluluğu ekle | High |
