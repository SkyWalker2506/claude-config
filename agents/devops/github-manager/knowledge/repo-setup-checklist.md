---
last_updated: 2026-04-10
refined_by: coverage-bootstrap
confidence: high
sources: 3
---

# Repo setup checklist (new GitHub repo)

## Quick Reference

| Adım | Kontrol |
|------|---------|
| LICENSE | MIT / Apache — hedef kitleye uygun |
| .gitignore | OS, IDE, build çıktıları |
| Branch default | `main` |
| Description + topics | Keşfedilebilirlik |

## Patterns & Decision Matrix

| Visibility | Ek |
|------------|-----|
| Public | SECURITY.md düşün |
| Private | Erişim listesi |

## Code Examples

```bash
gh repo create org/name --public --source=. --remote=origin --push
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Secrets commit | Credential leak |

## Deep Dive Sources

- [GitHub — Creating a repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [Choose a License](https://choosealicense.com/)
