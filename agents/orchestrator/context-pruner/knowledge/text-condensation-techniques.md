# Text Condensation Techniques

## Core Condensation Principles

1. **Preserve factual information, names, and sequences** — never drop key entities
2. **Combine similar points** — merge redundant statements into a single assertion
3. **Telegraphic English** — drop articles and connectors where meaning is clear
4. **Use abbreviations** — standard, domain-known abbreviations only
5. **Lists over prose** — bullet format conveys the same info in less space
6. **Preserve numerical style** — "1,000" → "1k"; don't alter data representation

## Progressive Condensation Steps

Apply in order for maximum compression:

### Step 1: Remove Non-Essential Words
- Drop filler phrases ("I think", "It is worth noting that", "As mentioned above")
- Replace "in order to" → "to"
- Replace "due to the fact that" → "because"
- Drop "very", "really", "quite", "actually"

### Step 2: Combine and Merge
- Merge sentences with the same subject
- Consolidate lists: "We have X, Y, and Z" → bullet points
- Combine qualifications: "It is good but also fast" → "good and fast"

### Step 3: Abbreviate and Compress
- Industry jargon → accepted shortforms
- Long phrases → noun phrases ("the process of authentication" → "auth")
- Narrative description → factual statements

## Context Window Management

When pruning conversation context:

### What to KEEP
- Goal statements and task definitions
- Decisions made (with brief rationale)
- Key outputs (file paths, IDs, results)
- Error messages and resolutions
- User preferences and constraints stated

### What to DROP
- Exploratory reasoning that led nowhere
- Failed attempts (except lessons learned)
- Repeated instructions already confirmed
- Verbose tool call outputs (summarize to key finding)
- Emotional/conversational filler

### Summary Template
```
## Context Summary (turn {N})
Goal: {1 sentence}
Done: {bullet list of completed steps}
Key outputs: {file paths, IDs, values}
Pending: {what's next}
Constraints: {still active constraints}
```

## Quality Check for Condensed Output

After condensing, verify:
- [ ] All key facts preserved?
- [ ] No ambiguity introduced?
- [ ] Sequences and ordering intact?
- [ ] Domain terminology preserved?
- [ ] Actionable items still clear?
