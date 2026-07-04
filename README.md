# Awesome AI Workflow

A compact, installable workflow skill for AI coding agents that should move
fast without losing traceability, review discipline, or permission boundaries.

This repository contains the `ultimate-agentic-workflow` skill. It uses a
small bootloader model instead of a large always-loaded instruction file:

```text
AGENTS.md / CLAUDE.md -> short repo instructions (bootloader)
OPS.md -> operational guide: commands, validation, durable lessons
.claude/ -> optional starter kit: subagents, hooks, skills, settings
ultimate-agentic-workflow/SKILL.md -> routing and accountability rules
references/workflow.md -> detailed lifecycle manual
references/orchestration.md -> subagents, fan-out, verification patterns, loops
references/context-engineering.md -> context budgets, durable notes, compaction survival
references/anti-slop.md -> minimalism ladder and slop taxonomy
references/claude-code-kit.md -> the installable .claude/ kit and goal loops
references/meta.md -> minting new skills/subagents/hooks; ecosystem map
references/large-codebase.md -> search routing and permission-gated tooling
references/pilot-measurement.md -> measure tools before trusting them
.workflow/<slug>/ -> durable run evidence for high-risk work
```

The goal is an agent-first workflow: the agent classifies task risk, loads only
the guidance it needs, orchestrates subagents only where fan-out pays for
itself, verifies with fresh-context reviewers, captures lessons so the repo
compounds, and still asks before installing dependencies, editing `.codex` or
`.claude`, or cloning external repositories.

## What It Gives You

- Tiny bootloader templates instead of giant always-loaded instruction files.
- T0-T3 task routing so a typo fix and a multi-session refactor do not use the
  same process.
- A deterministic `init_agents.py` bootstrap for Codex, Claude Code, or both,
  with ecosystem detection (Node/pnpm/yarn/bun, Python, Rust, Go, Maven,
  Gradle, Ruby) — plus `--claude-kit` to install the `.claude/` starter kit.
- **The `.claude/` starter kit**: five focused subagents (code-reviewer,
  skeptic-verifier, test-runner, researcher, implementer), a
  deterministic stop-gate hook that blocks completion while checks fail, an
  optional once-per-session learning gate, `/retro` (session lessons ->
  durable improvements) and `/mint-skill` (new skills/subagents with tuned
  trigger descriptions), and a settings template with safe defaults.
- One canonical state owner per tier, a single traceability matrix schema, and
  a verification ledger that final claims must cite.
- Anti-slop discipline: a minimalism ladder with a safety carve-out, and a
  slop taxonomy for code, tests, prose, and artifacts.
- Multi-agent orchestration guidance: fan-out sizing, structured packet
  results, model tiering, adversarial and fresh-context verification, judge
  panels, and machine-checkable loop stop conditions.
- Context engineering guidance against context rot: just-in-time retrieval,
  durable notes that survive compaction, and subagent context isolation.
- Goal-loop guidance: deterministic stop gates for exact conditions, the
  built-in `/goal` for judgment conditions, autonomous loops for batch work.
- A compounding loop (`references/meta.md`) that tells the agent when to mint
  a new skill, subagent, or hook — with an ecosystem map (Superpowers,
  Ponytail, Headroom, compound engineering, Beads, teach) so it builds on
  proven patterns instead of reinventing them.
- `verify_run.py` as a deterministic gate for T3 run directories.
- Large-codebase readiness checks and permission-gated setup for Serena,
  ripgrep, ast-grep, grepai, Ollama, and WarpGrep/Morph.
- A pilot protocol for measuring whether acceleration tools actually improve
  outcomes before making them default-on.

## Repository Layout

```text
ultimate-agentic-workflow/
|-- SKILL.md
|-- agents/openai.yaml
|-- scripts/
|   |-- init_agents.py
|   |-- large_codebase_tools.py
|   `-- verify_run.py
|-- assets/
|   |-- templates/
|   |   |-- BOOTLOADER.md.template
|   |   `-- OPS.md.template
|   `-- claude/
|       |-- agents/          # code-reviewer, skeptic-verifier, test-runner,
|       |                    # researcher, implementer
|       |-- hooks/           # stop_gate.py, learn_gate.py
|       |-- skills/          # retro/, mint-skill/
|       `-- settings.json.template
`-- references/
    |-- workflow.md
    |-- orchestration.md
    |-- context-engineering.md
    |-- anti-slop.md
    |-- claude-code-kit.md
    |-- meta.md
    |-- large-codebase.md
    `-- pilot-measurement.md

tests/
README.md
```

## Quick Start (any repo, new or existing)

```bash
# 1. See exactly what's present, what's missing, and what to run next (read-only):
python3 ultimate-agentic-workflow/scripts/preflight.py --project-root .

# 2. Bootstrap agent files + the .claude kit (refuses to overwrite anything):
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli claude --claude-kit --project-root .

# Existing CLAUDE.md/AGENTS.md? Print the rendered files and merge by hand instead:
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli claude --claude-kit --stdout --project-root .
```

