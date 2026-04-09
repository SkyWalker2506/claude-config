---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Calculator Builder Guide

## Quick Reference

**Core loop:** Define formula → validate inputs → deterministic output → optional sensitivity table.

- **Determinism:** Same inputs → same outputs; document rounding and tax assumptions in UI.
- **Units:** Store internal SI or base unit; format for display only (avoid mixed currency without FX source).
- **Edge cases:** Zero, negative where invalid, caps—return inline errors, not silent clamping unless disclosed.
- **Bridge to M3:** If **M3 A/B Test Agent** runs headline or input-order tests, keep formula version in `logic_version` for analysis.
- **Bridge to M2:** **M2** places calculator above fold or in sticky module—reserve `data-testid` hooks for QA.

| Layer | Responsibility |
|-------|----------------|
| Domain | Business rules (e.g. tier thresholds) |
| Presentation | Formatting, charts |
| Persistence | Saved scenarios (auth) |

## Patterns & Decision Matrix

| Stack | Pros | Cons |
|-------|------|------|
| Static HTML + JS | Fast, cheap host | No server-side secret formulas |
| Edge function | Hide proprietary multipliers | Cold start, cost |
| Spreadsheet export | PM-friendly | Drift vs code |

**Chart choice**

| Data | Chart |
|------|-------|
| Single scalar result | Big number + delta vs baseline |
| Range sweep | Line or area |
| Tier comparison | Horizontal bar |

## Code Examples

**1) Pure calculation module (TypeScript)—testable**

```typescript
export type CalcInput = { seats: number; pricePerSeat: number; discountPct: number };

export function annualContractValue(i: CalcInput): number {
  if (i.seats < 1 || i.pricePerSeat < 0) throw new Error('invalid_input');
  const gross = i.seats * i.pricePerSeat * 12;
  return gross * (1 - i.discountPct / 100);
}
```

**2) Versioned logic for experiments (JSON)**

```json
{
  "logic_version": "2026.04.1",
  "formula": "annualContractValue",
  "assumptions": ["12_month_contract", "usd_list"],
  "experiments": [{ "id": "exp_headline_calc", "m3_owner": true }]
}
```

## Anti-Patterns

- **Magic numbers in UI:** Business constants only in one module with comments and tests.
- **String math:** Use decimal library for money if language floats are unsafe at scale.
- **Copying competitor formulas** without legal review—risk of misrepresentation.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [MDN — Intl.NumberFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat) — locale-safe currency display
- [Decimal.js (npm)](https://mikemcl.github.io/decimal.js/) — precision for billing math
- [Testing Library — user-centric tests](https://testing-library.com/) — calculator UI tests
- [OWASP — client-side security](https://owasp.org/www-project-web-security-testing-guide/) — never trust client for authoritative pricing
