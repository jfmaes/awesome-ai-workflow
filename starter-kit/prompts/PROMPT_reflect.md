0a. Study @IMPLEMENTATION_PLAN.md and @IMPLEMENTATION_PLAN_DONE.md to understand the full picture of what was accomplished and what remains.
0b. Study @AGENTS.md to see current operational knowledge.
0c. Study recent git log (last 20 commits) to see what changed.
0d. Study `specs/*` to compare intent vs outcome.
0e. Study ~/AI_RETRO.md (full file) to see current cross-project learnings.
0f. If @HUMAN.md exists, study it for unresolved blockers and progress entries.
0g. Study review logs in `logs/ralph_review_*` (if present) to understand review outcomes — how many approved, fixed, discarded, skipped.

1. Perform a structured reflection on the recent build session. Ultrathink.

## Analyze:
- What tasks were completed successfully?
- What tasks required multiple iterations or self-correction? Why?
- Were there any patterns in failures (wrong assumptions, missing context, bad task sizing)?
- Did the plan need regeneration? Why?
- Were specs accurate, or did they need updating?
- What did the review step catch? Were discards justified or over-aggressive?
- Are there unresolved blockers in HUMAN.md that need human attention?

## Produce a reflection report:

Create or update `REFLECTION.md` with:

### Session Summary
- Tasks completed: [count]
- Tasks requiring rework: [count]
- Reviews: [approved/fixed/discarded/skipped counts]
- Plan regenerations: [count]
- Spec updates: [count]
- Unresolved blockers: [count, brief description]

### What Worked
- [Pattern or approach that was effective]

### Friction Points
- [Where things went wrong and root cause]

### AGENTS.md Updates
- [Specific operational learnings to add — keep brief]

### Cross-Project Learnings
- [Patterns that would apply to OTHER projects]

### Process Improvements
- [Changes to prompts, loop config, or workflow]

2. Apply AGENTS.md updates directly. Keep AGENTS.md under 60 lines — consolidate if needed.

3. Update ~/AI_RETRO.md using a subagent:
   - Add new cross-project learnings to the **Recent** section with today's date and project name.
   - Check the Recent section count. If >20 entries:
     a. Identify patterns that have been confirmed across 2+ projects → promote to **Rules** or the appropriate **Stack** section.
     b. Move outdated or one-off entries to ~/AI_RETRO_ARCHIVE.md.
     c. Trim Recent back to ≤20 entries.
   - Check **Rules** section. If >20 lines, consolidate: merge similar items, remove anything superseded.
   - Check each **Stack** section. If >10 lines, consolidate.

4. Do NOT implement any code changes. This is reflection only.

IMPORTANT: Be honest about failures. A reflection that says "everything went perfectly" is useless. The value is in identifying patterns that prevent future mistakes.
