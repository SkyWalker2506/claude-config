# Competing Agent Systems — Architecture & Definition Patterns

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

> Last updated: 2026-04-09
> Source: GitHub search, web research, official docs

---

## 1. GitAgent (open-gitagent/gitagent) — 2.6k stars

**What:** Framework-agnostic, git-native standard for defining AI agents. "Clone a repo, get an agent."

**Agent Definition Format:**
- `agent.yaml` — manifest with metadata, model preferences, compliance, skills, tools, segregation of duties
- `SOUL.md` — identity, personality, communication style, values (markdown)
- `RULES.md` — hard constraints and safety boundaries
- `DUTIES.md` — role-based access control

**Knowledge/Memory:**
- `knowledge/` directory for reference documents
- `memory/` directory with `runtime/` subfolder: `dailylog.md`, `key-decisions.md`, `context.md`
- Uses git branches + PRs for human-in-the-loop memory updates

**Comparison to our system:** Very similar philosophy — file-per-agent, markdown-first, knowledge directory. Their `SOUL.md` maps to our `AGENT.md`. They add `RULES.md` and `DUTIES.md` as separate files where we embed rules in AGENT.md.

**Link:** https://github.com/open-gitagent/gitagent

---

## 2. OpenAI Codex — AGENTS.md + Skills

**What:** OpenAI's coding agent with hierarchical instruction files.

**Agent Definition Format:**
- `AGENTS.md` — markdown file, hierarchical discovery (global `~/.codex/AGENTS.md` → project root → subdirectories)
- `AGENTS.override.md` — replaces standard at any level
- Skills: `SKILL.md` in `.agents/skills/` directories
- 32 KiB default limit per file

**Knowledge/Memory:**
- Two-phase persistent memory pipeline (internal, not file-exposed)
- No per-agent knowledge directories exposed to users
- Instructions concatenate root-down; closer files override earlier ones

**Comparison to our system:** Codex uses a single flat `AGENTS.md` per scope, not per-agent files. No persona concept — just instructions. Our system is more structured with dedicated agent definitions, knowledge directories, and memory per agent.

**Link:** https://developers.openai.com/codex/guides/agents-md

---

## 3. Anthropic Skills (anthropics/skills) — 113k stars

**What:** Official skill format for Claude Code and compatible agents.

**Skill Definition Format:**
```
skill-folder/
└── SKILL.md (YAML frontmatter + markdown body)
```
Frontmatter: `name`, `description`
Body: instructions, examples, guidelines

**Knowledge/Memory:**
- Skills can include resources and reference files
- No built-in per-skill memory — relies on Claude's native memory system

**Comparison to our system:** We build ON TOP of this format — our agents use SKILL.md-compatible skills but add AGENT.md for persona, knowledge/ for domain expertise, and memory/ for persistent learnings. The official format is skill-only, not agent-level.

**Link:** https://github.com/anthropics/skills

---

## 4. Superpowers (obra/superpowers) — 142k stars

**What:** Agentic skills framework — composable workflows that trigger based on development context.

**Definition Format:**
- Skills as triggered workflows (brainstorming, planning, development, review, debugging)
- No explicit persona files — capabilities organized by function
- Platform adapters: `.claude-plugin`, `.codex`, `.opencode` directories

**Knowledge/Memory:**
- Knowledge distributed across skill definitions and platform-specific docs
- No per-agent knowledge directory
- Emphasizes verification over assertions

**Comparison to our system:** Superpowers focuses on workflow automation, not agent identity. No persona, no per-agent memory. Our system adds the identity/knowledge layer that Superpowers lacks.

**Link:** https://github.com/obra/superpowers

---

## 5. CrewAI — YAML Agent Definitions

**What:** Multi-agent orchestration framework with YAML-driven agent configuration.

**Agent Definition Format (YAML):**
```yaml
agent_name:
  role: "Senior Data Analyst"
  goal: "Analyze data and provide insights"
  backstory: "You are an experienced analyst..."
```
25+ parameters including: tools, allow_delegation, max_iterations, knowledge_sources, memory, reasoning, multimodal.

**Knowledge/Memory:**
- `knowledge/` directory for PDFs and reference material
- `knowledge_sources` parameter per agent
- `memory=True` enables interaction history persistence
- Short-term, long-term, and entity memory types

**Comparison to our system:** CrewAI's role/goal/backstory maps roughly to our AGENT.md persona section. They use YAML; we use markdown. Their knowledge_sources are similar to our knowledge/ directory. Key difference: CrewAI agents are code-instantiated; ours are file-system-native.

**Link:** https://docs.crewai.com/en/concepts/agents

---

## 6. Cursor — .cursor/rules/ MDC Files

**What:** AI IDE with scoped instruction rules.

**Definition Format:**
- `.cursor/rules/*.mdc` — Markdown with YAML frontmatter
- Frontmatter: `description`, `alwaysApply` (boolean), `globs` (file patterns)
- Body: markdown instructions
- Supports persona-style instructions ("You are instructa, a senior Rails developer")

**Knowledge/Memory:**
- No per-agent knowledge directory
- No persistent memory across sessions (relies on conversation context)
- Rules scoped by file glob patterns

