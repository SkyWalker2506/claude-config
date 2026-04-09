---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Hero Section Patterns

## Quick Reference

**Hero jobs:** Communicate *what it is*, *for whom*, *why now*, *next step*—in <5 seconds.

| Pattern | Visual | Copy bias | Best for |
|---------|--------|-----------|----------|
| **Split** | Product UI left, copy right | Feature + outcome | B2B SaaS |
| **Center stack** | Headline + sub + CTA | Brand-led | PLG |
| **Background media** | Video or gradient | Emotional | Consumer |
| **Tool-first** | **M1** embed prominent | Utility | Calculators, graders |

- **CTA hierarchy:** One primary (filled), one secondary (ghost)—tertiary links dilute.
- **Mobile:** Stack copy → CTA → visual; thumb zone for primary button.
- **Bridge to M1:** Hero height must fit iframe min-height + legal footnote without pushing CTA below fold on 390px.
- **Bridge to M3:** Hero is highest-traffic test surface—document pixel baseline for “flicker-free” flag rollouts.

## Patterns & Decision Matrix

| If | Then |
|----|------|
| Complex product | Lead with outcome + screenshot |
| Strong brand | Logo + short punchy H1 |
| Regulated industry | Compliance line under CTA |

**Imagery**

| Type | Risk |
|------|------|
| Real UI | Stale after ship—schedule refresh |
| Abstract 3D | Pretty but vague—pair with concrete H1 |
| People | Must feel authentic, not stock |

## Code Examples

**1) Responsive hero CSS (simplified)**

```css
.hero {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr;
  align-items: center;
}
@media (min-width: 960px) {
  .hero { grid-template-columns: 1fr 1fr; }
}
.hero__cta { justify-self: start; }
```

**2) Accessibility: heading order**

```html
<section aria-labelledby="hero-title">
  <h1 id="hero-title">…</h1>
  <p class="subhead">…</p> <!-- not h2 unless real section title -->
</section>
```

## Anti-Patterns

- **Video autoplay with sound**—violates UX and policies.
- **H1 as logo** or missing H1—SEO and a11y fail.
- **Invisible CTA** (low contrast)—fails WCAG and conversion.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [WebAIM — Contrast checker](https://webaim.org/resources/contrastchecker/) — CTA contrast
- [MDN — Responsive design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design) — layout patterns
- [W3C — WCAG 2.2 Understanding](https://www.w3.org/WAI/WCAG22/Understanding/) — target size, focus
- [Baymard — E-commerce UX](https://baymard.com/) — above-the-fold research (paid + public summaries)
