# Stop Ralphing Everything: An Adaptive AI Coding Workflow

*How we built a system that scales from "just fix it" to autonomous build loops — and learns from every session.*

---

I've been spending a lot of time lately thinking about how I work with AI coding assistants. Not the novelty of it — that wore off months ago — but the *efficiency* of it. How do I stop repeating myself across projects? How do I prevent the AI from going off the rails on complex tasks? And how do I make each session slightly better than the last?

The answer, it turns out, isn't a single tool or a master prompt. It's a system — one that knows when to get out of the way and when to enforce discipline.

## The Problem: One Size Doesn't Fit All

The AI coding community has converged on a few powerful ideas in 2025-2026. Addy Osmani popularized the Spec → Plan → Code workflow. Geoff Huntley gave us Ralph — autonomous bash loops that keep the AI in its "smart zone" by clearing context every iteration. The Cursor Memory Bank project showed how phased workflows (VAN → PLAN → CREATIVE → BUILD → REFLECT → ARCHIVE) can bring structure to chaotic development sessions.

These are all great. But they share a problem: **they assume every task deserves the full treatment.**

I'm not going to write a spec.md, plan.md, and spin up an autonomous loop to rename a variable. Equally, I'm not going to just say "build me a fleet management system" and hope for the best. The missing piece is *adaptive complexity* — a system that scales its process to the task at hand.

## The Tier System: Let the AI Diagnose the Task

The core of the workflow is a four-tier complexity system. The LLM assesses the tier at the start of every task and states its assessment. You can always override.

**Tier 0 — Just Do It.** One file, clear intent, low risk. The AI should just execute. No preamble, no ceremony, no "let me first outline my approach." Just do it.

**Tier 1 — Think Aloud.** Medium tasks. The AI states its approach in 2-3 sentences, flags any assumptions, and starts working. "I'll add input validation to the three POST endpoints. I'm going to use Pydantic models since the rest of the codebase does. Starting now."

**Tier 2 — Spec & Plan.** Multi-file changes, design decisions with tradeoffs, things that affect other people's work. The AI drafts a brief spec, gets approval, produces a plan, gets approval, then executes in focused chunks.

**Tier 3 — Full Spec + Plan + Loop.** Major features, architectural decisions, multi-session work. Full JTBD spec, implementation plan, approval gates, potentially a Ralph loop for execution, and a reflection phase to capture learnings.

The detection signals are intuitive: files touched, reversibility, domain risk, ambiguity, duration, audience. A bug fix in a utility script is T0. A new auth system for a training platform is T3. The AI should be able to tell the difference and say so.

The key insight is that **the AI should actively suggest the tier**, not just comply with whatever level of ceremony you throw at it. If you ask it to "build OAuth support" without a spec, it should push back: "This is a T2 task — let me draft a quick spec before we start building."

## Ralph Is a Power Tool, Not a Screwdriver

I love the Ralph methodology. Fresh context per iteration, file-based memory, backpressure through tests — it's elegant. But it burns through tokens fast. Each iteration reloads specs, plan, AGENTS.md, and studies the codebase from scratch. A 20-iteration build session can consume 500K-2M tokens.

That's fine for overnight batch builds on a well-specified project. It's absurd for 5 tasks you could knock out in a single interactive session.

So the workflow is explicit about when to Ralph and when not to:

**Ralph is for:** 10+ well-defined tasks from a solid plan, overnight builds, systematic migration/refactoring, anything where the spec is clear and creativity is low.

**Ralph is not for:** Exploration, prototyping, debugging, anything with fewer than 5 tasks, high-creativity work, budget-constrained sessions.

The LLM should know this and say it. "This is a good candidate for a Ralph loop — 25 implementation tasks, clear specs, strong test coverage. Want me to generate the plan?" Or: "Only 6 tasks here, some needing design decisions. Let's work through these interactively instead of looping."

## The Learning Flywheel

Here's where it gets interesting. Every AI coding session generates implicit knowledge: what worked, what didn't, how the codebase actually behaves, which approaches this particular project needs. Normally, that knowledge evaporates when the context window clears.

The workflow captures it through three persistence layers:

**Per-repo persistence (AGENTS.md):** Operational learnings about *this specific project*. Build commands, test gotchas, codebase patterns. Updated automatically during Ralph loops, or manually after interactive sessions. This is Ralph's AGENTS.md, faithfully implemented. The key rule: keep it operational, keep it under 60 lines. It's loaded every iteration, so bloat here is expensive.

**Cross-project persistence (~/AI_RETRO.md):** Patterns that transcend individual projects. "Always confirm lab section placement before writing content." "When building MCP servers, define the tool schema first." This file lives in your home directory, outside any repo, and is shared across all your work.

The critical design challenge with AI_RETRO.md is **token creep**. If you work on 100 projects and each contributes learnings, the file becomes massive — exactly the kind of context pollution that degrades AI performance.

The solution is tiered structure with hard size caps:

- **Rules** (max 20 lines): Universal, distilled, proven patterns. Loaded every iteration.
- **Stack sections** (max 10 lines each): Python-specific, C#-specific, etc. Only the relevant section is loaded.
- **Recent** (max 20 entries): Rolling buffer. New learnings land here. When full, they must be promoted to Rules/Stack or archived.
- **Archive** (separate file): Historical reference. Never loaded into context.

Build and plan prompts only load Rules + the matching Stack section (~30 lines, ~500 tokens). The reflect prompt loads the full file to perform maintenance — promoting, consolidating, archiving. The total fixed context overhead per iteration stays bounded at ~7-12K tokens regardless of how many projects you've completed.

**Claude.ai memory (meta-layer):** For people who use Claude.ai alongside Claude Code or Codex, memory edits encode the highest-level workflow rules — preferences that apply to *how you work with AI in general*, not to any specific project. These are always in context in Claude.ai conversations, making ideation sessions and retrospectives informed by everything you've learned.

