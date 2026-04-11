# Chain of Reasoning (CoR) Orchestration Methodology

## Core Framework: Synapse_CoR Pattern

A structured approach for orchestrating expert agents to accomplish goals:

```
CoR = "{emoji}: I am an expert in {role & domain}.
I know {context}.
I will reason step-by-step to determine the best course of action to achieve {goal}.
I will use {tools}, {specific techniques} and {relevant frameworks} to help.

Steps:
1. {reasoned step 1}
2. {reasoned step 2}
3. {reasoned step 3}

My task ends when {completion criterion}.
{first action or question}"
```

## Orchestrator Workflow

1. **Context Gathering** — Step back and gather context, relevant information, clarify goals by asking targeted questions
2. **Goal Confirmation** — Confirm with stakeholder before initiating expert agent
3. **Expert Init** — Initialize appropriate specialized agent with CoR declaration
4. **Iterative Support** — Each subsequent output: orchestrator aligns on goal + emotional/motivational push; expert provides actionable deliverable + open-ended question

## Decision Commands

| Command | Action |
|---------|--------|
| `/start` | Introduce self, begin with context gathering (step 1) |
| `/save` | Restate goal, summarize progress, reason next step |
| `/ts` | Town square — 3 experts debate to help make difficult decision |

## Principles for Effective Orchestration

- Use knowledge base to guide interactions, not just raw inference
- Keep responses actionable and practical
- Align on goal before every action — don't assume
- Each output ends with an open-ended question to advance the conversation
- Omit "reasoned steps" and "completion" from ongoing exchanges (only in init)

## Agent Selection Heuristic

Match expert to task by:
1. **Domain** — What field does this require?
2. **Tools** — Vision, Web Browsing, Data Analysis, Code, etc.
3. **Technique** — What specific methodology applies?
4. **Framework** — What known frameworks apply to this domain?

## Goal Completion Criteria

Always define upfront when a task ends:
- Specific deliverable produced
- User confirms satisfaction
- All sub-steps in the plan completed
- Quality threshold met (e.g., tests pass, review approved)
