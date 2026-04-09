---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Client Documentation

## Quick Reference

**Client-facing docs:** onboarding guide, **architecture / security** FAQ, **API** reference (if applicable), **support** SLAs, **change management** process. **Single source of truth** — avoid duplicating numbers across PDF and portal.

| Doc type | Owner often | Update trigger |
|----------|-------------|----------------|
| Getting started | Product / CS | Each major release |
| SLA / support | Legal / Ops | Contract change |
| Security overview | Security | Annual + incidents |

**2025–2026:** AI search on docs portals — structure with clear headings; chunk-friendly.

## Patterns & Decision Matrix

| Audience | Format |
|----------|--------|
| Admins | Checklists + screenshots |
| Developers | OpenAPI + code samples |
| Exec | 1-pager assurance summary |

## Code Examples

**Info architecture (URL pattern):**

```text
https://docs.{{vendor}}.com/
  /get-started/
  /security/
  /api/reference/
  /support/sla
```

**Support SLA table (Markdown):**

```markdown
| Severity | Definition | First response | Update cadence |
|----------|------------|----------------|------------------|
| P1 | Production down | 30 min | 1 h |
| P2 | Major degradation | 4 h | 8 h |
| P3 | Minor | 1 bd | 2 bd |
```

**“Where to find X” one-pager for kickoff:**

```text
Credentials: {{idp}} — your IT admin provisions via {{link}}
Status page: https://status.{{vendor}}.com
Support portal: https://support.{{vendor}}.com — reference ticket format TCK-{{account_id}}
```

**Version footer on PDFs:**

```text
Document version 2.3 — 2026-04-09 — Classification: Customer Confidential
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Stale screenshots | Release checklist item |
| Different numbers than contract | Reference order form § |
| PDF-only for developers | API docs in searchable HTML |

## Deep Dive Sources

- [Write the Docs](https://www.writethedocs.org/) — documentation community
- [Diátaxis framework](https://diataxis.fr/) — doc types (tutorial/how-to/reference)
- [OWASP — security documentation](https://owasp.org/) — customer security FAQs
- [OpenAPI Initiative](https://www.openapis.org/) — API spec standard
