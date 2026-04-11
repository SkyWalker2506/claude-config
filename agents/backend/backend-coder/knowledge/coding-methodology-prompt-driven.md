# Coding Methodology: Prompt-Driven Development

## Core Principles

1. **Think step-by-step first** — Describe the plan in pseudocode before writing code
2. **Confirm, then code** — Verify understanding of requirements before implementation
3. **Write complete code** — No TODOs, no placeholders, no missing pieces
4. **Correctness over cleverness** — Accurate, bug-free, working code first; optimize after
5. **Readability over performance** — Unless performance is the explicit requirement

## Code Quality Checklist

Before submitting any code:
- [ ] All requested functionality fully implemented
- [ ] No TODOs or placeholder comments remaining
- [ ] All imports included
- [ ] Key components properly named (e.g., index.html, main.py)
- [ ] Mobile-friendly for UI code
- [ ] Up-to-date with current language/framework best practices
- [ ] Secure — no obvious vulnerabilities
- [ ] Performant and efficient

## Debug Workflow

When code doesn't work:
1. Re-read the error message carefully
2. Identify which line/component is failing
3. Form a hypothesis about the root cause
4. Add targeted logging/print statements if needed
5. Fix one thing at a time — don't shotgun
6. After fix: verify the change didn't break adjacent behavior

## Code Review Process

When reviewing code, check in order:
1. **Correctness** — Does it do what it claims?
2. **Security** — SQL injection, XSS, exposed secrets, unvalidated input
3. **Performance** — N+1 queries, unnecessary loops, missing indexes
4. **Readability** — Can another dev understand this in 6 months?
5. **Tests** — Are edge cases covered?

## Pseudocode-First Pattern

For complex features, always start with:
```
# Plan:
# 1. Receive input X
# 2. Validate: check for Y and Z
# 3. Transform: apply logic A
# 4. Persist: write to database via B
# 5. Return: formatted response C
```

Then implement each step, one at a time.

## When Uncertain

- Say "I'm not certain" rather than guessing
- Provide two approaches and their trade-offs
- Flag assumptions explicitly: "Assuming X is the case..."
