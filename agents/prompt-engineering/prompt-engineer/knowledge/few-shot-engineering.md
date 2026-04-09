---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Few-Shot Engineering

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

## Core Principle

Show, don't tell. One good example beats 10 lines of instruction.

## Example Selection

### Quality Criteria

1. **Representative** — covers the common case
2. **Diverse** — shows different scenarios, not variations of the same
3. **Edge-covering** — at least one example shows a tricky case
4. **Minimal** — shortest example that demonstrates the point

### How Many Examples

| Task Complexity | Examples Needed |
|----------------|----------------|
| Simple format conversion | 1-2 |
| Classification/routing | 3-5 |
| Complex generation | 2-3 + 1 edge case |
| Style matching | 2-3 of the target style |

More than 5 examples rarely helps — diminishing returns plus token cost.

## Format

### Input/Output Pairs

```
Example 1:
Input: "I want to add user authentication"
Output: "user-auth"

Example 2:
Input: "Fix payment processing timeout bug"
Output: "fix-payment-timeout"
```

### Annotated Examples

Add brief reasoning when the mapping isn't obvious:

```
Input: "Create a dashboard for analytics"
Output: "analytics-dashboard"
Reasoning: action-noun format, dropped generic "create"
```

## Edge Case Coverage

Always include at least one example that shows:
- What NOT to do (negative example)
- A boundary case
- Error handling

```
✅ CORRECT: `- [ ] T001 [US1] Create User model in src/models/user.py`
❌ WRONG: `- [ ] Create User model` (missing ID, story label, file path)
```

## Anti-Patterns

- **All happy path** — no edge cases shown, agent fails on unusual input
- **Too similar** — 5 examples of the same pattern teach nothing new
- **Too long** — examples that are 50+ lines each waste context
- **Unlabeled** — reader can't tell which part is input vs output
- **Contradictory** — examples that conflict with each other or with instructions

## Token-Efficient Few-Shot

When context is limited:
1. Use the shortest examples that demonstrate the pattern
2. Put the most important example first (primacy bias)
3. Remove examples that don't add new information
4. Consider using a single "golden example" instead of many mediocre ones
