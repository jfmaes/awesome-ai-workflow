# Tier Reference

## Complexity Tier System

The LLM assesses tier at task start and states it. User can always override.

### T0 — Just Do It
- Signals: 1 file, clear intent, low risk, quick fix
- Workflow: Execute directly. No ceremony.
- LLM says: *(nothing — just does it)*

### T1 — Think Aloud
- Signals: 1-3 files, clear scope, some design choices
- Workflow: State approach in 2-3 sentences → execute
- LLM says: "I'll approach this by [X], touching [files]. Starting now."

### T2 — Spec & Plan
- Signals: Multi-file, design tradeoffs, affects others, non-trivial scope
- Workflow: Brief spec → approval → plan → approval → execute in chunks
- LLM says: "This is T2 — let me draft a spec before building."

### T3 — Full Spec + Plan + Loop
- Signals: Architecture, multi-session, high cost of error, many parts
- Workflow: Full spec → plan → approval gate → build (potentially Ralph loop) → reflect
- LLM says: "This is T3. Let me build a proper spec first."

## Detection Signals

| Factor          | → Lower Tier      | → Higher Tier           |
|-----------------|--------------------|-------------------------|
| Files touched   | 1-2                | 5+                      |
| Reversibility   | Easy undo          | Hard to undo            |
| Domain risk     | Script, blog post  | Security tool, prod API |
| Existing system | Greenfield         | Integrated              |
| Ambiguity       | Clear requirements | Vague/conflicting       |
| Duration        | Minutes            | Hours to days           |
| Audience        | Just you           | Students, clients       |
| Dependencies    | None               | External APIs, teams    |

## Override Phrases
- "just do it" / "quick fix" → T0
- "let's plan" / "think about this" → T2+
- "I need a spec" / "this is complex" → T3
- "Ralph it" / "loop it" → T3 with autonomous loop

## When to Ralph (and When Not To)

**Use Ralph:** 10+ well-defined tasks, overnight builds, migration/refactoring, clear spec + low creativity.

**Don't Ralph:** Exploring/prototyping, <5 tasks, high-creativity, budget-constrained, debugging, vague specs.
