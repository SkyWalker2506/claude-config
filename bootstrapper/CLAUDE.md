# Bootstrapper — Yeni Proje Olusturucu

> Bu klasorde `claude` calistirinca aktif olur. Amaci: `~/Projects/` altina yeni proje klasoru olusturmak ve Claude Code ile calismaya hazir hale getirmek.

---

## Gorev

Kullanici senden yeni proje olusturmani istediginde asagidaki adimlari uygula. Kullanici sadece `claude` yazip girdiyse, ona ne yapmak istedigini sor.

---

## Adim 1 — Bilgi Toplama

Kullanicidan su bilgileri al (parametre olarak verilmemisse sor):

| Bilgi | Ornek | Zorunlu |
|-------|-------|---------|
| Proje adi | `my-app` | Evet |
| Stack | flutter / next / react / node / python / go / rust / custom | Evet |
| Jira proje anahtari | `MYAPP` | Hayir |
| Git remote URL | `git@github.com:user/repo.git` | Hayir |

**Validasyon:**
- Proje adi: kebab-case veya snake_case, bosluk yok
- `~/Projects/<proje-adi>` zaten varsa → UYAR, dur, kullaniciya sor
- Stack bilinmiyorsa → `custom` sec, framework/paket yoneticisi/test/lint komutlarini kullaniciya sor

### Stack haritasi

| Stack | Framework | Paket Yoneticisi | Test | Lint |
|-------|-----------|------------------|------|------|
| `flutter` | Flutter/Dart | flutter pub | flutter test | flutter analyze |
| `next` | Next.js | pnpm | pnpm test | pnpm lint |
| `react` | React (Vite) | pnpm | pnpm test | pnpm lint |
| `node` | Node.js | pnpm | pnpm test | pnpm lint |
| `python` | Python | pip/uv | pytest | ruff |
| `go` | Go | go mod | go test ./... | golangci-lint run |
| `rust` | Rust | cargo | cargo test | cargo clippy |

---

## Adim 2 — Klasor Yapisi

```
~/Projects/<proje-adi>/
  CLAUDE.md                    ← Proje kurallari (template'den)
  .claude/
    settings.json              ← MCP + hook'lar (template'den)
  .gitignore                   ← Stack'e gore
  docs/                        ← Dokumantasyon
  analysis/                    ← Analiz raporlari (/project-analysis ciktisi)
```

Jira varsa ek:
```
  docs/CLAUDE_JIRA.md          ← Jira entegrasyonu
```

**Baska dosya olusturma.** Framework init (`flutter create`, `npx create-next-app` vs.) calistirma — kullanici kendisi yapar.

---

## Adim 3 — CLAUDE.md Olustur

`~/Projects/claude-config/templates/project-claude.md` sablonunu oku ve placeholder'lari degistir:

| Placeholder | Kaynak |
|-------------|--------|
| `__PROJECT_NAME__` | Proje adi |
| `__FRAMEWORK__` | Stack haritasindan |
| `__PKG_MANAGER__` | Stack haritasindan |
| `__TEST_CMD__` | Stack haritasindan |
| `__LINT_CMD__` | Stack haritasindan |
| `__JIRA_KEY__` | Kullanicidan (yoksa "Yok") |

---

## Adim 4 — .claude/settings.json Olustur

`~/Projects/claude-config/templates/project-settings.json` sablonunu oku ve placeholder'lari degistir:

| Placeholder | Kaynak |
|-------------|--------|
| `__TEST_CMD__` | Stack haritasindan |

**Stack'e gore ek MCP:**
- `flutter` → `enabledMcpjsonServers` icine `"flutter-dev"`, `"firebase"` ekle
- Diger stack'ler → default liste yeterli

---

## Adim 5 — .gitignore Olustur

**Ortak (tum stack'ler):**
```gitignore
# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Claude
.claude/jcodemunch_indexed
```

**Stack-spesifik ekler:**

| Stack | Ekler |
|-------|-------|
| `flutter` | `.dart_tool/`, `build/`, `.flutter-plugins*`, `*.iml` |
| `next` | `.next/`, `node_modules/`, `out/`, `.vercel` |
| `react` | `node_modules/`, `dist/`, `build/` |
| `node` | `node_modules/`, `dist/`, `coverage/` |
| `python` | `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/` |
| `go` | `bin/`, `vendor/` |
| `rust` | `target/` |

---

## Adim 6 — Jira (varsa)

Jira key verilmisse `docs/CLAUDE_JIRA.md` olustur:

```markdown
# <PROJE_ADI> — Jira Entegrasyonu

## Proje
- **Jira Key:** <JIRA_KEY>
- **Board:** (doldurulacak)

## Workflow
| Durum | Transition ID | Kullanim |
|-------|--------------|----------|
| In Progress | 21 | Ise baslarken |
| Done | 31 | Is tamamlaninca |
| WAITING | 7 | Onay/credential beklerken |

## Notlar
Projeye ozel Jira kurallari buraya yazilir.
```

---

## Adim 7 — Git Init + Ilk Commit

```bash
cd ~/Projects/<proje-adi>
git init
git add -A
git commit -m "chore: bootstrap project with claude-config scaffolding"
```

Remote verilmisse:
```bash
git remote add origin <url>
```

---

## Adim 8 — Rapor

Islem bitince su formatta rapor ver:

```
## Proje Olusturuldu: <proje-adi>

| Ozellik | Deger |
|---------|-------|
| Konum   | ~/Projects/<proje-adi> |
| Stack   | <stack> |
| Jira    | <key veya Yok> |
| Git     | Initialized |

### Olusturulan Dosyalar
- CLAUDE.md
- .claude/settings.json
- .gitignore
- docs/
- analysis/
(jira varsa: docs/CLAUDE_JIRA.md)

### Sonraki Adimlar
1. `cd ~/Projects/<proje-adi> && claude`
2. Framework kur: <stack'e gore komut>
3. CLAUDE.md'yi projeye ozel detaylarla guncelle
```

---

## Kurallar

1. **Sadece iskelet olustur** — framework init calistirma (`flutter create`, `npx create-next-app` vs.)
2. **Template'leri `~/Projects/claude-config/templates/` altindan al** — hardcode etme
3. **Var olan klasoru ezme** — zaten varsa dur
4. **Secret yaratma** — `.env.example` olabilir ama gercek deger koyma
5. **Parent `~/Projects/CLAUDE.md`'ye dokunma** — o yonlendirici, devralinir
6. **Turkce konusma, Ingilizce kod/commit**
7. **Model etiketi:** yanit basinda `(Model Adi)`
