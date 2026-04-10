---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# SBOM and supply-chain signals for tool selection

## Quick Reference

| Sinyal | Ne işe yarar |
|--------|----------------|
| **package-lock / pnpm-lock** | Transitive bağımlılık sabitleme |
| **npm audit / osv-scanner** | Bilinen CVE |
| **Sigstore / npm provenance** | Paket bütünlüğü |
| **Maintainer cadence** | Son commit, issue TAT |

CLI ve IDE eklentileri için “tek demo” yerine **en az** kilit dosya + güvenlik taraması öner.

## Patterns & Decision Matrix

| Risk profili | Aksiyon |
|--------------|---------|
| Prod pipeline’a girecek | SBOM + imzalı release şart |
| Sadece lokal deneme | Sandbox + network kısıtı yeterli olabilir |
| Kapalı kaynak SaaS | Veri işleme sözleşmesi + alt işleyen listesi |

## Code Examples

**OSV-Scanner (CI örneği):**

```yaml
# .github/workflows/osv.yml
jobs:
  osv:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google/osv-scanner-action@v1
        with:
          scan-args: |-
            --lockfile=./package-lock.json
```

**npm audit JSON özeti (script):**

```bash
npm audit --json | jq '.metadata.vulnerabilities'
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| `curl | bash` ile prod kurulum | Arka kapı riski |
| Bağımlılık güncellemesini “hep latest” | Kırıcı sürüm |
| Lisansı okumadan kurumsal kullanım | GPL/AGPL çakışması |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [SLSA](https://slsa.dev/) — supply-chain seviyeleri
- [OpenSSF Scorecard](https://scorecard.dev/) — repo güvenlik skoru
- [npm — provenance](https://docs.npmjs.com/generating-provenance-statements) — kanıt bildirimi
- [OSV](https://google.github.io/osv-scanner/) — açık kaynak zafiyet eşlemesi
