---
last_updated: 2026-04-09
refined_by: opus
confidence: medium
---

# Memory Architecture

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

## Memory Types

| Type | Scope | Persistence | Example |
|------|-------|-------------|---------|
| **Session** | Single conversation | Ephemeral | Conversation history, tool results |
| **Project** | Per-project, cross-session | File-based | CLAUDE.md, MEMORY.md, learnings |
| **Global** | All projects | File-based | ~/.claude/CLAUDE.md, global settings |
| **Semantic** | Searchable knowledge | Vector DB | MemPalace, embeddings |

## Session Memory

- Lives in conversation context window
- Grows with each turn — eventually hits token limit
- **Compaction**: Summarize older turns, keep recent detail
- **Sub-agents**: Each gets own context — no shared session memory
- **Worktrees**: Separate git worktrees for parallel agent isolation

## Persistent Memory (File-Based)

### MEMORY.md Pattern (Claude Code native)
```markdown
# Memory Index
- [Topic](file.md) — one-line description
```
- Auto-managed by Claude Code in `~/.claude/projects/`
- Per-project memory persists across conversations
- Good for: preferences, decisions, recurring patterns

### Learnings Pattern
```markdown
# Learnings
- [Finding](finding.md) — date, confidence, source
```
- Agent-specific accumulated knowledge
- Refined over time — stale entries pruned via `/memory-prune`

## MemPalace Architecture

MemPalace uses a spatial metaphor for memory organization:

- **Palace**: Root container (~/.mempalace/palace/)
- **Wings**: Topic categories (emotions, technical, creative, etc.)
- **Halls**: Sub-categories within wings, matched by keywords
- **Drawers**: Individual memory items stored as vector embeddings

### Configuration
```json
{
  "palace_path": "~/.mempalace/palace",
  "collection_name": "mempalace_drawers",
  "topic_wings": ["emotions", "technical", "creative", ...]
}
```

### How It Works
1. Input text is classified into a wing via keyword matching
2. Embedded into vector space (ChromaDB)
3. Retrieved via semantic similarity search
4. Spatial metaphor aids human understanding of where memories live

### When to Use MemPalace vs File Memory
- **MemPalace**: Fuzzy recall, semantic search, large volumes, conversational AI
- **File memory**: Structured rules, explicit lookups, agent configuration

## State Management Patterns

### Stateless (Swarm/Agents SDK model)
- Each call starts fresh
- State passed explicitly in messages
- Simple, predictable, no hidden bugs

### Checkpointed (LangGraph model)
- State serialized at each node
- Resume from any checkpoint
- Required for long-running workflows

### Artifact-Based (Claude Code model)
- State lives in files (code, specs, task lists)
- Agents read/write shared filesystem
- Natural for development workflows

## Design Recommendations

1. **Default to file-based memory** — simple, debuggable, version-controlled
2. **Add vector search** only when keyword matching fails
3. **Keep session context lean** — offload to persistent files early
4. **Prune regularly** — stale memory is worse than no memory
5. **Never store secrets in memory** — use secrets.env separately
