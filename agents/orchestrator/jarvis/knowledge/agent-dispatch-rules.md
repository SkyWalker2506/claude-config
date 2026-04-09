---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Agent Dispatch Rules

## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---

## Temel Kural
Jarvis ASLA kod/design yazmaz. Her uretim isi ilgili agent'a dispatch edilir.

## Dispatch Tablosu

### Kod / Backend
| Gorev | Agent | Tier |
|-------|-------|------|
| Flutter widget/sayfa | B15 Mobile Dev | mid |
| React/web component | B3 Frontend Coder | mid |
| Backend API / DB | B2 Backend Coder | mid |
| Mimari karar | B1 Backend Architect | senior |
| Security audit | B13 Security Auditor | senior |
| Test yazma | B14 Test Writer | mid |
| Bug arastirma | B6 Bug Hunter | mid |
| Refactor | B7 Refactor Agent | mid |

### Design / UX
| Gorev | Agent | Tier |
|-------|-------|------|
| UX arastirma / rakip analizi | D1 UI/UX Researcher | mid |
| Design token / theme | D2 Design System | mid |
| Animasyon / motion | D10 Motion Graphics | junior |
| Mockup review | D8 Mockup Reviewer | mid |

### AI / Sistem
| Gorev | Agent | Tier |
|-------|-------|------|
| Agent mimarisi | N6 AI Systems Architect | senior |
| Skill tasarimi | N7 Skill Design Specialist | mid |
| Workflow tasarimi | N8 Workflow Engineer | mid |
| Prompt yazma | N1 Prompt Engineer | mid |
| Tool degerlendirme | K9 AI Tool Evaluator | junior |

### Proje Yonetimi
| Gorev | Agent | Tier |
|-------|-------|------|
| Jira islemleri | I1 Jira Manager | mid |
| Sprint planlama | I3 Sprint Planner | mid |

## Routing Kurallari

1. **Tek alan** → direkt ilgili agent'a dispatch
2. **Coklu alan** (frontend + backend) → her isi ayri agent'a paralel dispatch
3. **Belirsiz** → A2 Task Router'a sor veya kullaniciya sor
4. **Cascade** → bir agent'in ciktisi digerine girdi olabilir (D2 token → B15 implement)

## Tier → Model Esleme
| Tier | Model | Maliyet |
|------|-------|---------|
| junior | haiku / free | En dusuk |
| mid | sonnet / free | Orta |
| senior | opus | En yuksek — sadece gerekli ise |

## Jarvis'in Kendisi Ne Yapar
- Sohbet, planlama, karar danisma
- Git komutlari, commit, PR
- Agent dispatch ve sonuc takibi
- Raporlama ve ozet
- Agent sharpen tetikleme
- Memory/knowledge guncelleme
