# Ultimate Agentic Workflow

A skill-first AI engineering workflow for agents that should work hard without making you read a giant manual.

This repository replaces the older starter-kit layout with a compact installable skill:

```text
ultimate-agentic-workflow/
|-- SKILL.md
|-- agents/openai.yaml
|-- scripts/init_agents.py
|-- assets/templates/
`-- references/workflow.md
```

## What This Is

The workflow combines the strongest parts of:

- Superpowers: behavior primitives like brainstorming, TDD, planning, review, worktrees, and verification.
- Cursor Memory Bank: task lifecycle, active context, creative decisions, reflection, and archive.
- Ralph-style loops: autonomous execution for large batches once the spec and plan are stable.
- Dynamic workflow packets: `.workflow/<slug>/` run state, packet ownership, integration, and verification records.

The important design choice: **the full workflow is not meant to live in `AGENTS.md`.**

`AGENTS.md` should be a tiny bootloader. The skill owns the behavior. The long document is a reference that gets loaded only when the task deserves it.

## Install

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ultimate-agentic-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Start a new agent session and invoke it with:

```text
Use $ultimate-agentic-workflow to initialize this repo for accountable AI coding.
```

## Initialize A Repo

The skill includes a deterministic bootstrap script that can create the always-loaded agent files.

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

## Day-To-Day Use

The skill classifies work by tier:

- **T0:** answer or tiny safe edit directly
- **T1:** short approach, execute, verify
- **T2:** spec and plan before implementation
- **T3:** full traceability workflow with `.workflow/`, risk gates, verification ledger, review, reflection, and archive

For serious work, the agent uses Superpowers as the engine and this workflow as the routing/accountability layer.

## Why This Structure

Always-loaded files are expensive. A huge `AGENTS.md` makes every tiny task worse.

This layout keeps the automatic path clean:

```text
AGENTS.md / CLAUDE.md -> tiny bootloader
ultimate-agentic-workflow skill -> operational behavior
references/workflow.md -> detailed manual loaded only when needed
.workflow/ -> run evidence
memory-bank/ -> live task memory when useful
```

The result is an agent that can scale from a typo fix to a multi-agent build without pretending those are the same job.
