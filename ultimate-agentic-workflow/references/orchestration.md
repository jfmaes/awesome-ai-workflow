# Multi-Agent Orchestration

Read this before spawning subagents, running parallel work, or starting an autonomous loop. It covers when fan-out pays for itself, how to size it, the packet contract workers must honor, and the verification patterns that keep multi-agent output trustworthy.

## Contents

- Economics: When Multi-Agent Helps and Hurts
- Fan-Out Sizing
- Packet Contract
- Worker Rules
- Model and Effort Tiering
- Verification Patterns
- Judge Panel for Design Selection
- Loop-Until-Dry Discovery
- Autonomous Loop Stop Conditions

## Economics: When Multi-Agent Helps and Hurts

Agent work costs roughly an order of magnitude more tokens than chat, and multi-agent systems cost several times more again. Fan-out must be justified by value.

Helps:

- breadth-first discovery and research where questions are independent
- work that exceeds one context window
- independent verification of findings (fresh context is the point)
- audits and migrations over many independent targets

Hurts:

- most code *authoring*: tightly coupled changes, shared context, cross-file dependencies
- anything where workers would share a write scope
- tasks small enough that coordination overhead exceeds the work

Default: single agent with worktree/branch isolation for authoring; fan-out for discovery, review, and verification.

## Fan-Out Sizing

Scale worker count to task complexity, and guard against over-spawning:

| Task shape | Workers | Budget guidance |
| --- | --- | --- |
| Simple fact-finding or single lookup | 0-1 | A few tool calls; usually do it inline |
| Direct comparison or bounded survey | 2-4 | ~10-15 tool calls each |
| Open-ended discovery, audit, or multi-track research | 5-10+ | Explicitly divided, non-overlapping responsibilities |

Never spawn a swarm for a question one agent can answer. If unsure, start small and widen only when the first round proves the space is larger than expected.

## Packet Contract

Every packet has an owner, a bounded scope, and a structured result. The dispatch must specify: objective, context pointers, files or sources, explicit do/do-not boundaries, expected output format, and how the result will be verified.

Dispatch template:

```markdown
# Packet <ID>: <Name>

## Objective

## Context

## Files or Sources

## Ownership

## Do

## Do Not

## Expected Output

## Verification
```

Workers return a small, flat, structured result — not prose the controller must interpret:

```json
{
  "packet_id": "01-discovery",
  "status": "done | blocked | failed",
  "findings": [
    {"summary": "string", "evidence": "path/to/file:line", "confidence": "high | medium | low"}
  ],
  "files_touched": ["string"],
  "checks_run": [{"command": "string", "result": "pass | fail"}],
  "open_questions": ["string"]
}
```

Keep the schema flat. Validate it at the controller boundary the moment the result arrives; a malformed result is a failed packet, not something to guess around.

## Worker Rules

- Each worker gets a disjoint write scope. Parallel implementation is allowed only when write scopes do not overlap.
- Parallel code-writing workers use isolated worktrees or branches. Remember worktrees are fresh checkouts: untracked files (`.env`, local config) are absent unless copied deliberately.
- Workers are told they are not alone in the codebase and must not revert others' edits.
- Workers ask for missing context instead of guessing.
- Workers return distilled summaries with `file:line` evidence (see `context-engineering.md`), never raw logs.
- The controller checks worker claims against diffs and command output before integrating. A worker's "done" is a claim, not evidence.

## Model and Effort Tiering

Route by blast radius, not habit:

- Strongest model, highest effort: orchestration, spec and design decisions, integration judgment, final verification and review.
- Cheaper, faster models: mechanical packets — bulk searches, codemods, file-by-file transformations, formatting, well-specified boilerplate.
- Reasoning effort is a second routing axis: scale it with the risk tier and blast radius of the step, not uniformly.

If a cheap-model packet fails twice on the same objective, escalate the model rather than retrying a third time.

## Verification Patterns

Author-verified work is weakly verified. Isolation from the author's context is what removes self-review bias.

- **Fresh-context verifier:** for T2+ work, the verifying agent must not share the author's conversation. Give it the spec, the diff, and the verification commands — not the author's reasoning.
- **Skeptic pass:** for load-bearing findings or claims, dispatch a verifier whose only job is to refute the claim. Instruct it to default toward refuted when uncertain. A claim that survives a motivated skeptic is worth more than one that was merely double-checked.
- **Perspective-diverse verify:** when something can fail in more than one way, give each verifier a distinct lens (correctness, security, does-it-reproduce) instead of several identical checkers.
- **Reward-hack check:** ask explicitly, "could this pass its checks without genuinely doing the task?" — tests weakened, fixtures gamed, acceptance criteria satisfied in letter but not intent. "Tests pass" alone is not sufficient evidence.

## Judge Panel for Design Selection

When the solution space is wide, generate N independent approaches from distinct angles (e.g. simplest-possible, risk-first, user-first), then judge.

- Judges must see all candidates together in one context; comparative judgment beats independent scoring for relative decisions.
- Score against the spec's requirements, not aesthetics.
- Synthesize from the winner and graft the best ideas from runners-up; record the decision and rejected alternatives in the design decision doc.

## Loop-Until-Dry Discovery

For unknown-size discovery (bugs, issues, edge cases), fixed counts miss the tail. Instead:

1. Run a round of finders (diverse angles: by-file, by-symptom, by-history).
2. Deduplicate against everything already seen — including previously rejected findings, or the loop never converges.
3. Verify fresh findings with a skeptic pass.
4. Stop after 2 consecutive rounds that surface nothing new, with a hard cap on total rounds as a backstop.

## Autonomous Loop Stop Conditions

Any autonomous loop (Ralph-style or otherwise) needs machine-checkable termination, not "the agent feels done":

- **Success gate:** exit only when the deterministic checks pass — tests, typecheck, lint, build — plus the plan's acceptance criteria audit.
- **Circuit breaker:** stop and surface the state when the same error, an empty diff, or the same failing check recurs on consecutive iterations.
- **Budget cap:** a hard iteration or token cap set before the loop starts.
- **Checkpoint rule:** any irreversible or externally visible action (deploy, publish, migration, external mutation) forces a stop for approval regardless of loop state.
- **State in files:** each iteration commits or persists progress to the plan/state files so the loop tolerates fresh-context restarts. Progress lives in git and the run directory, not in the loop's context window.

Never present loop output as verified. The loop produces work; verification is a separate fresh-context pass.

On Claude Code, prefer existing primitives over hand-rolled loops: a deterministic stop-gate hook for exact conditions and the built-in `/goal` command for judgment-based conditions — see `claude-code-kit.md`.
