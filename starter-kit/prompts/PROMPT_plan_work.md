Phase 1 — RESEARCH (do this BEFORE reading the existing plan):

0a. Study `specs/*` with up to 250 parallel subagents to learn the application specifications.
0b. Study `src/lib/*` (or equivalent shared utilities) with up to 250 parallel subagents to understand shared utilities & components.
0c. For reference, the application source code is in `src/*`.
0d. Study the **Rules** section and the **Stack** section matching this project's language from ~/AI_RETRO.md. Ignore other sections.

1. EXPLORE the work scope "${WORK_SCOPE}" independently:
   - Use up to 500 subagents to research what this feature requires
   - Identify required components, dependencies, data models, API changes
   - Identify existing code that can be reused or needs modification
   - Map out the technical requirements WITHOUT referencing the existing plan
   - Ultrathink

Phase 2 — INTEGRATE:

2. NOW study @IMPLEMENTATION_PLAN.md (if present; it may be incorrect) and @IMPLEMENTATION_PLAN_DONE.md (if present) to understand what's already been done and what's currently planned. Identify overlaps between your research and existing items.

3. Merge your research findings into @IMPLEMENTATION_PLAN.md:
   - Add only new tasks that don't duplicate existing or completed items
   - For each task, derive required tests from acceptance criteria in specs — what specific outcomes need verification (behavior, performance, edge cases). Tests verify WHAT works, not HOW it's implemented.
   - TASK SIZING: Each task must be atomic and completable in a single build iteration. It should touch 1-3 files, have a clear "done" state verifiable by tests, and list the specific files to modify. If a task is too large, split it.
   - Sort by priority
   - Be conservative — if uncertain whether a task belongs to this work scope, exclude it. The plan can be regenerated if too narrow.

IMPORTANT: This is SCOPED PLANNING for "${WORK_SCOPE}" only. Create a plan containing ONLY tasks directly related to this work scope. Plan only. Do NOT implement anything. Do NOT assume functionality is missing; confirm with code search first.

ULTIMATE GOAL: Produce a focused, prioritized plan for "${WORK_SCOPE}" that can be built via the standard build loop.