The preflight also checks that core tools are usable (ripgrep, Serena, ast-grep,
uv) and whether proven frameworks are installed — the Superpowers plugin
(`/plugin install superpowers@claude-plugins-official`) and GSD (original repo
archived; successor `npx @opengsd/gsd-core@latest`) — and prints install
commands for anything missing. It installs nothing itself; every install is
approval-first.

## Install The Skill

For Codex, copy the skill into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ultimate-agentic-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

For Claude Code, copy it into a skills directory (project-local or user-level):

```bash
mkdir -p .claude/skills            # or: mkdir -p ~/.claude/skills
cp -R ultimate-agentic-workflow .claude/skills/
```

Start a new agent session and invoke it, e.g.:

```text
Use ultimate-agentic-workflow to initialize this repo for accountable AI coding.
```

## Initialize A Target Repo

The bootstrap script detects the project's ecosystem and writes short agent
files. Filenames have fixed roles across CLIs, so initializing both on one
repo is safe:

| File | Role |
| --- | --- |
| `AGENTS.md` | Codex bootloader |
| `CLAUDE.md` | Claude Code bootloader |
| `OPS.md` | Shared operational guide |

```bash
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli codex --project-root /path/to/repo
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli claude --project-root /path/to/repo
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli both --project-root /path/to/repo
```

Add `--claude-kit` to also install the `.claude/` starter kit (subagents,
hooks, skills, settings template) into the target repo — see
`references/claude-code-kit.md` for what each piece does and how to enable
the optional learning gate.

The script checks every target path before writing anything; if any target
exists it refuses and writes nothing unless `--force` is passed. An existing
`.claude/settings.json` is never replaced — the template is written alongside
it for manual merge.

## Task Tiers

| Tier | Use when | Expected process |
|---|---|---|
| T0 | Direct answer, tiny safe edit, obvious typo. | Answer or patch directly, then verify if files changed. |
| T1 | Small bounded implementation or doc change. | Durable goal note, execute, verify. |
| T2 | Non-trivial feature, architecture, behavior, or contract work. | Spec and plan before implementation; fresh-context review. |
| T3 | High-risk, broad, multi-agent, multi-session, or audit-heavy work. | `.workflow/<slug>/` with plan, state, packets, risk gates, verification, review, and final report. |

Escalate when work touches security, production data, secrets, migrations,
deployments, broad edits, ambiguous requirements, large unfamiliar codebases,
subagents, loops, or multi-session execution.

## Orchestration And Context

`references/orchestration.md` covers when multi-agent fan-out pays for itself
(discovery, review, verification) and when it hurts (most code authoring), how
to size fan-out, the structured packet contract workers must return, model and
reasoning-effort tiering, adversarial verification patterns, and stop
conditions for autonomous loops.

`references/context-engineering.md` covers context budgets, just-in-time
retrieval, durable notes that survive compaction, and subagent context
isolation.

## Large-Codebase Readiness

For large, unfamiliar, polyglot, or cross-file-heavy repositories, run the
read-only readiness checker before adding search or MCP tooling:

```bash
python3 ultimate-agentic-workflow/scripts/large_codebase_tools.py --project-root . --json
```

It reports repo shape and language signals, installed/missing tool status,
recommendations, and drafts approval-request text when a missing tool appears
useful. It installs nothing, edits no config, and only inspects the repo and
`PATH`. Search routing (`rg` -> symbol -> structural -> semantic) and the tool
catalog live in `references/large-codebase.md`.

## Permission-Gated Setup

Agents may prepare setup commands autonomously, but must ask before executing
anything that mutates `.codex`, `.claude`, `.mcp.json`, home/global MCP config,
package-manager caches, external GitHub checkouts, or files outside the
workspace. Approval requests must include exact commands, write targets,
network/data risks, credentials required, and rollback steps.

Default clone location for dependent repositories is
`.workflow/deps/<owner>-<repo>/` unless the user chooses another location.

## Pilot Measurement

Do not treat Serena, grepai, WarpGrep, or another acceleration tool as
default-on until it has been measured on the target repo class. Use
`references/pilot-measurement.md` to compare a baseline arm against a
treatment arm and recommend default-on only when correctness holds and
exploration cost measurably drops.

## Development

```bash
python3 -m pytest -q                                            # test suite
python3 -m compileall ultimate-agentic-workflow/scripts tests   # syntax check
git diff --check                                                # whitespace
```

## Design Rules

- Keep always-loaded agent files short; operational detail lives in `OPS.md`
  or the skill references.
- One canonical live-state file per tier; everything else is a projection.
- Use `.workflow/<slug>/` only when the task needs durable evidence.
- Fan out subagents for discovery and verification, not for coupled authoring.
- Prefer read-only readiness checks and exact approval text over silent tool
  installs.
- Treat acceleration claims as hypotheses until the pilot protocol measures
  them.

## Current Scope

This repo is intentionally small. It is not a full framework, daemon, or hosted
service. It is a portable skill plus references, scripts, and tests that target
agent behavior in other repositories.
