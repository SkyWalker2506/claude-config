# Skill Dosyalarında Model Yönlendirmesi Güncellemesi

| | |
|---|---|
| Tarih | 2026-08-26 13:36 |
| Calistiran | agy (gemini-3.7-flash-high, effort high) |
| Dizin | /Users/musabkara/Projects/claude-config |

## Gorev
Claude Code konfigürasyon reposundaki 9 skill dosyasında delege edilen mekanik işlerin model seçimlerini `global/model-routing.md` kuralına göre Sonnet/Haiku yerine `agy (Gemini)` olarak güncellemek, mimari/plan/review/karar aşamalarındaki Opus/Fable referanslarına dokunmamak ve her dosyaya tek satırlık `global/model-routing.md` referansı eklemek.

## Yapilanlar
- `global/skills/prototype/SKILL.md`: Sanat hattı ajanı model tablosunda `sonnet` -> `agy (Gemini)`, Agent çağrısında `model="gemini"` yapıldı; model yönlendirme referansı eklendi.
- `global/skills/team-build/SKILL.md`: Frontmatter, açıklama, akış, config ve önemli kurallarda geçen `Sonnet/Haiku` referansları mekanik kodlama için `agy (Gemini)` olarak güncellendi; Opus spec/review korundu; model yönlendirme referansı eklendi.
- `global/skills/dispatch/SKILL.md`: Strategy tablosundaki `cheap_first`, `two_pass`, `opus_plan` satırlarında mekanik kodlama Sonnet/Haiku yerine `agy (Gemini)` / `gemini` olarak güncellendi; Opus mimari ve review rolleri korundu; model yönlendirme referansı eklendi.
- `global/skills/showrunner/SKILL.md`: G1 ve Faz B'deki arka plan sanat ajanı ve model tablosundaki `/image-run` çalıştırıcı ajanı `agy (Gemini)` olarak güncellendi; Fable plan ve Opus kod/review rolleri korundu; model yönlendirme referansı eklendi.
- `global/skills/gdd-review/SKILL.md`: Uzun GDD bölüm özeti mekanik işi için model tablosundaki `sonnet` -> `agy (Gemini)` olarak güncellendi; puanlama ve v2 rolleri korundu; model yönlendirme referansı eklendi.
- `global/skills/yolo/SKILL.md`: Otonom mekanik yürütücü Agent şablonunda `model="sonnet"` -> `model="gemini"` yapıldı; model yönlendirme referansı eklendi.
- `global/skills/audit/SKILL.md`: Kod tarama Agent şablonunda `model="sonnet"` -> `model="gemini"` yapıldı; model yönlendirme referansı eklendi.
- `global/skills/project-analysis/SKILL.md`: Hızlı mod, dispatch tablosu, watchdog ve summary tablosundaki mekanik analiz lead'leri (ArtLead, CodeLead, GrowthLead, BizLead) `agy (Gemini)` olarak güncellendi; SecLead ve Master (Opus) korundu; model yönlendirme referansı eklendi.
- `global/skills/forge/SKILL.md`: Pre-flight model kontrolü, Task Pipeline Coder modeli, adım 2 kod yazma, summary ve Score agent dispatch satırlarında `Sonnet` -> `agy (Gemini)` olarak güncellendi; Reviewer (Opus) ve Master rolleri korundu; model yönlendirme referansı eklendi.

## Degisen dosyalar
```
 global/skills/audit/SKILL.md            |  4 +++-
 global/skills/dispatch/SKILL.md         |  8 +++++---
 global/skills/forge/SKILL.md            | 20 +++++++++++---------
 global/skills/gdd-review/SKILL.md       |  4 +++-
 global/skills/project-analysis/SKILL.md | 32 +++++++++++++++++---------------
 global/skills/prototype/SKILL.md        |  6 ++++--
 global/skills/showrunner/SKILL.md       | 10 ++++++----
 global/skills/team-build/SKILL.md       | 28 ++++++++++++++--------------
 global/skills/yolo/SKILL.md             |  4 +++-
 9 files changed, 66 insertions(+), 50 deletions(-)
```

## Dogrulama
- `git diff --stat` ve `git diff` ile 9 dosyadaki tüm değişiklikler incelendi; yalnızca hedef satırların değiştiği ve tablo hizalamalarının korunduğu doğrulandı.
- Tüm dosyalarda `grep` ile `sonnet` ve `haiku` taraması yapıldı, delege edilen mekanik işlerde bu modellerin kalmadığı doğrulandı.
- `global/model-routing.md` referansının 9 dosyada da bulunduğu `grep` ile doğrulandı.
- Fable ve Opus içeren kısımların (mimari, tasarım, planlama, derin kodlama, güvenlik, review) korunduğu doğrulandı.

## Yapilmayanlar / bilinen eksikler
yok
