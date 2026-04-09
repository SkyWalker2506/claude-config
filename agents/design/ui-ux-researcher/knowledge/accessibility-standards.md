---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Accessibility Standards — WCAG 2.2 AA

## Touch Targets
- Minimum 48x48dp (WCAG 2.5.8 Target Size)
- 24dp minimum with 24dp spacing allowed (sparse layouts)
- VocabApp quiz answer buttons: ensure >=48dp height

## Color Contrast
- Normal text (<18pt): 4.5:1 ratio minimum
- Large text (>=18pt bold or >=24pt): 3:1 ratio minimum
- Non-text UI (icons, borders): 3:1 ratio minimum
- VocabApp uses `AppColors` with pre-calculated contrast — verify new additions

## Screen Reader (Flutter Semantics)
```dart
// Label non-text elements
Semantics(
  label: 'Streak: 5 days',
  child: StreakChip(count: 5),
)

// Exclude decorative elements
ExcludeSemantics(child: DecorativeIcon())

// Announce state changes
SemanticsService.announce('Correct answer!', TextDirection.ltr);
```

## Focus Management
- Logical tab order (top-to-bottom, left-to-right)
- Focus trap inside dialogs/bottom sheets
- Return focus to trigger after dialog closes
- Skip repetitive navigation with `Semantics(sortKey:)`

## Motion & Vestibular
- Respect `MediaQuery.disableAnimations` (VocabApp has `animDuration()` helper)
- No auto-playing animations >5s without pause
- Parallax and zoom effects need reduce-motion fallback

## Content
- Meaningful link/button text (not "Click here")
- Error messages: state what's wrong + how to fix
- Form labels always visible (not placeholder-only)
- Language attribute set on localized content

## WCAG 2.2 AA Checklist
- [ ] 2.4.7 Focus Visible — focus indicator on all interactive elements
- [ ] 2.5.8 Target Size — 48dp minimum or 24dp with spacing
- [ ] 1.4.3 Contrast — 4.5:1 text, 3:1 non-text
- [ ] 1.4.11 Non-text Contrast — UI components 3:1
- [ ] 2.4.6 Headings — descriptive, hierarchical
- [ ] 3.3.2 Labels — all inputs labeled
- [ ] 2.5.4 Motion Actuation — alternatives for shake/tilt
- [ ] 1.3.4 Orientation — no orientation lock
- [ ] 3.2.6 Consistent Help — help in same location across pages
