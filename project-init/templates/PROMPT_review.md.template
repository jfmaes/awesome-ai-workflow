You are reviewing the most recent build iteration. Your job is to score the work and either approve, fix, or discard it.

0a. Study the git diff of HEAD (the last commit from the build iteration): `git diff HEAD~1..HEAD`. If HEAD~1 doesn't exist (first commit), use `git show HEAD` instead. If nothing was committed this iteration, write SCORE=0 ACTION=skipped and stop.
0b. Study `specs/*` to compare intent vs implementation.
0c. Study @IMPLEMENTATION_PLAN.md for task context.
0d. If @HUMAN.md exists, check for stale blockers and flag them.

1. Score the implementation 1-10 based on:
   - **Spec compliance** — Does it match what the spec describes?
   - **Code quality** — Clean, idiomatic, no obvious bugs or anti-patterns?
   - **Test coverage** — Are required tests present and meaningful?
   - **Completeness** — Is the task fully done, or are there stubs/placeholders?

2. Classify issues by severity:
   - **Critical** (blocks progress): broken tests, security issues, spec violations, missing core functionality → must fix or discard
   - **Non-critical** (note for later): style nits, minor refactoring opportunities, optional improvements → note in @IMPLEMENTATION_PLAN.md but do NOT block approval

3. Based on the score, take ONE of these actions:

   **Score >= 8 — APPROVE:**
   - Write the score file and done. No changes needed.

   **Score 6-7 — ATTEMPT FIXES (critical issues only):**
   - Fix only critical issues. Leave non-critical items as notes in @IMPLEMENTATION_PLAN.md for future iterations.
   - `git add -A && git commit -m "review: fix [brief description]"`
   - Re-score after fixes.
   - If now >= 8, approve.
   - If still < 8 after one round of fixes, discard (see below).

   **Score < 6 — DISCARD:**
   - The commit is too low quality to salvage quickly.
   - Run `git reset --hard HEAD~1` to discard the commit.
   - Document why in @IMPLEMENTATION_PLAN.md — add a note to the relevant task about what went wrong so the next build iteration avoids the same mistakes.
   - Write the score file.

4. Write the score file `.ralph_review_score` with exactly this format:
   ```
   SCORE=N
   ACTION=approved|fixed|discarded|skipped
   ```
   Where N is the final score (1-10) and ACTION is what you did.

IMPORTANT: Be honest and rigorous. A review that always approves is useless. The value is in catching bad code before it accumulates. But also be pragmatic — non-critical style issues should never block approval or trigger a discard.
