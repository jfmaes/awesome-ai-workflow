# Awesome AI Workflow

A compact, installable workflow skill for AI coding agents that should move
fast without losing traceability, review discipline, or permission boundaries.

This repository contains the `ultimate-agentic-workflow` skill. It replaces a
large always-loaded starter kit with a small bootloader model:

```text
AGENTS.md or CLAUDE.md -> short repo instructions
ultimate-agentic-workflow/SKILL.md -> routing and accountability rules
references/workflow.md -> detailed lifecycle manual
references/large-codebase.md -> optional large-repo acceleration policy
memory-bank/ -> compact working memory when a target repo uses it
.workflow/<slug>/ -> durable run evidence for high-risk work
```

The goal is an agent-first workflow: the agent can classify task risk, load only
the guidance it needs, use stronger tools when justified, and still ask before
installing dependencies, editing `.codex` or `.claude`, or cloning external
repositories.

## What It Gives You

- Tiny Codex and Claude bootloader templates instead of giant always-loaded
  instruction files.
- T0-T3 task routing so a typo fix and a multi-session refactor do not use the
  same process.
- A deterministic `init_agents.py` bootstrap script for adding `AGENTS.md`,
  `CLAUDE.md`, and `OPS.md` to a target repo.
- Traceability patterns for plans, source ledgers, risk registers,
  verification ledgers, review records, reflection, and archive notes.
- Large-codebase readiness checks that detect when Serena-like symbol tooling
  may help, while staying read-only by default.
- Permission-gated setup guidance for Serena, ripgrep, ast-grep, grepai,
  Ollama, WarpGrep/Morph, Codex MCP, Claude MCP, and dependent GitHub clones.
- A pilot protocol for measuring whether acceleration tools actually improve
  outcomes before making them default-on.

## Repository Layout

```text
ultimate-agentic-workflow/
|-- SKILL.md
|-- agents/openai.yaml
|-- scripts/
|   |-- init_agents.py
|   `-- large_codebase_tools.py
|-- assets/templates/
|   |-- AGENTS.md.codex.template
|   |-- CLAUDE.md.template
|   `-- OPS.md.template
`-- references/
    |-- workflow.md
    |-- large-codebase.md
    `-- pilot-measurement.md

tests/
|-- test_large_codebase_tools.py
`-- test_workflow_enhancements.py

