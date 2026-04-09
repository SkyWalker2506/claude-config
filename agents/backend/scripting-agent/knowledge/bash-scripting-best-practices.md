---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Bash Scripting Best Practices

## Quick Reference

| Practice | Detail |
|----------|--------|
| **Shebang** | `#!/usr/bin/env bash` |
| **Strict mode** | `set -euo pipefail` |
| **Quoting** | `"$var"` always |
| **Temp files** | `mktemp` |

**2025–2026:** ShellCheck in CI; avoid bash for complex logic — use Python.

## Patterns & Decision Matrix

| Task | Tool |
|------|------|
| JSON | `jq` not raw sed |

## Code Examples

```bash
#!/usr/bin/env bash
set -euo pipefail
main() { echo "$1"; }
main "$@"
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| `rm -rf $DIR` unquoted | Empty var disaster |

## Deep Dive Sources

- [Google — Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck](https://www.shellcheck.net/)
