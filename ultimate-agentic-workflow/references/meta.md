# Extending the System

How to grow a repo's agentic capability deliberately: when to mint a new skill, subagent, or hook; how to keep the always-loaded surface small while capability compounds; and which ecosystem frameworks are worth knowing.

## Contents

- The Compounding Loop
- When to Mint What
- Authoring Quality Bar
- Architect Coverage Map
- Ecosystem Map

## The Compounding Loop

A repo gets better at agentic work the same way a team does: by converting experience into structure. The loop:

1. **Notice** friction, repetition, or a correction (during work, or via `/retro` / the learning gate).
2. **Classify** it: fact, workflow, role, or rule.
3. **Crystallize** it into the right primitive (table below) via `/mint-skill`.
4. **Measure**: does the new primitive actually fire when it should, and does it earn its context cost? Prune what does not.

Run this loop honestly and the kit becomes specific to the repo; skip it and every session re-learns the same lessons.

## When to Mint What

| Signal | Primitive | Why |
| --- | --- | --- |
| A durable fact or command ("tests need `-p 3.13`") | One line in `OPS.md` | Cheapest possible storage; always loaded, so keep it terse |
| A multi-step workflow performed 2+ times | Skill | Loads on demand; survives across sessions; invocable |
| A recurring role with verbose output or restricted tools (review, research, running checks) | Subagent | Fresh context, tool limits, output distillation |
| A rule that must hold every time, not be remembered | Hook (or `stop-gate.json` check) | Enforcement beats memory; agents forget, gates do not |
| Integration with an external system | MCP server | Do not fake tools with prompts |
| A one-off trick | Nothing | Minting one-offs is how kits bloat into slop |

Two mistakes to avoid: minting too early (a workflow done once is not a pattern) and hoarding in `CLAUDE.md` (always-loaded lines tax every future session; anything procedural belongs in an on-demand skill).

## Authoring Quality Bar

Full checklist in the `/mint-skill` skill; the invariants:

- Body small, references one level deep, `## Contents` in anything over 100 lines.
- The `description` is the trigger mechanism: third person, what + when, concrete vocabulary a user would actually use — and tested against should-fire / should-not-fire prompts, not guessed.
- One default path plus an escape hatch; no option menus.
- Side-effecting skills are manual-invocation only.
- Subagents get minimum tools; reviewers and verifiers get no Edit/Write (Bash stays, restricted by instruction to non-mutating commands).
- Try it on one real task before calling it shipped.

## Architect Coverage Map

Architect-level Claude Code competence (as reflected in Anthropic's partner certification domains) breaks into five areas. Where this system covers each:

| Domain | Covered by |
| --- | --- |
| Agentic architecture & orchestration | `orchestration.md`, the subagent kit, `workflow.md` execution modes |
| Claude Code configuration & workflows | `claude-code-kit.md` (agents, hooks, skills, settings), `init_agents.py` |
| Prompt engineering & structured output | packet contract in `orchestration.md`, skill-authoring bar here |
| Tool design & MCP integration | `large-codebase.md` (permission-gated MCP setup), "when to mint what" above |
| Context management & reliability | `context-engineering.md`, deterministic gates, verification ledger in `workflow.md` |

Use the map as a self-audit: if a repo's agentic setup is weak in one domain, that row says which reference to apply.

## Ecosystem Map

Frameworks worth knowing, each with the one idea this system adopted or recommends. Check these (and the awesome-claude-code/awesome-claude-skills catalogs) before building something new — duplicating a battle-tested tool is slop.

| Framework | What it is | The idea worth taking |
| --- | --- | --- |
| Superpowers (obra) | SDLC-as-skills: brainstorm → plan → subagent-driven dev → TDD → review → verify | Fresh implementer subagent sees only plan + tests; a second independent subagent reviews — adopted in our agent kit |
| Ponytail | Minimalism/YAGNI ruleset plugin | The 7-rung decision ladder + safety carve-out — adopted in `anti-slop.md`; deferred shortcuts become tracked debt |
| Headroom | Context-compression proxy (reversible, content-aware) | Compress-but-keep-retrievable: park full outputs in files, keep summaries in context — echoed in `context-engineering.md` |
| Compound engineering (Every) | Plan-heavy loop ending in a `/compound` learning step | A dedicated learning-capture step every session — adopted as `/retro` + the learning gate |
| teach / reflect / upskill (alexknowshtml) | Session-sourced Socratic quizzing and retrospectives | Session transcripts are a lesson mine; capture before the session ends — adopted in the learning gate concept |
| Beads (`bd`) | Dependency-graph issue tracker built for agents | `bd ready`-style "what is unblocked now" beats flat TODO lists for multi-session/multi-agent work — consider it when `.workflow/state.json` packets outgrow themselves |
| GSD (original archived June 2026; successor open-gsd/gsd-core, npm `@opengsd/gsd-core`) | Spec-driven system with research/plan/execute/verify agent roles | The named four-role split — mirrored by our researcher/implementer/test-runner/skeptic-verifier agents |
| skill-creator (Anthropic) | Meta-skill for authoring skills | Treat the trigger description as something you test and tune, not write once — adopted in `/mint-skill` |

Ecosystem facts drift; verify a framework's current state against its repo before adopting it, per `pilot-measurement.md`.
