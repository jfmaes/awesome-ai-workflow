---
name: ultimate-agentic-workflow
description: Use when initializing a repo for AI coding, creating AGENTS.md/CLAUDE.md bootloaders, choosing T0-T3 workflow depth, or running accountable multi-step agent work with traceability, verification, review, reflection, or .workflow artifacts.
---

# Ultimate Agentic Workflow

## Overview

Use this skill as the routing and accountability layer for AI coding. Keep always-loaded repo instructions tiny; load detailed workflow guidance only when tier and risk justify it.

## Initialize Agent Files

When the user asks to initialize, bootstrap, install, set up `AGENTS.md`, or make the workflow automatic, run:

```bash
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli codex --project-root .
```

For Claude Code projects, use `--cli claude`.

The script:

- detects common source/test directories and package commands
- writes the correct always-loaded bootloader file
- writes the matching operational guide
- refuses to overwrite unless `--force` is provided

File naming:

| CLI | Bootloader | Operational guide |
| --- | --- | --- |
| Codex | `AGENTS.md` | `OPS.md` |
| Claude Code | `CLAUDE.md` | `AGENTS.md` |

## Tier Decision

Classify before acting:

- **T0:** answer or tiny safe edit directly
- **T1:** state short approach, execute, verify
- **T2:** write spec/plan before implementation
- **T3:** create full traceability workflow with `.workflow/`, risk gates, verification ledger, review, reflection, and archive

Escalate for security, production data, secrets, migrations, deployments, broad edits, ambiguous requirements, large or unfamiliar codebases, subagents, loops, or multi-session work.

## Execution Rules

- Use Superpowers skills for behavior primitives when available: brainstorming, TDD, worktrees, writing plans, review, and verification.
- Do not put the full workflow in `AGENTS.md` or `CLAUDE.md`; those files are bootloaders.
- Preserve the original user goal in T2/T3 artifacts.
- Do not claim completion without fresh verification evidence.
- For multi-agent work, assign packet ownership and integrate results explicitly.
- For T3, create `.workflow/<slug>/` with plan, state, orchestration, packets, results, and final report.

## When More Detail Is Needed

Read `references/workflow.md` for:

- full lifecycle
- traceability matrix
- claim ledger
- verification ledger
- risk register
- review records
- reflection/archive templates
- Ralph loop policy

Read `references/large-codebase.md` for large or unfamiliar codebases, optional MCP/search tooling, and permission-gated `.codex` / `.claude` / GitHub dependency setup.
Use `scripts/large_codebase_tools.py --project-root . --json` as the read-only readiness check before asking to install Serena or related large-codebase tools.

Read `references/pilot-measurement.md` before treating any acceleration tool as default-on or citing efficiency gains.
