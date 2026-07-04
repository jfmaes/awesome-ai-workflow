---
name: ultimate-agentic-workflow
description: Routes AI coding work by risk tier (T0-T3) and enforces traceability, verification, and anti-slop discipline. Use when initializing or scaffolding a repo for AI coding (preflight readiness check, AGENTS.md/CLAUDE.md bootloaders, .claude starter kit with subagents/hooks/skills), migrating or upgrading a repo from a previous version of this workflow, checking or installing agent tooling and frameworks (ripgrep, Serena, Superpowers, GSD), classifying task ceremony, orchestrating subagents or parallel work, running goal loops or autonomous loops, managing context rot/compaction on long tasks, capturing session lessons, creating new skills or subagents, or producing accountable multi-step work with .workflow artifacts, verification ledgers, and fresh-context review.
---

# Ultimate Agentic Workflow

## Overview

Use this skill as the routing and accountability layer for AI coding. Keep always-loaded repo instructions tiny; load detailed workflow guidance only when tier and risk justify it.

In every command below, `<skill-dir>` is the directory containing this SKILL.md — `ultimate-agentic-workflow/` in a repo clone, or the installed skill/plugin directory otherwise.

Harness support: the references are harness-agnostic; `AGENTS.md` + `OPS.md` bootstrap works for any AGENTS.md-convention harness (Codex, OpenCode, Cursor, Gemini CLI, ...); `CLAUDE.md` and the `.claude/` kit are the Claude Code layer. See the Harness Support section of the README.

## Preflight

For any repo — new or existing — start with the read-only readiness check:

```bash
python3 <skill-dir>/scripts/preflight.py --project-root .
```

It reports repo and bootloader state, `.claude` kit presence, tool availability (ripgrep, Serena, ast-grep, ...), and whether proven frameworks are installed (the Superpowers plugin; GSD, whose original repo is archived — successor open-gsd/gsd-core, npm `@opengsd/gsd-core`), then prints an ordered next-steps list with exact commands. It also detects repos initialized by v1 of this skill and prints the exact migration steps (`git mv AGENTS.md OPS.md`, then init with `--skip-existing`) — when asked to migrate or upgrade the workflow, run preflight and follow its output. It executes nothing beyond read-only listings; every install stays approval-first. Prefer installing Superpowers over reimplementing its behavior skills — this kit's hooks, gates, and verifier agents complement it, they do not replace it.

## Initialize Agent Files

One guided command does preflight + bootstrap (asks before writing; `--yes` to skip the prompt):

```bash
python3 <skill-dir>/scripts/setup.py --project-root .
```

Or run the pieces directly when the user asks to initialize, bootstrap, or set up `AGENTS.md`/`CLAUDE.md`:

```bash
python3 <skill-dir>/scripts/init_agents.py --cli codex --project-root .
```

`--cli codex` writes the universal `AGENTS.md` read by Codex, OpenCode, Cursor, Gemini CLI, and other AGENTS.md-convention harnesses. Use `--cli claude` for Claude Code, or `--cli both` (default in setup.py) to serve everything. Add `--claude-kit` to also install the `.claude/` starter kit: subagents (code-reviewer, skeptic-verifier, test-runner, researcher, implementer), Stop hooks (deterministic stop gate, optional learning gate), skills (`/retro`, `/mint-skill`), and a settings template — see `references/claude-code-kit.md`.

The script detects the project's ecosystem (Node/pnpm/yarn/bun, Python, Rust, Go, Maven, Gradle, Ruby) and commands, then writes:

- `AGENTS.md` (Codex bootloader) and/or `CLAUDE.md` (Claude Code bootloader)
- `OPS.md` (shared operational guide)

It checks every target path first and refuses to overwrite unless `--force` is given — a failed run writes nothing. For existing repos with their own `CLAUDE.md`/`AGENTS.md`, use `--stdout` to print the rendered files and merge manually instead of overwriting.

## Tier Decision

Classify before acting:

- **T0:** answer or tiny safe edit directly
- **T1:** write a one-line durable goal note, execute, verify
- **T2:** write spec/plan before implementation
- **T3:** create full traceability workflow with `.workflow/`, risk gates, verification ledger, review, reflection, and archive

Escalate for security, production data, secrets, migrations, deployments, broad edits, ambiguous requirements, large or unfamiliar codebases, subagents, loops, or multi-session work.

## Execution Rules

- Do not put the full workflow in `AGENTS.md` or `CLAUDE.md`; those files are bootloaders.
- Preserve the original user goal verbatim in the tier's canonical state file (T1+); state must survive context compaction.
- Do not claim completion without fresh verification evidence.
- For T2+ work, review comes from a fresh context, not the author; self-review must be labeled as such.
- Multi-agent fan-out is for discovery, review, and verification by default; authoring stays single-agent with worktree isolation unless tasks have disjoint write scopes.
- Route mechanical subagent work to cheaper models; keep orchestration, design, integration, and verification on the strongest model.
- Apply the anti-slop gates to everything produced: walk the minimalism ladder before writing code, never weaken a safety guard for brevity, and record deliberate shortcuts as tracked debt.
- Validate T3 run directories before execution: `python3 <skill-dir>/scripts/verify_run.py --run-dir .workflow/<slug>`.
- When friction or a workflow repeats, propose crystallizing it: an `OPS.md` line, a skill, a subagent, or a hook — per `references/meta.md` and the `/mint-skill` skill.
- Use Superpowers skills for behavior primitives when available: brainstorming, TDD, worktrees, writing plans, review, and verification.

## When More Detail Is Needed

All references are one level deep from this file; load only what the current phase needs:

- `references/workflow.md`: full T0-T3 lifecycle, state ownership, traceability matrix, verification ledger, review, reflection, archive, deterministic gates, loop policy.
- `references/orchestration.md`: subagent economics and fan-out sizing, packet contract with structured results, worker rules, model tiering, adversarial/fresh-context verification, judge panels, loop stop conditions.
- `references/context-engineering.md`: context budgets, just-in-time retrieval, durable notes, compaction survival, subagent context isolation.
- `references/anti-slop.md`: the minimalism ladder, safety carve-out, and slop taxonomy for code, tests, prose, and artifacts.
- `references/claude-code-kit.md`: the installable `.claude/` kit — subagents, stop gate and learning gate hooks, `/retro` and `/mint-skill` skills, settings template, goal loops.
- `references/meta.md`: the compounding loop — when to mint a skill vs subagent vs hook vs MCP, authoring quality bar, architect coverage map, ecosystem map (Superpowers, Ponytail, Headroom, compound engineering, Beads, teach).
- `references/large-codebase.md`: search routing (`rg` -> symbol -> structural -> semantic), tool readiness, permission-gated `.codex`/`.claude`/MCP setup. Run `python3 <skill-dir>/scripts/large_codebase_tools.py --project-root . --json` as the read-only readiness check before asking to install anything.
- `references/pilot-measurement.md`: measure any acceleration tool before treating it as default-on or citing efficiency gains.
