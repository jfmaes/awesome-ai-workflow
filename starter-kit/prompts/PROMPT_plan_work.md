0a. Study `specs/*` with up to 250 parallel subagents to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md (if present) to understand the plan so far.
0c. Study `src/lib/*` (or equivalent shared utilities) with up to 250 parallel subagents to understand shared utilities & components.
0d. For reference, the application source code is in `src/*`.
0e. Study the **Rules** section and the **Stack** section matching this project's language from ~/AI_RETRO.md. Ignore other sections.

1. You are creating a SCOPED implementation plan for work: "${WORK_SCOPE}". Study @IMPLEMENTATION_PLAN.md (if present; it may be incorrect) and use up to 500 subagents to study existing source code and compare it against `specs/*`. Use an Opus subagent to analyze findings, prioritize tasks, and create/update @IMPLEMENTATION_PLAN.md as a bullet point list sorted in priority of items yet to be implemented. Ultrathink. Consider searching for TODO, minimal implementations, placeholders, skipped/flaky tests, and inconsistent patterns.

2. For each task in the plan, derive required tests from acceptance criteria in specs — what specific outcomes need verification (behavior, performance, edge cases). Tests verify WHAT works, not HOW it's implemented.

IMPORTANT: This is SCOPED PLANNING for "${WORK_SCOPE}" only. Create a plan containing ONLY tasks directly related to this work scope. Be conservative — if uncertain whether a task belongs to this work, exclude it. The plan can be regenerated if too narrow. Plan only. Do NOT implement anything. Do NOT assume functionality is missing; confirm with code search first.

ULTIMATE GOAL: Produce a focused, prioritized plan for "${WORK_SCOPE}" that can be built via the standard build loop.