**Comparison to our system:** Cursor rules are per-project, not per-agent. No knowledge directory, no memory persistence. Our system is fundamentally more structured for multi-agent scenarios.

**Link:** https://cursor.com/docs/context/rules

---

## 7. Windsurf (Cascade) — Memories + Codemaps

**What:** AI IDE with deep codebase integration.

**Definition Format:**
- `.windsurfrules` file for project instructions
- No formal agent definition spec
- 5 parallel agents support (Feb 2026)

**Knowledge/Memory:**
- Codemaps: structured representations of large codebases
- Memories: persist context across conversations
- No per-agent knowledge files

**Comparison to our system:** Windsurf focuses on IDE-level intelligence, not agent definitions. Their Memories feature is similar to our memory/ directory but less structured.

---

## 8. Devin — Knowledge Graph + Playbooks

**What:** Cloud-based autonomous software engineer.

**Definition Format:**
- No public agent definition spec
- `.rules` and `.md` files for permanent agent ingestion
- Playbooks: step-by-step instructions for specific workflows

**Knowledge/Memory:**
- Knowledge Graph built from codebase indexing
- Learns patterns, conventions, and "tribal knowledge" over time
- Enterprise: upload documentation to create custom knowledge base
- Dynamic re-planning on failures

**Comparison to our system:** Devin's knowledge graph is more automated (indexes codebase). Our system is more explicit (curated knowledge files). Devin is proprietary; our approach is open and portable.

---

## 9. LangGraph — StateGraph + Memory Stores

**What:** Agent orchestration framework using graph-based state management.

**Agent Definition Format:**
- Agents defined as Python code (StateGraph with typed state, nodes, edges)
- No declarative file-based agent definition
- State schema via TypedDict or Pydantic

**Knowledge/Memory:**
- Short-term: thread-scoped checkpoints
- Long-term: custom namespaces, cross-session
- Knowledge graph integration (Neo4j)
- Episodic memory: past interactions and successes/failures

**Comparison to our system:** LangGraph is code-first, not file-first. Its memory system is more sophisticated (typed, versioned, graph-backed) but requires code to configure. Our file-based approach is more accessible and portable.

**Link:** https://www.langchain.com/langgraph

---

## 10. MATE (antiv/mate) — Database-Driven Agents — 42 stars

**What:** Production multi-agent orchestration engine on Google ADK.

**Agent Definition Format (Database):**
- Agents stored in PostgreSQL/MySQL/SQLite table `agents_config`
- Fields: name, type (llm/sequential/parallel/loop), model_name, instruction, parent_agents, tool_config (JSON), allowed_for_roles, project_id
- Agent types: llm, sequential, parallel, loop
- Agents can create/update/delete other agents at runtime

**Knowledge/Memory:**
- Memory blocks: reusable context stored in database
- Token usage tracking per interaction
- Conversation history persistence
- Web dashboard for visual management

**Comparison to our system:** Fully database-driven vs our file-system approach. MATE is more enterprise-oriented (RBAC, multi-tenant) but less portable. Our approach is git-native and works offline.

**Link:** https://github.com/antiv/mate

---

## 11. AgentSkills Specification (agentskills/agentskills) — 15.5k stars

**What:** Open format for portable agent capabilities, maintained by Anthropic ecosystem.

**Skill Format:**
- Folders with SKILL.md + optional scripts/resources
- YAML frontmatter + markdown body
- Cross-platform compatibility goal

**Comparison to our system:** This IS the foundation our system uses. We extend it with AGENT.md (persona layer) and knowledge/memory directories per agent.

**Link:** https://github.com/agentskills/agentskills

---

## Summary: How Our System Compares

| Feature | Our System | GitAgent | Codex | CrewAI | Cursor | Devin | LangGraph |
|---------|-----------|----------|-------|--------|--------|-------|-----------|
| Per-agent definition file | AGENT.md | SOUL.md + agent.yaml | AGENTS.md (shared) | YAML | .mdc rules | .rules | Code only |
| Persona/identity | Yes | Yes (SOUL.md) | No | role/goal/backstory | Optional | No | No |
| Knowledge directory | knowledge/ | knowledge/ | No | knowledge/ | No | Knowledge Graph | Code-configured |
| Memory per agent | memory/ | memory/ | Internal | memory=True | No | Internal | Checkpoints |
| File format | Markdown | Markdown + YAML | Markdown | YAML | MDC | Proprietary | Python |
| Git-native | Yes | Yes | Partial | No | Yes | No | No |
| Multi-agent | Yes (registry) | Single repo | Single | Crew orchestration | No | No | Graph-based |

### Key Insight

Our system (Knowledge-First with AGENT.md + knowledge/ + memory/) is most similar to **GitAgent** in philosophy. The main differentiators:

1. **We are unique** in combining agent personas + knowledge directories + persistent memory in a multi-agent registry — no other system does all three in a file-based, git-native way
2. **GitAgent** is the closest competitor but focuses on single-agent-per-repo, not multi-agent orchestration
3. **CrewAI** has the richest agent definition fields but requires Python code, not pure files
4. **Codex/Cursor** focus on instruction injection, not agent identity
5. **Devin** has the most advanced knowledge system but is proprietary and non-portable
