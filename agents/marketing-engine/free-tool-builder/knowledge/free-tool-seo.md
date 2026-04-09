---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Free Tool SEO

## Quick Reference

- **Indexable URL:** `/tools/{slug}` with stable content; avoid infinite query combinations as canonical chaos—use `noindex` for infinite permutations or `canonical` to base URL.
- **Title pattern:** `{Primary benefit} — Free {Tool type} | {Brand}` (≤~60 chars where possible).
- **Structured data:** `WebApplication` or `SoftwareApplication` + `FAQPage` if you have FAQ block.
- **Bridge to M2:** **M2 Landing Page Agent** may host a *marketing narrative* at `/lp/{campaign}` pointing to same tool—set `rel=canonical` on duplicate campaign LPs to `/tools/{slug}` unless campaign is intentionally unique content.
- **Core Web Vitals:** Tools often fail LCP on heavy charts—lazy-load chart libs, skeleton placeholders.

| Page element | SEO role |
|--------------|----------|
| H1 | Primary query + intent |
| Intro paragraph | Semantic coverage (synonyms) |
| Result share | Social + backlinks (Open Graph) |

## Patterns & Decision Matrix

| Situation | Action |
|-----------|--------|
| Multi-step wizard | One URL + JS steps OK; ensure critical text in HTML for crawlers or SSR |
| Per-result share pages | `noindex` thin pages OR unique blurbs per outcome |
| Embeddable widget | `iframe` on partner sites—link back with branded anchor |

**Sitemap**

| Tool type | Changefreq | Priority |
|-----------|------------|----------|
| Evergreen calculator | monthly | 0.7 |
| Campaign quiz | weekly during campaign | 0.5 |

## Code Examples

**1) JSON-LD SoftwareApplication**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "ACV ROI Calculator",
  "applicationCategory": "BusinessApplication",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "description": "Estimate annual contract value and savings vs spreadsheets."
}
</script>
```

**2) Canonical guard (meta)**

```html
<link rel="canonical" href="https://example.com/tools/roi-calculator" />
<meta name="robots" content="index,follow,max-image-preview:large" />
```

## Anti-Patterns

- **Keyword stuffing** in hidden divs—violates Google spam policies.
- **Soft-404** empty result pages indexed.
- **Duplicate tool** at `/calc` and `/calculator` without consolidation.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Search Central — Canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) — duplicate handling
- [Google Search Central — Structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) — rich results
- [Schema.org — SoftwareApplication](https://schema.org/SoftwareApplication) — vocabulary
- [web.dev — Core Web Vitals](https://web.dev/vitals/) — performance thresholds
