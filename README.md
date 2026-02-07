# AI-Assisted Development Workflow

A practical system for working with AI coding assistants (Claude Code, OpenAI Codex, Claude.ai) across the full spectrum of tasks — from quick fixes to autonomous build loops.

**Now with full OpenAI Codex support!** The system auto-detects your CLI and adapts file naming and loop infrastructure accordingly.

Built on principles from the [Ralph Playbook](https://claytonfarr.github.io/ralph-playbook/), [Cursor Memory Bank](https://github.com/vanzan01/cursor-memory-bank), and [Addy Osmani's LLM coding workflow](https://addyosmani.com/blog/ai-coding-workflow/).

---

## The Core Idea

Not every task needs the same amount of ceremony. A one-line bug fix and a greenfield microservice are fundamentally different jobs, and your AI workflow should adapt accordingly.

This system provides:

- **A complexity tier system** that scales process to the task
- **Templates for specs, plans, and project rules** when structure is needed
- **Ralph-style autonomous loops** for sustained build sessions — used selectively
- **A reflection and learning cycle** so the system improves over time
- **Cross-project persistence** so learnings carry forward

The LLM should identify the right tier and suggest the appropriate workflow, not blindly apply the heaviest process to every request.

---

## Complexity Tiers

Every task falls into one of four tiers. The LLM should assess this at the start and state its assessment. You can always override.

### Tier 0 — Just Do It

**Signals:** Single question, quick fix, one file, clear intent, low risk.

**Workflow:** Answer or implement directly. No ceremony.

**Examples:**
- "Fix this TypeError on line 42"
- "Add a docstring to this function"
- "What does this regex do?"
- "Rename this variable across the file"

**What the LLM should say:** *(nothing special — just do it)*

---

### Tier 1 — Think Aloud

**Signals:** Medium task, clear scope, 1–3 files, some design choices but nothing architectural.

**Workflow:** State the approach in 2–3 sentences. Confirm if ambiguous. Execute.

**Examples:**
- "Write a script to deduplicate files by hash"
- "Add input validation to this API endpoint"
- "Refactor this function to reduce nesting"
- "Write unit tests for the auth module"

**What the LLM should say:**
> "I'll approach this by [X]. I'll touch [files]. The main decision is [Y] — I'm going with [Z] because [reason]. Starting now."

---

### Tier 2 — Spec & Plan

**Signals:** Multi-file changes, touches existing systems, design decisions with tradeoffs, affects other contributors, non-trivial scope.

**Workflow:** Produce a brief spec → get approval → produce a plan → get approval → execute in focused chunks.

**Examples:**
- "Add a new lab section to SEC699 Day 2"
- "Implement file deduplication for the fleet manager"
- "Add OAuth to the API"
- "Create a new MCP server for X"

**What the LLM should say:**
> "This is a T2 task — let me draft a quick spec before we start building. I want to confirm [scope/approach/constraints] with you first."

**Files used:** Spec (inline or `specs/*.md`), brief plan, CLAUDE.md for conventions.

---

### Tier 3 — Full Spec + Plan + Loop

**Signals:** New system or major feature, architectural decisions, multi-session work, high cost of getting it wrong, many moving parts.

**Workflow:** Full spec.md → plan.md → approval gate → build (potentially via Ralph loop) → reflect → persist learnings.

**Examples:**
- "Design and build the fleet management system for 100+ endpoints"
- "Modernize SEC699 from on-prem to hybrid identity-aware"
- "Build the RAG engine's hard-wall data isolation layer"
- "Create the 2D isometric game's sprite pipeline"

**What the LLM should say:**
> "This is a T3 task. Before touching code, I want to build a proper spec covering [requirements, data model, constraints, acceptance criteria]. Then we'll produce an implementation plan you can review. Want me to start the spec, or do you want to discuss the approach first?"

**Files used:** `specs/*.md`, `IMPLEMENTATION_PLAN.md`, `CLAUDE.md`, `AGENTS.md`, potentially Ralph loop.

---

### Tier Detection Signals

The LLM should consider these factors when assessing tier:

| Factor | Lower Tier | Higher Tier |
|--------|-----------|-------------|
| **Files touched** | 1–2 | 5+ |
| **Reversibility** | Easy to undo | Hard to undo |
| **Domain risk** | Blog post, utility script | Security tooling, production API |
| **Existing system** | Greenfield or isolated | Integrated with other components |
| **Ambiguity** | Clear requirements | Vague or conflicting |
| **Duration** | Minutes | Hours to days |
| **Audience** | Just you | Students, clients, public |
| **Dependencies** | None | External APIs, other teams |

**Override phrases:**
- "Just do it" / "quick fix" → T0 regardless
- "Let me think about this" / "let's plan" → T2+
- "I need a spec" / "this is complex" → T3
- "Ralph it" / "loop it" → T3 with autonomous loop

---

## When to Use Ralph Loops (and When Not To)

Ralph loops are powerful but expensive. They burn through API tokens fast — each iteration loads specs, plan, and AGENTS.md from scratch. That's by design (fresh context = smart zone), but it means Ralph is a power tool, not the default.

### Use Ralph When

| Scenario | Why Ralph Works |
|----------|----------------|
| **10+ well-defined tasks** from a solid plan | Loop picks the next task automatically — you don't need to steer |
| **Overnight/background builds** | Set it and come back to committed code |
| **Repetitive patterns** with strong backpressure | Tests catch errors; each iteration is isolated |
| **Codebase migration/refactoring** | Systematic, bounded work across many files |
| **Spec is clear, creativity is low** | Ralph excels at execution, not design decisions |

### Don't Use Ralph When

| Scenario | What to Do Instead |
|----------|-------------------|
| **Exploring/prototyping** — you don't know what you want yet | Interactive session (T1–T2). Iterate by hand. |
| **< 5 tasks** — loop overhead isn't worth it | Just work through tasks in one session |
| **High-creativity work** — architecture, design, UX | Creative phase manually (T2–T3), then maybe Ralph the implementation |
| **Budget-constrained** — watching token spend | Interactive sessions give you more control per token |
| **Debugging a specific issue** — you need to steer | Interactive with breakpoints and inspection |
| **Specs are vague or changing** | Finish the spec first, THEN consider Ralph |

### What the LLM Should Suggest

When you describe a task, the LLM should proactively assess:

```
"This looks like a T2 task. I'd suggest we:
1. Draft a brief spec (5 min)
2. Produce a plan with ~8 tasks
3. Work through them interactively

Ralph loop isn't worth it here — there are only 8 tasks and
some need design decisions. Want to start with the spec?"
```

Or conversely:

```
"This is T3 with about 25 well-defined implementation tasks
after planning. Good candidate for a Ralph loop once the spec
and plan are approved. Want me to start the spec?"
```

---

## File Structure

### Per-Project Files (live in the repo)

```
project/
├── loop.sh                         # Ralph loop orchestrator (multi-CLI support)
├── ralph_stream_parser.py          # Stream parser for human-readable loop output
├── CLAUDE.md / AGENTS.md           # Project rules (Claude uses CLAUDE.md, Codex uses AGENTS.md)
├── AGENTS.md / OPS.md              # Operational guide (Claude uses AGENTS.md, Codex uses OPS.md)
├── IMPLEMENTATION_PLAN.md          # Task list (generated, updated by loops)
├── REFLECTION.md                   # Post-session reflections
├── prompts/
│   ├── PROMPT_plan.md              # Planning mode prompt
│   ├── PROMPT_build.md             # Building mode prompt
│   ├── PROMPT_plan_work.md         # Scoped planning for feature branches
│   └── PROMPT_reflect.md           # Reflection mode prompt
├── specs/
│   ├── _TEMPLATE.md               # Spec template
│   └── [topic].md                  # One per JTBD topic of concern
├── logs/                           # Loop execution logs (gitignored)
└── src/                            # Application code
```

**CLI-aware file naming:**
| Purpose | Claude Code | OpenAI Codex |
|---------|-------------|--------------|
| Project instructions | `CLAUDE.md` | `AGENTS.md` |
| Operational guide | `AGENTS.md` | `OPS.md` |

The `loop.sh` script auto-detects which CLI you have installed and uses the appropriate files.

### Cross-Project Files (live in your home directory)

```
~/
├── AI_RETRO.md                     # Cross-project learnings (size-capped, selectively loaded)
├── AI_RETRO_ARCHIVE.md             # Historical learnings (never loaded into context)
└── ralph-starter-kit/              # This kit (fork per project)
```

### Token Budget Per Iteration

Every Ralph iteration loads fixed context before doing real work. Keep this lean:

```
CLAUDE.md / AGENTS.md  ~2K tokens   (project rules, <100 lines)
AGENTS.md / OPS.md     ~1.5K tokens (operational guide, <60 lines)
AI_RETRO.md (partial)  ~0.5K tokens (Rules + one Stack section only)
specs/*                ~2-5K tokens (varies — keep specs focused)
IMPLEMENTATION_PLAN.md ~1-3K tokens (shrinks as tasks complete)
────────────────────────────────────
Fixed overhead:        ~7-12K tokens per iteration
```

AI_RETRO.md uses **selective loading** to stay bounded:
- Build/plan prompts load ONLY the Rules section (~20 lines) + the matching Stack section (~10 lines)
- The reflect prompt loads the full file but only to perform maintenance
- The Archive file is never loaded into build/plan context

### Claude.ai (Persistent Memory)

- **Memory edits** — Workflow rules, preferences, cross-project patterns
- **Past chat search** — Historical context, searchable by topic
- **Projects** — Per-project instructions and knowledge files for sustained work

---

## How Everything Connects

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Claude.ai   │    │  Claude Code  │    │    Codex     │      │
│  │  (thinking)  │    │  (building)   │    │  (building)  │      │
│  ├──────────────┤    ├──────────────┤    ├──────────────┤      │
│  │ • Ideation   │    │ • T0–T3 work │    │ • T0–T3 work │      │
│  │ • Research   │    │ • Ralph loops │    │ • Ralph loops│      │
│  │ • Retros     │    │ • Spec/Plan  │    │ • Spec/Plan  │      │
│  │ • Planning   │    │ • Reflection │    │ • Reflection │      │
│  │   discussions│    │              │    │              │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              PERSISTENCE LAYER                      │       │
│  ├─────────────────────────────────────────────────────┤       │
│  │                                                     │       │
│  │  Per-Repo          Cross-Project     Claude.ai      │       │
│  │  ┌───────────┐    ┌─────────────┐   ┌───────────┐  │       │
│  │  │ CLAUDE.md │    │ AI_RETRO.md │   │ Memory    │  │       │
│  │  │ AGENTS.md │    │ (~/home)    │   │ Edits     │  │       │
│  │  │ specs/*   │    │             │   │ (30 slots)│  │       │
│  │  │ plan      │    │             │   │           │  │       │
│  │  │ reflection│    │             │   │ Past Chat │  │       │
│  │  └───────────┘    └─────────────┘   │ Search    │  │       │
│  │                                     └───────────┘  │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              LEARNING FLYWHEEL                      │       │
│  │                                                     │       │
│  │  Build ──▶ Reflect ──▶ Update AGENTS.md             │       │
│  │    │                        │                       │       │
│  │    │          CROSS_PROJECT learnings                │       │
│  │    │                        │                       │       │
│  │    │                ┌───────┴────────┐              │       │
│  │    │                ▼                ▼              │       │
│  │    │          AI_RETRO.md    Claude.ai              │       │
│  │    │          (patterns)     memory edits           │       │
│  │    │                │                │              │       │
│  │    ▼                ▼                ▼              │       │
│  │  Next task     Other repos     All future           │       │
│  │  benefits       benefit        conversations        │       │
│  │                                benefit              │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Information Flow

1. **You have an idea** → Discuss in Claude.ai (ideation) or jump straight into Claude Code (if scope is clear)
2. **LLM assesses tier** → Suggests appropriate workflow
3. **For T2–T3**: Spec and plan are produced → You approve → Execution begins
4. **For Ralph loops**: `./loop.sh plan` → `./loop.sh` → autonomous execution
5. **After substantial work**: `./loop.sh reflect` or manual reflection captures learnings
6. **Cross-project learnings** flow to `~/AI_RETRO.md` and Claude.ai memory edits
7. **Next time** you start a project or conversation, the system is slightly smarter

---

## Getting Started

### First Time Setup (Once)

1. **Download the starter kit** to `~/ralph-starter-kit/`
2. **Copy `AI_RETRO.md` and `AI_RETRO_ARCHIVE.md` to your home directory** — these live outside repos
3. **Optionally**: set up Claude.ai memory edits encoding your workflow preferences

### New Project Setup

**Option 1: Use the project-init skill (recommended)**

In Claude Code, run:
```
/project-init
```

The skill will interview you about your project and generate all files automatically, including:
- Correct file naming for your CLI (Claude or Codex)
- Populated CLAUDE.md/AGENTS.md or AGENTS.md/OPS.md
- Project-specific specs and plan
- Executable loop.sh

**Option 2: Manual setup**

```bash
# 1. Copy the kit into your project
cp -r ~/ralph-starter-kit/{CLAUDE.md,AGENTS.md,loop.sh,ralph_stream_parser.py,prompts,specs,IMPLEMENTATION_PLAN.md} /path/to/project/
cd /path/to/project/

# 2. If using Codex, rename files:
#    CLAUDE.md → (delete)
#    AGENTS.md → OPS.md
#    Then create AGENTS.md from project-init/templates/CODEX.md.template

# 3. Make scripts executable
chmod +x loop.sh ralph_stream_parser.py
```

### Day-to-Day Usage

**Most of the time (T0–T2):** Just work in Claude Code or Codex normally. The tier system is a mental model, not mandatory process. CLAUDE.md is loaded automatically and gives the LLM project context.

**When scope grows (T2):** Ask the LLM to draft a spec. Review it. Then work through the plan interactively.

**When you have a big batch (T3):** Spec → Plan → approve → `./loop.sh` → `./loop.sh reflect`.

**Periodically:** Review `~/AI_RETRO.md`, update Claude.ai memory edits, prune stale rules from AGENTS.md.

---

## Ralph Loop Reference

### Commands

```bash
./loop.sh build                     # Build mode, unlimited (Ctrl+C to stop)
./loop.sh build 20                  # Build mode, max 20 iterations
./loop.sh plan                      # Planning mode (gap analysis → task list)
./loop.sh plan 5                    # Planning mode, max 5 iterations
./loop.sh plan-work "feature desc"  # Scoped plan for feature branch
./loop.sh reflect                   # Post-build reflection
```

### Environment Variables

```bash
RALPH_CLI=claude ./loop.sh          # Force Claude Code (auto-detected by default)
RALPH_CLI=codex ./loop.sh           # Force OpenAI Codex
RALPH_MODEL=sonnet ./loop.sh        # Sonnet for speed/cost (Claude)
RALPH_MODEL=opus ./loop.sh plan     # Opus for planning (Claude, default)
RALPH_MODEL=codex ./loop.sh         # Codex model (OpenAI, default)
RALPH_PROMPTS_DIR=prompts ./loop.sh # Custom prompt directory
```

The loop auto-detects which CLI you have installed (`claude` or `codex`) and uses appropriate model defaults:
- **Claude Code**: `sonnet` for build, `opus` for plan/reflect
- **OpenAI Codex**: `codex` for all modes

### Feature Branch Workflow

```bash
./loop.sh plan                                    # Full plan on main
git checkout -b ralph/user-auth                    # Feature branch
./loop.sh plan-work "OAuth with session mgmt"      # Scoped plan
./loop.sh 15                                       # Build (max 15 tasks)
./loop.sh reflect                                  # Capture learnings
gh pr create --base main --fill                    # PR
```

### Safety

Ralph runs with `--dangerously-skip-permissions`. **Always use a sandbox** (Docker, VM, or at minimum a repo where `git reset --hard` is acceptable). The loop.sh includes a confirmation prompt before starting.

---

## The Self-Improvement Cycle

### After a Build Session

Run `./loop.sh reflect` or do it manually. The reflection identifies:

- **What worked** → reinforce in AGENTS.md
- **What failed** → add guardrails to AGENTS.md or CLAUDE.md
- **Cross-project patterns** → add to `~/AI_RETRO.md`
- **Workflow improvements** → update prompts or loop config

### Monthly Retro (in Claude.ai)

Prompt:
> "Let's do a workflow retro. Search our recent chats and tell me what patterns you see — friction points, repeated corrections, things that worked well."

### What Goes Where

| Learning Type | Destination | Example |
|---------------|-------------|---------|
| How to build/test THIS project | `AGENTS.md` | "Run `pytest -x` — fail fast" |
| Project conventions | `CLAUDE.md` | "All endpoints return JSON envelope" |
| Cross-project patterns | `~/AI_RETRO.md` (auto-updated by reflect) | "Confirm lab Day/Section before writing content" |
| Workflow preferences | Claude.ai memory | "Prefers implementation-first for prototypes" |
| One-time decisions | Nowhere (searchable) | "Chose approach B for fleet dedup" |

---

## Production Readiness

### Ready to Use ✅

| Component | Notes |
|-----------|-------|
| **Tier system** | Mental model + LLM guidance. Works immediately. |
| **CLAUDE.md template** | Standard practice. Auto-loaded by Claude Code. |
| **AGENTS.md template** | Deliberately minimal. Grows through use. |
| **Spec template** | JTBD-oriented with acceptance criteria. |
| **PROMPT_plan.md** | Faithful Ralph methodology + acceptance-driven tests. |
| **PROMPT_build.md** | Faithful Ralph methodology. Community battle-tested. |
| **PROMPT_plan_work.md** | Clean implementation of Clayton Farr's enhancement. |
| **AI_RETRO.md** | Simple journal. Value comes from the habit. |
| **INIT_PROMPT.md** | Interview-based bootstrapping. Will refine with use. |

### Needs a Live Test Run ⚠️

| Component | What to Verify |
|-----------|---------------|
| **loop.sh** | Verify `claude -p` piping, `--dangerously-skip-permissions`, and `--model` flags match your Claude Code CLI version. Test git push handling. Run a 3–5 iteration test on a throwaway repo first. |
| **PROMPT_reflect.md** | Untested prompt. Concept is proven but wording needs tuning. Expect 2–3 iterations after seeing actual output. |
| **Subagent counts** | "Up to 250/500 parallel subagents" comes from Geoff's setup. Start lower if you're watching costs. These are ceilings, not targets. |
| **Cross-project flow** | AI_RETRO updates are automated via PROMPT_reflect.md, but the compaction logic (promote/archive when Recent >20) hasn't been tested. Watch the first few reflections to verify it consolidates properly. |

### Not Included (Future Additions)

| Feature | What It Would Do | When to Add |
|---------|-----------------|-------------|
| **LLM-as-judge tests** | Subjective quality backpressure (UX, tone) | When building user-facing features |
| **AUDIENCE_JTBD.md** | SLC release slicing based on audience | When doing product work vs internal tooling |
| **Codex-specific prompt** | OPENAI.md tuned for Codex strengths | When Codex workflow diverges enough to warrant it |
| **Token budget tracking** | Monitor spend per session | When costs become a concern |
| **Automated retro script** | Grep reflections, suggest memory edits | After 10+ reflections exist |

---

## Customization

### Tuning Prompts

Key language patterns from Ralph methodology:
- **"study"** (not "read") — triggers deeper analysis
- **"don't assume not implemented"** — THE critical guardrail against duplication
- **"ultrathink"** — extended reasoning for complex decisions
- **"capture the why"** — forces intent documentation
- **Guardrails use ascending 9s** — higher number = more critical

Add guardrails only after observing failures. Don't preemptively add rules.

### Tuning AGENTS.md

Start nearly empty. Geoff's advice:

1. Watch initial loops
2. Spot where Ralph goes wrong
3. Add one brief, specific rule
4. Never add rules for problems that haven't happened

Keep under 60 lines. Loaded every iteration — bloat here is expensive.

---

## FAQ

**Do I need Ralph for every project?**
No. Most work is T0–T2 and doesn't need a loop. Ralph is for T3 batch execution with 10+ tasks from a solid plan.

**What about Codex?**
Full Codex support is built-in! The system auto-detects your CLI and adapts:
- Files are named appropriately (AGENTS.md for project instructions, OPS.md for operational guide)
- `loop.sh` auto-detects and uses the `codex` CLI with `--yolo` mode
- Stream parser works with both Claude's stream-json and Codex's JSON events
- All templates and prompts are model-agnostic

Just install the Codex CLI and run `./loop.sh` — it works identically to Claude Code.

**How do I handle multi-session work without Ralph?**
End-of-session: ask the LLM to summarize state, decisions, and next steps as a handoff note. Paste it at the start of the next session.

**What's a Ralph session cost in tokens?**
Each iteration loads ~5K–15K tokens of fixed context (specs + plan + AGENTS.md) plus codebase reads. A 20-iteration session: roughly 500K–2M tokens. Planning is cheaper (1–3 iterations).

**Can I override the tier?**
Always. "This is T0, just do it" or "treat this as T3" — the system is guidance, not enforcement.

---

## Credits

- [Geoff Huntley](https://ghuntley.com/ralph/) — Ralph methodology
- [Clayton Farr](https://claytonfarr.github.io/ralph-playbook/) — Ralph Playbook
- [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/) — Spec/Plan/Code workflow
- [vanzan01](https://github.com/vanzan01/cursor-memory-bank) — Memory Bank complexity levels
- [Vinci Rufus](https://www.vincirufus.com/posts/ralph-loop-compound-engineering-future-software-development/) — Compound engineering