CLAUDE_EXEC_REPORT.md
README.md
```

## Install The Skill

Copy the skill into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ultimate-agentic-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Start a new agent session and invoke it with:

```text
Use $ultimate-agentic-workflow to initialize this repo for accountable AI coding.
```

## Initialize A Target Repo

The skill includes a deterministic bootstrap script. It detects common
source/test directories and package commands, then writes short agent files.

For Codex:

```bash
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli codex --project-root /path/to/repo
```

This creates:

- `AGENTS.md`: short Codex bootloader and project instructions
- `OPS.md`: operational notes and validation commands

For Claude Code:

```bash
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli claude --project-root /path/to/repo
```

This creates:

- `CLAUDE.md`: short Claude bootloader and project instructions
- `AGENTS.md`: operational notes and validation commands

The script refuses to overwrite existing files unless `--force` is passed.

## Task Tiers

The workflow classifies work before acting:

| Tier | Use when | Expected process |
|---|---|---|
| T0 | Direct answer, tiny safe edit, obvious typo. | Answer or patch directly, then verify if files changed. |
| T1 | Small bounded implementation or doc change. | State short approach, execute, verify. |
| T2 | Non-trivial feature, architecture, behavior, or contract work. | Write or update a spec/plan before implementation. |
| T3 | High-risk, broad, multi-agent, multi-session, or audit-heavy work. | Create `.workflow/<slug>/` with plan, state, packets, risk gates, verification, review, and final report. |

Escalate when work touches security, production data, secrets, migrations,
deployments, broad edits, ambiguous requirements, large unfamiliar codebases,
subagents, loops, or multi-session execution.

## Large-Codebase Readiness

For large, unfamiliar, polyglot, or cross-file-heavy repositories, run the
read-only readiness checker before adding search or MCP tooling:

```bash
python3 ultimate-agentic-workflow/scripts/large_codebase_tools.py --project-root . --json
```

The script reports:

- total file count and source-file count;
- detected languages and monorepo signals;
- whether Serena-like symbol navigation appears useful;
- installed or missing tool status for `uv`, `rg`, Serena, ast-grep, grepai,
  Ollama, and WarpGrep/Morph;
- recommendations for when to use each tool;
- approval-request text with exact install/config commands when Serena is useful
  but missing.

It does not install dependencies, edit `.codex`, edit `.claude`, mutate MCP
config, run package managers, or clone repositories. It only inspects the repo
shape and `PATH`.

Human-readable mode is also available:

```bash
python3 ultimate-agentic-workflow/scripts/large_codebase_tools.py --project-root .
```

## Search Routing

Use the cheapest reliable retrieval mode first:

| Need | First tool |
|---|---|
| Known text, route, config key, error, filename, or symbol string. | `rg` |
| Definitions, callers, references, implementations, rename impact. | Serena or another LSP/code-intelligence tool |
| Syntax-shaped patterns or safe structural rewrites. | ast-grep, tree-sitter, or a language parser |
| Unknown vocabulary or fuzzy concept search after exact/symbol/structural search fails. | grepai or another semantic search tool |
| Hosted fuzzy search for approved data paths. | WarpGrep/Morph MCP |

Search tools narrow the candidate set. They do not replace source reads,
integration judgment, tests, or review.

## Permission-Gated Setup

Agents may prepare setup commands autonomously, but must ask before executing
anything that mutates:

- `.codex`, `.claude`, `.mcp.json`, or home/global MCP config;
- package-manager caches or global tool installs;
- external GitHub checkouts;
- files outside the workspace.

Approval requests must include:

- exact commands;
- exact write targets;
- network/data risks, including whether code leaves the machine;
- credentials or API keys required;
- rollback steps.

Default clone location for dependent repositories is
`.workflow/deps/<owner>-<repo>/` unless the user chooses another location.

## Pilot Measurement

Do not treat Serena, grepai, WarpGrep, or another acceleration tool as
default-on until it has been measured on the target repo class.

Use `ultimate-agentic-workflow/references/pilot-measurement.md` to compare a
baseline arm against a treatment arm with the candidate tool. Track correctness,
wall-clock time, tool calls, files read, lines read, tokens when available, diff
size, setup overhead, failed commands, and review findings.

Recommend a tool as default-on only when it matches or improves correctness,
reduces exploration cost, does not add unresolved review findings, and has a
clear permission and data-handling story.

## Handoff To Another Agent

Use `CLAUDE_EXEC_REPORT.md` as an example of a downstream-agent handoff. It
front-loads what the repo already covers, points to exact local files, names the
open research questions, and avoids making the next agent rediscover the repo
from scratch.

That report also records post-research corrections: Ponytail, Serena, semantic
search, hosted WarpGrep/Morph, and efficiency claims should be validated against
current primary sources before being treated as fact.

## Development

Run the focused test suite:

```bash
python3 -m pytest -q
```

Run syntax compilation for scripts and tests:

```bash
python3 -m compileall ultimate-agentic-workflow/scripts tests
```

Check whitespace before committing:

```bash
git diff --check
```

## Design Rules

- Keep always-loaded agent files short.
- Put operational detail in `OPS.md` or the skill references, not in every
  generated bootloader.
- Use `.workflow/<slug>/` only when the task needs durable evidence.
- Use `memory-bank/` for compact current context when a target repo has adopted
  that pattern.
- Prefer read-only readiness and exact approval text over silent tool installs.
- Treat acceleration claims as hypotheses until the pilot protocol measures
  them.

## Core Files

- `ultimate-agentic-workflow/SKILL.md`: skill entrypoint and routing rules.
- `ultimate-agentic-workflow/references/workflow.md`: detailed T0-T3 lifecycle,
  traceability, review, and archive process.
- `ultimate-agentic-workflow/references/large-codebase.md`: search routing,
  tool catalog, Serena setup, semantic-search guidance, and permission-gated
  setup rules.
- `ultimate-agentic-workflow/references/pilot-measurement.md`: A/B protocol for
  proving tool value before defaulting to it.
- `ultimate-agentic-workflow/scripts/init_agents.py`: bootloader initializer for
  Codex and Claude repos.
- `ultimate-agentic-workflow/scripts/large_codebase_tools.py`: read-only
  large-codebase readiness checker.
- `ultimate-agentic-workflow/assets/templates/`: generated bootloader and
  operations guide templates.

## Current Scope

This repo is intentionally small. It is not a full framework, daemon, or hosted
service. It is a portable skill plus references, scripts, and tests that target
agent behavior in other repositories.
