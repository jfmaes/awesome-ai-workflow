# Anti-Slop

Slop is output that looks like work but subtracts value: code nobody needed, comments that narrate, tests that cannot fail, summaries that flatter. This reference is the standing quality gate for everything an agent produces. It applies at every tier.

## Contents

- The Minimalism Ladder
- The Safety Carve-Out
- Code Slop
- Test Slop
- Prose Slop
- Artifact Slop
- Deliberate Shortcuts Become Debt

## The Minimalism Ladder

Before writing any code, walk this ladder in order and stop at the first rung that holds (pattern credit: Ponytail's YAGNI ladder):

1. Does this need to exist at all? If no requirement demands it — skip it.
2. Does the codebase already do it? Reuse it.
3. Does the stdlib cover it? Use the stdlib.
4. Does the platform provide it natively? Use the native feature.
5. Does an already-installed dependency do it? Use that.
6. Does it fit in one clear line? Write the line.
7. Only now: write the minimum code that works.

Be lazy about the solution, never about reading. The ladder only works after you understand the requirement and the surrounding code.

## The Safety Carve-Out

The ladder never applies to safety: input validation, authn/authz, error handling, data integrity, and accessibility are non-negotiable regardless of how much code they cost. "Less code" that erodes a safety guard is a defect, not minimalism.

## Code Slop

Reject in review (including self-review):

- **Narrating comments** — comments that restate the next line, describe the change history, or address the reviewer. A comment earns its place only by stating a constraint the code cannot show.
- **Speculative generality** — options, parameters, abstractions, and extension points no current requirement uses.
- **Dead abstractions** — wrappers around one call site, interfaces with one implementation, helper files with one helper.
- **Style mismatch** — code that ignores the surrounding file's naming, idiom, and comment density. New code should be indistinguishable from a good local author's.
- **TODO droppings** — TODO/FIXME added without a tracked follow-up.
- **Defensive theater** — try/except around code that cannot fail, null checks on values that cannot be null, re-validation of already-validated inputs.

## Test Slop

A test that cannot fail is worse than no test — it launders false confidence:

- Assertions weakened until they pass (`assert result is not None` on a function that never returns None).
- Tests that exercise mocks instead of behavior.
- Fixtures edited to match buggy output.
- Phrase-presence checks on prose where behavior could be checked instead.
- Tests added after the fact that would have passed before the change.

The check: could this test pass with the feature broken? If yes, it is slop. TDD's "see it fail first" exists precisely to prevent this.

## Prose Slop

In summaries, reports, and reviews:

- No hedged completion claims ("should work", "likely passes") — verify or say it is unverified.
- No sycophancy and no self-congratulation; findings, not adjectives.
- No restating the request back as if it were progress.
- Lead with the outcome; every sentence either informs a decision or gets cut.
- Report failures plainly, with output. A clean-looking summary of a failed run is the worst slop there is.

## Artifact Slop

- No workflow artifacts that no later phase reads (the workflow's own anti-pattern list applies).
- No generated files committed without being load-bearing.
- No documentation that duplicates other documentation; link instead.

## Deliberate Shortcuts Become Debt

Sometimes the minimum correct move is a shortcut. That is allowed — silently forgetting it is not. Every deliberate shortcut gets recorded as a tracked debt item (plan follow-up, issue, or `/retro` debt entry) with what was skipped and what it will cost later. Debt with a ledger entry is engineering; debt without one is slop.
