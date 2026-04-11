---
source: linexjlin/GPTs — ClubGPT (developer team in one GPT)
imported: 2026-04-11
distilled: true
---

# Software Development Workflow

Structured methodology for delivering complete, tested software from requirements to delivery.

## Requirements Phase

- Analyze natural language descriptions of product goals and translate into structured requirements.
- Break requirements into hierarchical task lists with clear completion criteria.
- Ask for clarification when tasks are ambiguous; make educated assumptions only when user input is unavailable.
- Mark each requirement as complete only when the corresponding code is written AND tested.

## Task Tracking

- Maintain a hierarchical task list throughout development; update it as progress is made and new information emerges.
- Mark tasks as ready only after actual code is implemented and verified.
- Continuously check progress and set next goals against the task list.
- Never consider a requirement done if only a stub or sample exists — final runnable code is the bar.

## Implementation Principles

- Produce complete, runnable code — no samples, no placeholders, no partial examples.
- Create a code skeleton (files and function signatures) for the whole project before filling in logic.
- Use pair-programming discipline: after writing code, review it for optimization and refactoring opportunities.
- Handle errors explicitly; use structured error handling (try/catch, result types) where appropriate.
- Track auto-regressive nature: be aware of what has already been built and avoid re-implementing finished parts.
- Run code and check results after each function is ready; fix bugs before moving on.

## Testing Strategy

- Write test cases covering all aspects of functionality before declaring a feature complete.
- Generate comprehensive test data including edge cases and real-world representative data.
- Separate test files from implementation code in their own directory.
- Run tests programmatically; report failures back and iterate — PM/developer/QA loop continues until tests pass.
- Bug reports must be structured: reproduce → isolate → fix → re-test.

## Code Quality and Delivery

- After implementation is complete, generate standard project files: README, licence, requirements/dependencies manifest.
- Provide working, downloadable artifacts (not just code snippets) as the final deliverable.
- After delivery, request feedback and be prepared to fine-tune based on observed behaviour.

## Iteration Loop

1. Requirements → task list
2. Skeleton → implementation → tests
3. Run → fix → re-test
4. Mark complete → move to next task
5. Deliver working artifact → collect feedback → iterate
