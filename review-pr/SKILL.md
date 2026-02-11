---
name: review-pr
description: "Review a feature branch before merging. Use when: (1) A build loop has finished on a feature branch, (2) User says 'review this branch', 'review PR', 'is this ready to merge', 'check my branch', (3) User wants a structured quality assessment of all changes on a branch vs main. Produces a structured review with spec compliance, architectural assessment, and merge recommendation."
---

# Review PR

Review the aggregate work on a feature branch before merging to main. This is the step between "build loop finished" and "create PR."

The per-iteration review prompt (`PROMPT_review.md`) scores individual commits. This skill reviews the **whole branch** — catching issues that only emerge when you look at the full diff.

## When to Use

- After `./loop.sh build` completes on a feature branch
- Before running `gh pr create`
- When you want a second opinion on branch-level quality

## Workflow

### Step 1: Identify the base branch

Determine the base branch to diff against. In order of preference:
1. If the user specifies a base branch, use that
2. Check if there's an upstream tracking branch configured
3. Default to `main` (or `master` if main doesn't exist)

### Step 2: Gather context

Study these in parallel:
- `git diff <base>...HEAD` — the full diff of all changes on this branch
- `git log <base>..HEAD --oneline` — all commits on this branch
- `specs/*` — the specifications this work should satisfy
- `IMPLEMENTATION_PLAN.md` — what tasks were planned
- `IMPLEMENTATION_PLAN_DONE.md` — what tasks were completed
- `HUMAN.md` — any unresolved blockers

### Step 3: Assess the branch

Evaluate the branch holistically. Ultrathink. Score each dimension 1-10:

**Spec Compliance:**
- Does the implementation match what the specs describe?
- Are acceptance criteria met?
- Are there spec requirements that were missed entirely?

**Architectural Quality:**
- Do the changes fit the existing codebase patterns?
- Are there cross-cutting concerns (e.g., a series of individually-fine commits that collectively create inconsistency)?
- Is there unnecessary complexity or over-engineering?

**Test Coverage:**
- Are all required tests present?
- Do tests cover edge cases from the specs?
- Are there untested code paths in the diff?

**Completeness:**
- Are there TODOs, stubs, or placeholders left in the diff?
- Does IMPLEMENTATION_PLAN.md still have pending tasks that should have been done?
- Are there unresolved blockers in HUMAN.md?

**Code Hygiene:**
- Dead code, unused imports, debug artifacts?
- Consistent naming and style with the rest of the codebase?
- Documentation where needed (not everywhere — only where logic isn't self-evident)?

### Step 4: Produce the review

Output a structured review:

```markdown
## Branch Review: <branch-name> → <base-branch>

### Summary
- Commits: [count]
- Files changed: [count]
- Tasks completed: [count from IMPLEMENTATION_PLAN_DONE.md]
- Unresolved blockers: [count from HUMAN.md, or "none"]

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Spec compliance | X/10 | [brief] |
| Architecture | X/10 | [brief] |
| Test coverage | X/10 | [brief] |
| Completeness | X/10 | [brief] |
| Code hygiene | X/10 | [brief] |
| **Overall** | **X/10** | |

### Critical Issues (must fix before merge)
- [issue + file:line + what to fix]

### Non-Critical Notes (address later)
- [observation — won't block merge]

### Recommendation
**MERGE** / **FIX THEN MERGE** / **NEEDS REWORK**

[1-2 sentence rationale]
```

### Step 5: Offer next steps

Based on the recommendation:

- **MERGE**: Offer to run `gh pr create` with the review summary as the PR body
- **FIX THEN MERGE**: List the critical fixes. Offer to fix them now (interactive, not a loop — these are targeted fixes)
- **NEEDS REWORK**: Suggest what to change in IMPLEMENTATION_PLAN.md and whether to re-run the build loop

## Key Rules

- **Review the diff, not individual commits.** The per-commit review already happened in the loop. This is about the aggregate.
- **Compare against specs, not assumptions.** If a spec says X and the code does Y, that's a finding — even if Y seems reasonable.
- **Distinguish critical from non-critical.** Style nits should never block a merge. Missing spec requirements should always block.
- **Be direct.** "This is ready to merge" or "This needs X fixed" — not "consider perhaps maybe..."
- **Check for things only visible at branch level:** inconsistent patterns across files, missing integration between components, architectural drift from the original plan.
