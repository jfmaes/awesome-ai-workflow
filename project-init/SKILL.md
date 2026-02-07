---
name: project-init
description: "Initialize AI-assisted development projects with adaptive workflow scaffolding. Use when: (1) Starting a new project or repo from scratch, (2) Adding AI workflow structure to an existing codebase, (3) User says 'init', 'initialize', 'bootstrap', 'set up for AI coding', 'add Ralph', 'add spec/plan workflow', (4) User wants CLAUDE.md, AGENTS.md, specs, or loop infrastructure generated. Produces project rules, operational guide, specs, implementation plan, and optionally a Ralph loop script. Uses a tier system (T0-T3) to scale process to task complexity."
---

# Project Init

Bootstrap AI-assisted development projects with adaptive workflow scaffolding.

Produces: CLAUDE.md, AGENTS.md, specs/, IMPLEMENTATION_PLAN.md, loop.sh, and prompt files — populated for the specific project through a structured interview.

## Quick Start

1. Read templates from this skill's `templates/` directory
2. Interview the user about their project
3. Study the existing codebase (if any)
4. Generate all files
5. Verify with user

## Workflow

### Step 1: Read Templates

Before doing anything, load the reference templates:

```
view templates/CLAUDE.md.template
view templates/AGENTS.md.template
view templates/SPEC_TEMPLATE.md
view templates/TIER_REFERENCE.md
```

### Step 2: Interview

Ask the user these questions **one group at a time**. Wait for answers before proceeding. Skip groups that don't apply.

**Group 1 — Project Identity:**
- What is this project? (1-2 sentence pitch)
- What is the primary Job To Be Done for the end user?
- Any secondary JTBDs?

**Group 2 — Technical Stack:**
- Language(s) and frameworks?
- Build system and package manager?
- Test framework + run command?
- Linter/formatter + run command?
- How to build and run locally?
- Docker or containerization?

**Group 3 — Architecture:**
- Monolith, services, or other?
- Key directories? (or offer to study the repo)
- Database(s) and query layer?
- External APIs or integrations?

**Group 4 — Conventions:**
- Code style preferences?
- Anti-patterns to avoid?
- Git workflow (branch naming, commit format)?
- Anything the AI should NEVER do?

**Group 5 — Current State (existing repos only):**
- What works? What's broken? What's missing?
- Known tech debt?
- Previous AI-generated code needing attention?

### Step 3: Study Existing Codebase (if applicable)

If there's existing code:
1. Study directory structure
2. Study config files (package.json, pyproject.toml, Dockerfile, Cargo.toml, etc.)
3. Identify existing patterns, utilities, conventions
4. Note inconsistencies or gaps
5. Check for existing CLAUDE.md, AGENTS.md, or similar — don't overwrite without asking

### Step 4: Assess Complexity Tier

Based on the interview and codebase study, assess the project's **typical task complexity** and tell the user:

| Tier | Description | Files to Generate |
|------|-------------|-------------------|
| T0-T1 | Simple project, quick tasks | CLAUDE.md only |
| T2 | Multi-file work, design decisions | CLAUDE.md, AGENTS.md, specs/, spec template |
| T3 | Major feature, architecture, multi-session | Full kit: CLAUDE.md, AGENTS.md, specs/, plan, loop.sh, all prompts |

State the assessment:
> "This looks like a T2/T3 project. I'll generate [list of files]. Want the full Ralph loop infrastructure, or just the spec/plan templates?"

### Step 5: Generate Files

Generate files in the project root using the templates as structure. **Populate with project-specific content from the interview and codebase study.**

#### Always generate:

**CLAUDE.md** — Fill in all sections. Keep under 100 lines.
- Project name, description, stack
- Build/run/test/lint commands (verified if possible)
- Architecture and directory layout
- Code style and anti-patterns
- Git conventions
- Tier system reference (from TIER_REFERENCE.md)

**AGENTS.md** — Start minimal. Only include confirmed information.
- Build & run commands
- Validation commands
- Leave Operational Notes and Codebase Patterns mostly empty

#### Generate for T2+:

**specs/*.md** — One per JTBD topic of concern.
- Use SPEC_TEMPLATE.md structure
- Include acceptance criteria
- Flag unknowns as `OPEN_QUESTION:`

**IMPLEMENTATION_PLAN.md** — Initial gap analysis.
- Compare specs against existing code
- Prioritized task list
- Mark as draft (will be regenerated)

#### Generate for T3 (if user wants Ralph loop):

**loop.sh** — Copy from templates/loop.sh.template, make executable.

**prompts/** directory:
- PROMPT_plan.md
- PROMPT_build.md
- PROMPT_plan_work.md
- PROMPT_reflect.md

Copy from templates, then customize:
- Update source directory references (`src/*` → actual directory)
- Update shared utilities path (`src/lib/*` → actual path)
- Verify ~/AI_RETRO.md reference path

### Step 6: AI_RETRO.md Setup

Check if ~/AI_RETRO.md exists:
- If yes: no action needed
- If no: create ~/AI_RETRO.md and ~/AI_RETRO_ARCHIVE.md from templates

Add a matching **Stack** section to ~/AI_RETRO.md if one doesn't exist for this project's language.

### Step 7: Verify

Present a summary to the user:

```
Files generated:
  ✅ CLAUDE.md (XX lines)
  ✅ AGENTS.md (XX lines)
  ✅ specs/topic-a.md
  ✅ specs/topic-b.md
  ✅ IMPLEMENTATION_PLAN.md (XX tasks)
  ✅ loop.sh (executable)
  ✅ prompts/ (4 files)
  ✅ ~/AI_RETRO.md (created/updated)

Tier assessment: T[X]
Recommended workflow: [description]
```

Ask:
1. Does anything need correction?
2. Ready to start working?

## Key Rules

- **Study before assuming.** "Don't assume not implemented." Check for existing files before generating.
- **Keep CLAUDE.md under 100 lines.** It's loaded every context window.
- **Keep AGENTS.md under 60 lines.** Start nearly empty — it grows through use.
- **Specs must be actionable.** Detailed enough that an agent can implement without asking questions.
- **The plan is disposable.** Getting it wrong is cheap. Don't over-invest in the initial plan.
- **Don't over-scaffold.** A T1 project doesn't need Ralph loop infrastructure. Match ceremony to complexity.
- **Verify commands work.** If you can test build/test/lint commands, do so before writing them to CLAUDE.md.
