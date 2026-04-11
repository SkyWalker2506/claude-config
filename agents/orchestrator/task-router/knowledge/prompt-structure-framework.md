# Prompt Structure Framework (LangGPT Method)

## Core Template Structure

When designing prompts for agents or sub-tasks, use this structured format:

```
Role: {who the agent is}
Profile: {background, expertise, domain}
Skills: {specific capabilities}
Rules: {constraints, what not to do}
Workflow: {step-by-step operating procedure}
Tools: {available tools and when to use them}
```

## Five Essential Components of Any Prompt

1. **Define the Persona** — Who is this agent? What domain do they specialize in?
2. **Set the Context** — Background information that narrows the relevant domain
3. **Clarify the Task and Goal** — Start with an action verb; make the desired outcome explicit
4. **Determine Essential Information** — What specific inputs are needed to execute?
5. **Establish Constraints** — Boundaries that guide toward accuracy and quality

## Prompt Writing Principles

- Always use: `YOU + ACTION + INSTRUCTION` structure
- Be explicit about format expectations (bullet lists, markdown, code blocks)
- State what NOT to do as clearly as what to do
- Negative prompts should be interwoven with positive instructions, not just appended

## Structured Prompt Components

### Pre-conditioning
Prime the model for the task before main instructions. Sets context and mode.

### System Prompt
Core instructions: tools being used, how to behave, domain constraints.

### Negative Prompts
Explicitly state what to avoid — connected by reference within the system prompt.

### Output Format
Define expected output structure: length, format, language, sections.

## Dispatch Prompt Pattern

When routing tasks to sub-agents, include:
1. **Task description** — What needs to be done
2. **Context bundle** — Relevant background the agent needs
3. **Success criteria** — How to know the task is complete
4. **Output format** — How to return results
5. **Constraints** — Time, scope, tool limits

## Quality Signals in Prompts

Good prompt indicators:
- Specific, not vague ("Write a REST endpoint" vs "Write some code")
- Measurable outcome ("Return a JSON object with fields X, Y, Z")
- Constraints stated upfront ("Do not use external libraries")
- Persona matched to task complexity
