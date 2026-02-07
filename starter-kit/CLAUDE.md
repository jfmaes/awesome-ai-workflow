# CLAUDE.md

> Project rules for AI-assisted development. Loaded automatically by Claude Code.
> Keep this under 100 lines. Operational learnings go in AGENTS.md.

## Project

- **Name:** [PROJECT_NAME]
- **Description:** [1-2 sentences]
- **Stack:** [language, framework, key dependencies]

## Commands

```bash
# Build
[build command]

# Run
[run command]

# Test (all)
[test command]

# Test (specific)
[targeted test command, e.g., pytest path/to/test.py]

# Lint
[lint command]

# Type check
[typecheck command, if applicable]
```

## Architecture

- **Source code:** `src/` [or wherever]
- **Tests:** `tests/` [or wherever]
- **Shared utilities:** `src/lib/` [or wherever — treat as project stdlib]
- **Config:** [key config files]

## Code Style

- [Key convention 1, e.g., "Functional > OOP unless domain requires it"]
- [Key convention 2, e.g., "Type hints required on all public functions"]
- [Key convention 3, e.g., "No wildcard imports"]
- File naming: [convention]
- Import order: [convention]

## Anti-Patterns (NEVER do these)

- [Thing the AI tends to get wrong in this codebase]
- [Another thing]
- Never leave placeholder/stub implementations — implement completely or don't start

## Git

- Branch naming: [convention, e.g., "feature/description", "ralph/description"]
- Commit messages: [convention, e.g., "conventional commits", "descriptive imperative"]
- Always `git add -A && git commit` after passing tests

## Project-Specific Rules

- [Rule 1]
- [Rule 2]

## Ralph Integration

- Specs: `specs/*.md`
- Plan: `IMPLEMENTATION_PLAN.md`
- Operational guide: `AGENTS.md`
- Loop script: `loop.sh`
- Prompts: `prompts/PROMPT_plan.md`, `prompts/PROMPT_build.md`

## Complexity Tiers

Assess every task before starting. State the tier. User can override.

- **T0 (Just do it):** Single file, clear intent, low risk → execute directly
- **T1 (Think aloud):** 1-3 files, medium scope → state approach, then execute
- **T2 (Spec & plan):** Multi-file, design decisions → draft spec → approval → plan → build
- **T3 (Full spec + plan):** Architecture, multi-session → full spec.md + plan.md + approval gates

Override: "just do it" → T0, "let's plan" → T2+, "Ralph it" → T3 with loop.
