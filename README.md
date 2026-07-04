# Awesome AI Workflow

**Next-gen agentic development scaffolding — one command, any repo, any harness.** A portable skill + starter kit that gives any repo — new or existing, Claude Code or Codex or any AGENTS.md harness — a production-grade agentic workflow: risk-tiered ceremony, enforced verification, anti-slop gates, multi-agent orchestration patterns, context-rot defenses, and a compounding loop that makes the setup smarter every session.

```bash
python3 ultimate-agentic-workflow/scripts/setup.py --project-root .
```

That's it. It audits your repo read-only, shows exactly what it will create, asks once, and writes. Nothing is ever overwritten. (Command shown for a repo clone; installed as a plugin or skill, replace `ultimate-agentic-workflow/` with your install's skill directory — every script works from any location.)

## v2: The Next-Generation Rework

This is a ground-up rework of the original skill — not a polish pass. v1 was a workflow *document*: good advice an agent could follow or silently skip. v2 is a workflow *system*: the advice became mechanisms, the mechanisms became enforceable, and the whole thing was rebuilt from primary sources and battle-tested by adversarial multi-agent review before shipping.

What makes v2 better:

| | v1 | v2 |
| --- | --- | --- |
| **Enforcement** | Prose asking agents to verify before claiming done | A Stop-hook gate that makes stopping *impossible* while your checks fail — and a preflight that verifies the gate is actually wired, not just installed |
| **Entrypoint** | Copy files, read a 1,100-line manual | One guided command (`setup.py`), or `/plugin install` in Claude Code; brownfield-safe with `--stdout` merge and `--skip-existing` |
| **Traceability** | Four overlapping ledgers that could drift apart | One traceability matrix + one verification ledger, with an explicit canonical state file per tier and a `verify_run.py` gate |
| **Subagents** | None | Five tool-restricted roles — reviewers and verifiers that *cannot* edit the code they judge — designed to compose with Superpowers and GSD, not compete |
| **Orchestration & context** | Not covered | `orchestration.md` (fan-out economics, packet contracts, model tiering, judge panels, loop stop conditions) and `context-engineering.md` (compaction survival, subagent isolation), grounded in Anthropic's primary engineering guidance |
| **Slop** | Implicit taste | An explicit minimalism ladder with a safety carve-out, plus a slop taxonomy for code, tests, prose, and artifacts |
| **Compounding** | Static instructions | `/retro` + `/mint-skill` + an optional learning gate: every session can leave the repo's agentic setup smarter than it found it |
| **Ecosystem** | Isolated | Preflight detects and recommends proven frameworks (Superpowers, GSD's successor) with exact install commands; `meta.md` maps what to steal from where |
| **Reach** | Codex-first, single install path | Claude Code (plugin/skill), Codex, and every AGENTS.md harness (OpenCode, Cursor, Gemini CLI); all scripts run from clone, skills dir, or plugin cache |
| **Quality bar** | Phrase-matching tests | 64 behavioral tests; four adversarial multi-agent review rounds (50+ reviewer/skeptic agents) with every confirmed finding fixed and regression-tested |

## Why Use This

Agentic coding fails in predictable ways. Each one gets a mechanism here — not a paragraph of advice, a *mechanism*:

| Pain point | What this repo does about it |
| --- | --- |
| **Agents claim "done" when it isn't** | A deterministic Stop-hook gate: the agent *cannot end its turn* while your tests/lint fail. Plus a read-only `skeptic-verifier` subagent whose only job is to refute completion claims. |
| **Slop** — filler comments, dead abstractions, gamed tests, flattering summaries | `anti-slop.md`: a 7-rung minimalism ladder (with a hard safety carve-out), and a slop taxonomy for code, tests, prose, and artifacts that reviews are run against. |
| **Context rot on long tasks** | `context-engineering.md`: just-in-time retrieval, durable notes that survive compaction, subagent context isolation with distilled 1-2k-token returns. |
| **No traceability** — what was asked, decided, verified? | T0-T3 tiers with one canonical state file per tier, a requirement traceability matrix, and a verification ledger that final claims must cite. Validated by `verify_run.py`, not by promises. |
| **Multi-agent chaos or waste** | `orchestration.md`: when fan-out pays (roughly an order of magnitude more tokens — usually worth it for discovery/review/verification, *not* authoring), sizing tables, structured packet contracts, model tiering, judge panels, loop-until-dry. |
| **Goal loops that never terminate or terminate early** | Deterministic conditions → the stop gate. Judgment conditions → the built-in `/goal`. Batch loops → machine-checkable stop conditions, circuit breakers, budget caps. |
| **Every session relearns the same lessons** | `/retro` mines each session for durable lessons and routes them to the right home; `/mint-skill` turns repeated workflows into new skills/subagents with tuned trigger descriptions; an optional learning gate blocks the first stop of a session once and prompts a `/retro` pass before the agent can finish. |
| **Reinventing what the ecosystem already solved** | The preflight detects and recommends proven frameworks (Superpowers plugin, GSD's successor) with exact install commands, and `meta.md` maps the ecosystem (Ponytail, Headroom, Beads, compound engineering) so you steal ideas instead of rebuilding them. |

Grounded, not vibes: built from Anthropic's primary engineering guidance (context engineering, the multi-agent research system, skill authoring), reviewed by adversarial multi-agent passes whose skeptic verifiers reproduced every reported bug before it was fixed, and covered by a behavioral test suite (`python3 -m pytest -q`).

## Quick Start (any repo, new or existing)

One guided command — audits first, shows what it will create, asks before writing:

```bash
python3 ultimate-agentic-workflow/scripts/setup.py --project-root .        # add --yes to skip the prompt
```

Or run the pieces individually:

```bash
# Read-only audit: what's present, what's missing, what to run next:
python3 ultimate-agentic-workflow/scripts/preflight.py --project-root .

# Bootstrap agent files + the .claude kit (refuses to overwrite anything):
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli both --claude-kit --project-root .

# Existing CLAUDE.md/AGENTS.md? Print the rendered files and merge by hand instead:
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli both --claude-kit --stdout --project-root .
```

The preflight also checks that core tools are usable (ripgrep, Serena, ast-grep,
uv) and whether proven frameworks are installed — the Superpowers plugin
(`/plugin install superpowers@claude-plugins-official`) and GSD (original repo
archived; successor open-gsd/gsd-core, install: `npx @opengsd/gsd-core@latest`) — and prints install
commands for anything missing. It installs nothing itself; every install is
approval-first.

### What you get after setup

- `AGENTS.md` / `CLAUDE.md`: tiny always-loaded bootloaders with your repo's detected build/test/lint commands (Node incl. pnpm/yarn/bun, Python, Rust, Go, Maven, Gradle, Ruby).
- `OPS.md`: the shared operational guide where durable repo lessons accumulate.
- `.claude/`: five focused subagents (`code-reviewer`, `skeptic-verifier`, `test-runner`, `researcher`, `implementer`), the stop-gate and learning-gate hooks, `/retro` + `/mint-skill` skills, and a settings template with safe defaults.
- Then configure the gate: put your test/lint commands in `.claude/stop-gate.json` and the agent literally cannot claim completion while they fail.

## Install The Skill

**Claude Code (plugin — easiest).** This repo is a plugin marketplace; inside Claude Code run:

```text
/plugin marketplace add jfmaes/awesome-ai-workflow
/plugin install ultimate-agentic-workflow@awesome-ai-workflow
```

**Claude Code (skills directory).** Copy it project-local or user-level:

```bash
mkdir -p .claude/skills            # or: mkdir -p ~/.claude/skills
cp -R ultimate-agentic-workflow .claude/skills/
```

**Codex.** Copy it into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ultimate-agentic-workflow "${CODEX_HOME:-$HOME/.codex}/skills/"
```

**Other harnesses (OpenCode, Cursor, Gemini CLI, ...).** Clone the repo anywhere and run the Quick Start scripts — see Harness Support below.

Start a new agent session and invoke it, e.g.:

```text
Use ultimate-agentic-workflow to initialize this repo for accountable AI coding.
```

## For AI Agents

If you are an agent reading this: the entrypoint is `ultimate-agentic-workflow/SKILL.md`. It is the router — read it first, then load references on demand (they are all exactly one level deep from it). Conventions you need:

- `<skill-dir>` in any documented command means the directory containing `SKILL.md` — a repo clone (`ultimate-agentic-workflow/`), a skills-directory install, or the plugin cache. All scripts work from any of them.
- Classify every task T0-T3 before acting; ceremony scales with risk, and the tier's canonical state file is defined in `references/workflow.md` → State Ownership.
- Never claim completion without a fresh verification-ledger row. Never present self-review as independent review.
- Run `python3 <skill-dir>/scripts/preflight.py --project-root .` before proposing setup changes; everything that installs or mutates config requires user approval with exact commands, write targets, risks, and rollback.

## Migrating from v1

Repos that installed the previous version of this workflow migrate in minutes, and `preflight.py` detects the v1 layout and prints these steps for you:

**v1 Claude layout** (`CLAUDE.md` bootloader + `AGENTS.md` acting as the operational guide — the roles changed in v2):

```bash
git mv AGENTS.md OPS.md    # the old AGENTS.md was the ops guide; that role now lives in OPS.md
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli both --claude-kit --skip-existing --project-root .
# optional: diff your CLAUDE.md against the fresh template and merge improvements
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli claude --stdout --project-root .
```

**v1 Codex layout** (`AGENTS.md` + `OPS.md`): the roles are unchanged — just add the missing pieces:

```bash
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli both --claude-kit --skip-existing --project-root .
```

**The skill itself**: replace the old copy in your skills directory (`~/.codex/skills/` or `.claude/skills/`) with this version, or switch to the plugin install.

**Your artifacts are safe**: v2 kept the tier model, requirement/verification IDs, `.workflow/<slug>/` layout, and spec formats. Existing `specs/`, `.workflow/` runs, and `memory-bank/` content need no changes — v2 only clarified that `memory-bank` is a projection, not the canonical state. `--skip-existing` guarantees nothing you customized gets touched.

## Harness Support

| Piece | Claude Code | Codex | OpenCode / Cursor / Gemini CLI / other AGENTS.md harnesses |
| --- | --- | --- | --- |
| References (workflow, orchestration, context-engineering, anti-slop, meta, large-codebase, pilot) | yes | yes | yes — plain markdown, point your harness at them |
| `AGENTS.md` bootloader + `OPS.md` | yes (also reads AGENTS.md) | yes | yes — the AGENTS.md convention is the cross-harness standard |
| `CLAUDE.md` bootloader | yes | — | — |
| Scripts (`setup.py`, `preflight.py`, `init_agents.py`, `verify_run.py`, `large_codebase_tools.py`) | yes | yes | yes — plain Python 3, no harness dependency |
| `.claude/` kit: subagents, Stop hooks, `/retro`, `/mint-skill` | yes | — | — (mechanisms are Claude Code's; the agent role prompts in `assets/claude/agents/` are plain markdown and port as system prompts) |
| Plugin install | yes | — | — |

The enforcement layer (hooks, stop gates, subagents) is harness-native by
necessity; everything else — the tiers, ledgers, orchestration patterns,
context rules, and anti-slop gates — travels with any harness that can read
markdown and run Python.

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

## Repository Layout

```text
ultimate-agentic-workflow/
|-- SKILL.md                     # the router — agents start here
|-- .claude-plugin/plugin.json   # plugin manifest
|-- scripts/
|   |-- setup.py                 # one-command guided setup
|   |-- preflight.py             # read-only readiness audit
|   |-- init_agents.py           # deterministic bootstrap (+ --claude-kit, --stdout)
|   |-- verify_run.py            # T3 run-directory gate
|   `-- large_codebase_tools.py  # tool readiness for big repos
|-- assets/
|   |-- templates/               # BOOTLOADER.md, OPS.md
|   `-- claude/                  # the installable .claude/ kit
|       |-- agents/              # code-reviewer, skeptic-verifier, test-runner,
|       |                        # researcher, implementer
|       |-- hooks/               # stop_gate.py, learn_gate.py
|       |-- skills/              # retro/, mint-skill/
|       `-- settings.json.template
`-- references/
    |-- workflow.md              # T0-T3 lifecycle, ledgers, state ownership
    |-- orchestration.md         # fan-out, packets, verification patterns, loops
    |-- context-engineering.md   # context budgets, compaction survival
    |-- anti-slop.md             # minimalism ladder, slop taxonomy
    |-- claude-code-kit.md       # the kit, goal loops
    |-- meta.md                  # minting skills/subagents, ecosystem map
    |-- large-codebase.md        # search routing, permission-gated tooling
    `-- pilot-measurement.md     # measure tools before trusting them

.claude-plugin/marketplace.json  # makes this repo /plugin-installable
tests/                           # behavioral test suite
```

## Development

```bash
python3 -m pytest -q                                            # test suite
python3 -m compileall ultimate-agentic-workflow/scripts tests   # syntax check
git diff --check                                                # whitespace
```

## Design Rules

- Keep always-loaded agent files short; operational detail lives in `OPS.md`
  or the skill references (see `references/large-codebase.md` for search and
  tooling policy).
- One canonical live-state file per tier; everything else is a projection.
- Use `.workflow/<slug>/` only when the task needs durable evidence.
- Fan out subagents for discovery and verification, not for coupled authoring.
- Enforcement beats memory: anything that must happen every time becomes a
  hook or gate, not a reminder.
- Prefer proven frameworks over reinvention; prefer read-only readiness checks
  and exact approval text over silent installs.
- Treat acceleration claims as hypotheses until the pilot protocol measures
  them.

## Changelog

### 2026-07-04 — v2: the next-generation rework

- **One-command entrypoint**: `setup.py` (guided, never overwrites), plugin
  packaging (`/plugin marketplace add jfmaes/awesome-ai-workflow`), and a
  `<skill-dir>` convention so every documented command works from a clone,
  a skills install, or the plugin cache.
- **`.claude/` starter kit**: five subagents (code-reviewer, skeptic-verifier,
  test-runner, researcher, implementer), a deterministic stop-gate Stop hook
  (blocks completion while configured checks fail, anchored on
  `CLAUDE_PROJECT_DIR`), an optional once-per-session learning gate, `/retro`
  and `/mint-skill` skills, and a settings template.
- **New references**: `orchestration.md`, `context-engineering.md`,
  `anti-slop.md`, `meta.md`, `claude-code-kit.md` — grounded in primary
  sources and the verified ecosystem (Superpowers, Ponytail, Headroom,
  compound engineering, GSD, Beads, teach/reflect).
- **Preflight + brownfield support**: read-only audit of repo state, tools,
  and frameworks with an ordered next-steps list; `--stdout` merge path for
  repos with existing agent files; multi-harness documentation.
- **workflow.md overhaul**: provenance cut, four overlapping ledgers
  consolidated into one traceability matrix + verification ledger, explicit
  per-tier state ownership, deterministic gates, loop stop conditions.
- **Hardened scripts**: fixed the dual-CLI `AGENTS.md` corruption bug,
  non-object/empty `package.json` crashes, partial writes under `--force`,
  symlink and ignored-dir handling in the readiness checker; added
  `verify_run.py`; multi-ecosystem command detection.
- **Tests**: phrase-presence checks replaced with behavioral tests,
  including regressions for every bug confirmed by adversarial
  multi-agent review passes.

### 2026-05 — v1

- Initial `ultimate-agentic-workflow` skill: T0-T3 tier model, traceability
  workflow, large-codebase readiness checker, pilot measurement protocol,
  Codex/Claude bootloader templates.

## Credits & Current Scope

Patterns adapted (concepts, not copied text) from Anthropic's engineering
guidance and the ecosystem: obra/superpowers, Ponytail, Headroom, Every's
compound engineering, GSD, Beads, and alexknowshtml's teach/reflect skills —
see `references/meta.md` for the full map.

This repo is intentionally small. It is not a framework, daemon, or hosted
service. It is a portable skill plus references, scripts, and tests that
target agent behavior in other repositories.