## The Reflection Loop

The compound engineering insight — that each feature should make the next feature easier to build — requires a mechanism to actually capture and apply learnings. In our workflow, that's the reflection phase.

After a substantial build session, `./loop.sh reflect` runs a structured analysis:

- What tasks completed successfully?
- What required multiple iterations or self-correction? Why?
- Were there patterns in failures?
- Did the plan need regeneration?

The reflection prompt then does three things automatically:
1. Updates AGENTS.md with operational learnings for this project
2. Updates ~/AI_RETRO.md with cross-project patterns (including compaction if the Recent section is full)
3. Produces a REFLECTION.md for the human record

This isn't just documentation — it's the mechanism by which the system gets smarter. A learning captured today ("always search before assuming something isn't implemented") becomes a rule loaded into every future iteration of every future project.

## The Multi-Tool Reality

Most AI coding workflow guides assume a single tool. In practice, I use three:

**Claude.ai** is the thinking room. Ideation, research, planning discussions, retrospectives. Long-form reasoning about architecture or approach before touching code. This is where memory edits live and where monthly workflow retros happen.

**Claude Code** (VS Code) is the workshop. T0-T3 work, Ralph loops, spec/plan generation, reflection. CLAUDE.md is auto-loaded. Filesystem persists naturally. This is where most actual work happens.

**OpenAI Codex** is the speed shop. Fast iteration, prototyping, cost-effective build sessions. Same spec/plan templates work here — the methodology is model-agnostic.

The persistence layer connects them: AGENTS.md and CLAUDE.md live in repos (shared by Claude Code and Codex). AI_RETRO.md lives in the home directory (shared across all repos). Claude.ai memory edits transcend all tools.

## What We Actually Built

The starter kit is a set of generic, forkable files:

**Templates:** CLAUDE.md (project rules), AGENTS.md (operational guide), spec template (JTBD-oriented with acceptance criteria), IMPLEMENTATION_PLAN.md (task list).

**Prompts:** PROMPT_plan.md (gap analysis, no implementation), PROMPT_build.md (one task per iteration with backpressure), PROMPT_plan_work.md (scoped planning for feature branches), PROMPT_reflect.md (structured reflection with AI_RETRO maintenance).

**Orchestration:** loop.sh with plan/build/plan-work/reflect modes, model selection, max-iteration limits, safety confirmation.

**Bootstrap:** INIT_PROMPT.md — an interview-based initialization prompt that populates all templates for a specific project. You paste it into Claude Code for a new project, answer questions about your stack and conventions, and it generates everything. Generic becomes specific without pre-filling.

**Cross-project:** AI_RETRO.md with size-capped sections and selective loading. AI_RETRO_ARCHIVE.md for historical reference.

The entire kit is designed to be forked per project. Copy it in, run the init prompt, and you're working.

## The Ideology

A few principles drove the design:

**Process should be proportional to risk.** The tier system isn't bureaucracy — it's an immune system. Low-risk tasks pass through freely. High-risk tasks trigger checkpoints. The AI should enforce this, not the human.

**Fresh context beats accumulated context.** Ralph's core insight applies everywhere. Don't let context rot. Start clean. Use files as memory, not the conversation window.

**Start with nothing and add rules reactively.** Geoff Huntley's advice for AGENTS.md applies to the whole system: don't pre-populate with imagined best practices. Watch where things go wrong, then add a specific guard. The system teaches you what it needs.

**Plans are disposable.** Regenerating a plan costs one loop iteration. Fighting a stale plan costs hours of accumulated drift. When in doubt, throw it away and re-plan.

**The human is on the loop, not in it.** Engineer the conditions for good outcomes. Set up backpressure (tests, lints, type checks). Write clear specs with acceptance criteria. Then let the AI work. Step in to course-correct, not to micromanage.

**The system should get smarter over time.** Every build session feeds the flywheel: AGENTS.md captures project-specific learnings, AI_RETRO.md captures cross-project patterns, memory edits capture workflow preferences. None of this requires manual effort beyond approving what the reflection phase proposes.

## What's Not Solved Yet

Being honest about gaps:

**The reflect prompt is theoretical.** It hasn't been battle-tested. The concept is proven — Memory Bank's /reflect, compound engineering — but the specific wording will need tuning after real sessions.

**AI_RETRO compaction is untested.** The selective loading and promote-or-archive logic makes sense on paper. Whether the LLM actually performs reliable compaction during reflection is an open question. The first few reflections will tell us.

**Codex integration is loose.** The templates work with any LLM, but there's no Codex-specific prompt or loop script yet. It'll come when the workflow diverges enough to warrant it.

**Claude.ai memory is small.** 30 slots × 200 characters is tight for encoding cross-project patterns. It forces discipline — only the most proven, universal rules earn a slot — but it means some learnings exist only in AI_RETRO.md and past chat search.

## Try It

The starter kit is designed to be picked up and used immediately. The tier system requires zero tooling — it's a mental model any LLM can apply from CLAUDE.md instructions. The templates are generic. The loop script needs one test run to verify CLI flags.

Start with a real project. Copy the kit in. Run INIT_PROMPT.md. Work through a few tasks interactively. Run a reflection. See what it captures.

The system will tell you what it needs next.

---

*Built by Jean-François, SANS instructor and builder of Offensive Guardian - An offensive security consultancy, with Claude. The starter kit is available as a forkable template. The workflow synthesizes ideas from Geoff Huntley (Ralph), Clayton Farr (Ralph Playbook), Addy Osmani (LLM coding workflow), vanzan01 (Cursor Memory Bank), and Vinci Rufus (compound engineering).*
