# Project Initialization Prompt

> **Usage:** Copy this into your first Claude Code or Codex session for a new project.
> It will interview you, then populate CLAUDE.md, AGENTS.md, and initial specs.
> After this conversation, you're ready to run `./loop.sh plan`.

---

You are initializing a new project for autonomous AI-assisted development using the Ralph methodology.

## Your Tasks

### Phase 1: Interview (ask me, don't assume)

Ask me the following, one group at a time. Wait for my answers before proceeding.

**Project Identity:**
- What is this project? (1-2 sentence elevator pitch)
- What is the primary Job To Be Done (JTBD) for the end user?
- What secondary JTBDs exist?

**Technical Stack:**
- Language(s) and frameworks?
- Package manager and build system?
- Test framework and how to run tests?
- Linter/formatter and how to run them?
- How to build and run the project locally?
- Docker or other containerization?

**Architecture:**
- Monolith, microservices, or something else?
- Key directories and what lives where? (or should I study the existing repo?)
- Database(s) and ORM/query layer?
- External APIs or integrations?

**Conventions:**
- Code style preferences (functional vs OOP, naming, file structure)?
- Any anti-patterns you specifically want to avoid?
- Git workflow (branch naming, commit message format)?
- Anything the AI should NEVER do in this codebase?

**Current State:**
- Is there existing code, or are we starting fresh?
- If existing: what works, what's broken, what's missing?
- Known technical debt?
- Any previous AI-generated code that needs attention?

### Phase 2: Study (if existing repo)

If there's an existing codebase:
1. Study the directory structure
2. Study key config files (package.json, pyproject.toml, Dockerfile, etc.)
3. Identify existing patterns, utilities, and conventions
4. Note any inconsistencies or gaps

### Phase 3: Generate Files

Based on my answers and your study, generate:

1. **CLAUDE.md** — Project rules file (use the template in this repo)
   - Fill in all sections with project-specific details
   - Include build/test/lint commands
   - Document conventions and anti-patterns
   - Keep it under 100 lines

2. **AGENTS.md** — Start minimal (use the template)
   - Only include what you've confirmed works
   - Build/run/test commands
   - Leave Operational Notes mostly empty (Ralph will populate through iteration)

3. **specs/*.md** — One spec per JTBD topic of concern
   - Use the spec template
   - Include acceptance criteria
   - Flag open questions as `OPEN_QUESTION:`

4. **IMPLEMENTATION_PLAN.md** — Initial plan
   - Gap analysis: specs vs current code
   - Prioritized task list
   - Note: this is a first draft; will be regenerated after review

### Phase 4: Verify

After generating all files:
1. Show me a summary of what was created
2. Ask if anything needs correction
3. Confirm I'm ready to start the loop

---

**Remember:**
- Study before assuming. "Don't assume not implemented."
- Keep CLAUDE.md and AGENTS.md concise — they're loaded every iteration.
- Specs should be detailed enough that an agent can implement without asking questions.
- The plan is disposable. Getting it wrong is cheap.
