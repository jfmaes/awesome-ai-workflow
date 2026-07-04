# Ultimate Traceability Agentic Workflow

The goal is not maximum ceremony. The goal is maximum accountability at the minimum useful ceremony for the task's risk.

## Contents

- Core Contract
- Traceability Invariants
- State Ownership
- Repository Layout
- Tier Model
- Lifecycle Phases 00-14
- Requirement Traceability Matrix
- Deterministic Gates
- Autonomous Loop Policy
- Memory Hygiene
- Minimal Workflow by Tier
- Adoption Plan
- Anti-Patterns
- Final Accountability Standard

Related references, loaded on demand:

- `orchestration.md`: subagents, fan-out sizing, packet contract, verification patterns, loop stop conditions.
- `context-engineering.md`: context budget, durable notes, compaction survival, subagent isolation.
- `large-codebase.md`: search routing, tool readiness, permission-gated setup.
- `pilot-measurement.md`: measuring acceleration tools before trusting them.

## Core Contract

Every non-trivial agent run must leave behind enough evidence that another agent or human can answer:

1. What was requested?
2. What was assumed?
3. What sources were inspected?
4. What decisions were made, and what alternatives were rejected?
5. What exact work was planned?
6. Who or what agent owned each work packet?
7. What changed?
8. What proved the result?
9. What remains unresolved?
10. What should future sessions remember?

If the record cannot answer those questions, the run is not accountable.

## Traceability Invariants

These invariants apply to all tiers except true T0 one-shot answers:

- One source of truth per concern; other files are projections or history (see State Ownership).
- Requirement IDs are stable: `REQ-001`, `AC-001`, `DEC-001`, `TASK-001`, `VERIFY-001`, `REVIEW-001`.
- Every acceptance criterion maps to at least one verification check.
- Every design decision records considered alternatives and rationale.
- Every implementation task maps back to requirements or explicit maintenance work.
- Every final claim cites fresh evidence: no claim stronger than a verification ledger row.
- Every subagent packet has an owner, scope, constraints, expected output, and integration decision.
- Every risky action has an approval record before execution.
- Reflection updates operational knowledge only when it will change future behavior.

## State Ownership

Exactly one file owns live task state at any time. Everything else is a projection or historical record. Drift between state files is a process failure.

| Tier | Canonical live state | Projections / history |
| --- | --- | --- |
| T0 | none (the final answer is the record) | — |
| T1 | a short durable note: goal + constraints + current step, in the plan file or task note | — |
| T2 | the implementation plan (`IMPLEMENTATION_PLAN.md`) | `memory-bank/tasks.md` mirrors it if the repo uses that pattern |
| T3 | `.workflow/<slug>/state.json` | `plan.md` is the human-readable view; `memory-bank/*` and `IMPLEMENTATION_PLAN.md` are projections |

Rules:

- Update the canonical file first; sync projections after, or mark them stale.
- After compaction or session resume, re-anchor from the canonical file before acting (see `context-engineering.md`).
- Write the T1 durable note before any edit that could span a compaction: one or two lines is enough.

## Repository Layout

Default layout for a project adopting the full workflow. Most projects need only a subset — create directories when a tier first requires them, not upfront.

```text
project/
|-- AGENTS.md or CLAUDE.md      # bootloader (short, always loaded)
|-- OPS.md                      # operational guide: commands, validation, durable lessons
|-- IMPLEMENTATION_PLAN.md      # only while T2+ work is active
|-- specs/<topic>.md            # T2+ specs
|-- docs/decisions/             # design decision records
|-- .workflow/<run-slug>/       # T3 run evidence (plan.md, state.json, packets/, results/, final-report.md)
|-- logs/                       # gitignored raw logs
`-- src/
```

Optional compatibility patterns, used only when the target repo has adopted them:

- `memory-bank/` (tasks, active context, progress, creative, reflection, archive)
- `prompts/` and `loop.sh` for repos that actually run autonomous loops

`.workflow/<run-slug>/` is committed only when it contains useful audit artifacts rather than bulky transcripts.

## Tier Model

Assess the tier at intake; the user can override it.

| Tier | Use When | Required Artifacts | Normal Flow |
| --- | --- | --- | --- |
| T0: Just Do It | One answer, one obvious edit, low risk, easy rollback | None beyond the answer or tiny diff | Do the work; verify if a claim is made |
| T1: Think Aloud | One to three files, clear intent, modest risk | Durable goal note; command evidence if edited | Inspect -> act -> verify -> summarize |
| T2: Spec and Plan | Multi-file change, design choices, other contributors affected | Spec, implementation plan | Intake -> plan -> optional creative -> build -> verify -> review -> reflect |
| T3: Full Accountable Loop | Architecture, migration, high risk, multi-session, 10+ tasks, loop or swarm candidate | `.workflow/<slug>/`, spec, plan, risk gates, packet results, verification ledger, reflection/archive | Full lifecycle below |

Escalate the tier when any of these are true:

- The task touches security, payments, production data, user accounts, secrets, migrations, deployment, or public publishing.
- The agent would need broad edits, destructive commands, or long-running expensive jobs.
- Requirements are ambiguous or conflict.
- Verification requires multiple layers beyond unit tests.
- The user asks for a loop, swarm, subagents, or sustained autonomous execution.

De-escalate only when the user explicitly asks for a quick fix and the risk is genuinely low.

Ceremony maps to fragility: low tiers get judgment and prose; high tiers get exact artifacts, gates, and scripts. Do not apply T3 ceremony to T1 work.

## Lifecycle Overview

```text
00 Intake -> 01 Context Hydration -> 02 Scope and Risk Gate -> 03 Spec ->
04 Creative Design -> 05 Orchestration Plan -> 06 Isolation ->
07 Implementation Plan -> 08 Execution -> 09 Integration -> 10 Verification ->
11 Review -> 12 Reflection -> 13 Archive -> 14 Finish
```

Lower tiers skip phases per the Minimal Workflow by Tier section.

## 00 Intake

Purpose: convert the request into a tracked goal without losing the original wording.

Actions:

- Restate the goal in one sentence.
- Preserve the original objective verbatim in the tier's canonical state file (T1+).
- Identify stakeholders, user-visible outcomes, and non-goals.
- Assign a tier and say why.
- Record explicit constraints, such as "do not run pytest" or "static review only".

Exit evidence: goal statement, tier decision, initial success criteria, known constraints — in the canonical state file, not only in conversation.

Failure modes: shrinking the goal to the easiest subset; treating a vague request as implementation-ready; losing the original request to context compaction.

## 01 Context Hydration

Purpose: load only the context the current tier needs. Full policy: `context-engineering.md`.

T0-T1: read nearby instructions (`AGENTS.md`, `CLAUDE.md`, `OPS.md`, `README.md`) and the directly relevant files.

T2-T3: additionally read specs, active plans, recent commits, and relevant source; search for existing implementation before assuming a gap; load cross-project memory selectively.

Search routing: use the cheapest reliable retrieval mode first — exact text (`rg`), then symbol graph, then structural, then semantic as a last resort. The routing table and tool policy live in `large-codebase.md`; consult it for large or unfamiliar repos before adding search/MCP tooling, and run `scripts/large_codebase_tools.py --project-root . --json` before asking to install anything.

Exit evidence (T2+):

```markdown
## Source Ledger
| Source | Why Read | Findings | Used For |
| --- | --- | --- | --- |
| `AGENTS.md` | Project instructions | Test command is `npm test` | Verification plan |
| `src/auth/*` | Existing auth flow | Session middleware exists | Scope decision |
```

Failure modes: reading everything and wasting context; reading too little and duplicating existing work; using stale memory as current evidence.

## 02 Scope and Risk Gate

Purpose: decide whether work can proceed without additional approval.

Approval is required before:

- deleting, overwriting, mass-renaming, force-pushing, or rewriting history
- deploying, publishing, emailing, posting, or mutating external systems
- running database migrations, broad codemods, or dependency upgrades
- touching credentials, secrets, billing, production data, user accounts, or private customer data
- spawning many agents or running expensive jobs
- making changes outside the requested workspace

Safe without extra approval:

- reading local files in the requested workspace
- drafting specs, plans, packets, reports, and local workflow artifacts
- running narrow tests, linters, typechecks, builds, and dry runs
- creating non-destructive workflow directories under `.workflow/`

Exit evidence (T2+):

```markdown
## Risk Register
| Risk | Approval Required | Mitigation | Status |
| --- | --- | --- | --- |
| Broad codemod across API clients | Yes | Draft exact command first | Pending approval |
| Unit test run | No | Narrow command, local only | Approved by policy |
```

Failure modes: burying several risky actions in one broad approval; treating "agentic" as permission for external mutation; running destructive commands because they are reversible in theory.

## 03 Spec

Purpose: establish what must be true before planning implementation.

T2 minimum spec:

```markdown
# <Topic> Spec

## Goal

## Non-Goals

## Requirements
| ID | Requirement | Priority | Source |
| --- | --- | --- | --- |
| REQ-001 | ... | Must | User |

## Acceptance Criteria
| ID | Requirement | Criterion | Verification |
| --- | --- | --- | --- |
| AC-001 | REQ-001 | ... | VERIFY-001 |

## Constraints

## Open Questions
```

Rules:

- Acceptance criteria describe observable behavior, not implementation details.
- Unknowns are marked `OPEN_QUESTION`, not silently guessed.
- Requirement IDs are stable for the rest of the run.
- Specs are approved before implementation for T2+ unless the user explicitly chooses a lower-ceremony path.
- Requirements discovered during implementation are added back to the spec, not left implicit.

Failure modes: a plan containing requirements absent from the spec; acceptance criteria with no verification path.

## 04 Creative Design

Purpose: make major design choices explicit before code exists.

Use when architecture, UX, algorithms, data models, or operational strategy have real alternatives; when the wrong choice is expensive to reverse; or when multiple agents need one shared decision. When the solution space is wide, consider a judge panel over independent candidate designs (`orchestration.md`).

Template:

```markdown
# Design Decision: DEC-001 <Name>

## Problem

## Requirements
- REQ-001

## Options
| Option | Summary | Strengths | Weaknesses | Risk |
| --- | --- | --- | --- | --- |

## Decision

## Rationale

## Discarded Alternatives

## Implementation Guidance

## Verification Impact
```

Store decisions in `docs/decisions/DEC-001-<name>.md` (or `memory-bank/creative/` where that pattern is adopted).

Failure modes: "we chose X" without why; no record of rejected alternatives; a later implementer reopening the decision because it was not discoverable.

## 05 Orchestration Plan

Purpose: create a run-level accountability shell for T3 and multi-agent work. Subagent mechanics, packet contract, and fan-out sizing live in `orchestration.md`.

Create:

```text
.workflow/<run-slug>/
|-- plan.md          # human source of truth
|-- state.json       # canonical machine state
|-- orchestration.md # dispatch decisions
|-- packets/
|-- results/
`-- final-report.md
```

`plan.md` sections: Goal, Success Criteria, Current Context, Constraints, Risks, Approval Required, Work Packets, Integration Policy, Verification, Reusable Artifacts.

`state.json` is the canonical live state:

```json
{
  "goal": "string",
  "success_criteria": ["string"],
  "constraints": ["string"],
  "risks": [
    {"risk": "string", "approval_required": true, "mitigation": "string"}
  ],
  "max_concurrent_agents": 4,
  "max_total_agents": 12,
  "packets": [
    {
      "id": "01-discovery",
      "objective": "string",
      "files_or_sources": ["string"],
      "ownership": "string",
      "status": "pending"
    }
  ],
  "verification": [
    {"check": "string", "command": "string or null", "required": true, "status": "pending"}
  ]
}
```

Before execution, validate the run directory:

```bash
python3 <skill-dir>/scripts/verify_run.py --run-dir .workflow/<run-slug>
```

Failure modes: orchestration exists but does not drive actual work; `state.json` drifts from `plan.md`; results dumped without integration decisions.

## 06 Isolation

Purpose: protect the main workspace and make diffs attributable.

For T2+ code work:

- Prefer a git worktree or feature branch; parallel code-writing workers each get their own (see `orchestration.md`).
- Verify initial git status; record the base commit; confirm the test baseline when practical.

```markdown
## Isolation Record
| Field | Value |
| --- | --- |
| Base branch | `main` |
| Work branch | `agent/<slug>` |
| Base SHA | `<sha>` |
| Initial status | clean/dirty with notes |
| Baseline checks | command + result |
```

Rules:

- Never revert user changes unrelated to the task.
- If the workspace is dirty, distinguish user changes from agent changes.
- Do not start implementation on `main` unless the user explicitly accepts that risk.

Failure modes: agent edits mixed into unrelated local changes; no stable base for review; subagents overwriting each other because ownership was not assigned.

## 07 Implementation Plan

Purpose: convert approved requirements into testable, bite-sized tasks.

Plan requirements:

- Every task has exact files.
- Every task maps to requirements or maintenance rationale (rows in the Requirement Traceability Matrix — one schema, defined once below).
- Every behavior task starts with tests; test commands include expected red and green outcomes when practical.
- Every task has a commit boundary unless the work is too small for that to be useful.

Task template:

```markdown
### TASK-001: <Name>

**Requirements:** REQ-001

**Files:**
- Modify: `src/example.ts`
- Test: `tests/example.test.ts`

- [ ] Write failing test for AC-001.
- [ ] Run test and confirm expected failure.
- [ ] Implement minimal code.
- [ ] Run focused test and confirm pass.
- [ ] Run required regression checks.
- [ ] Update the traceability matrix row.
- [ ] Commit with message `<type>: <summary>`.
```

Exit evidence: plan self-review passes; no placeholders (`TBD`, "add appropriate tests", "handle edge cases"); requirement coverage complete in the matrix.

Failure modes: plan too vague for another agent to execute; "write tests later"; plan requiring hidden context from the controller's chat.

## 08 Execution

Purpose: do the planned work while preserving ownership and evidence.

Execution modes:

| Mode | Use When | Accountability Controls |
| --- | --- | --- |
| Inline execution | T0-T2, tightly coupled changes | Task checklist, focused commits, verification ledger |
| Subagent-driven | Approved plan with independent tasks | Packet contract, disjoint write scopes, structured results, fresh reviewers (`orchestration.md`) |
| Autonomous loop | T3, 10+ mechanical tasks, low remaining design uncertainty | Stop conditions, circuit breakers, budget caps (`orchestration.md`) |

Rules:

- Multi-agent fan-out is for discovery, review, and verification by default; authoring stays single-agent unless tasks are genuinely independent with disjoint write scopes.
- Route mechanical packets to cheaper models; keep orchestration, design, integration, and verification on the strongest model (`orchestration.md`).
- The controller checks worker claims against diffs and command output before integrating.
- TDD for behavior changes: write failing test -> see correct failure -> minimal implementation -> see pass -> refactor while green.

Exit evidence: task checklist updates, test red/green evidence, diff or commit evidence, packet results.

Failure modes: code before tests for behavior changes; trusting subagent success claims without checking; parallel agents touching the same files.

## 09 Integration

Purpose: decide what to accept, reject, or revise from each work packet.

```markdown
## Integration
| Packet | Result | Decision | Reason | Follow-Up |
| --- | --- | --- | --- | --- |
| 01-discovery | Found existing auth middleware | Accepted | Authoritative source verified | Scope adjusted |
| 02-ui | Added form changes | Revise | Missing AC-004 | Send back to worker |
```

Rules:

- If two packets disagree, inspect the authoritative source.
- Accepted findings must map to source evidence; rejected findings must include a reason.
- Conflicts are resolved before verification.
- Update the plan or spec if discoveries changed scope.

Failure modes: combining all packet outputs as if equally true; losing conflict rationale; running final verification before integration is complete.

## 10 Verification

Purpose: prove the result against the original requirements, not against vibes.

Verification ladder:

1. Static checks for changed files.
2. Focused unit tests.
3. Integration tests for touched paths.
4. Typecheck/lint/build.
5. UI or browser smoke tests when visual behavior changed.
6. Security checks when egress, auth, secrets, or parsing changed.
7. Manual checklist for non-code deliverables.
8. Requirement-by-requirement audit.

Verification ledger — the single evidence table; final claims cite its rows:

```markdown
## Verification Ledger
| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-001 | REQ-001 | Unit test | `npm test -- auth.test.ts` | pass | pass, 8/8 | pass |
| VERIFY-002 | REQ-002 | Manual doc audit | `rg "REQ-002" docs specs` | mapped | mapped in plan | pass |
```

Completion claim gate — before claiming anything is done:

1. Identify which ledger row proves the claim; add the row if missing.
2. Run or inspect the evidence fresh; read the actual output.
3. Confirm the evidence covers the full claim, not a narrow slice of it.
4. Ask whether the check could pass without the task genuinely being done (gamed tests, weakened assertions) — see the reward-hack check in `orchestration.md`.
5. Report skipped checks honestly.

No final claim is stronger than its ledger row.

Failure modes: "tests pass" based on an old run; a narrow test supporting a broad claim; treating review comments as proof; ignoring skipped checks.

## 11 Review

Purpose: catch spec drift and implementation defects before the work is considered ready.

Review stages:

1. Spec compliance review: did the work implement exactly the approved requirements?
2. Code quality review: is the implementation maintainable, simple, and consistent?
3. Risk review: did the work introduce security, reliability, data, or operational hazards?
4. Human review: required before merge, PR, external publishing, or irreversible operations.

For T2+, reviews come from a fresh context, not the author: dispatch a reviewer agent that receives the spec, the diff, and the verification commands — not the author's reasoning. When no subagent runner exists, state explicitly that the review is self-review and weight it accordingly.

Simplicity gate:

- Does the needed behavior already exist in the repo before writing new code?
- Can stdlib, native platform APIs, or an already installed dependency solve it?
- Is the custom code the smallest safe diff that preserves correctness, security, tests, and user scope?
- Did the change avoid new dependencies, MCP tools, generated code, or external repos unless the user approved the added setup?

```markdown
## Review Record
| ID | Review | Reviewer | Scope | Findings | Decision |
| --- | --- | --- | --- | --- | --- |
| REVIEW-001 | Spec compliance | agent/spec-reviewer (fresh context) | TASK-001 | No gaps | Approved |
| REVIEW-002 | Code quality | agent/quality-reviewer (fresh context) | TASK-001 | Important: duplicate helper | Revise |
```

Rules: critical findings block; important findings are fixed before proceeding unless the user accepts the tradeoff; minor findings are tracked; external review feedback is evaluated against the codebase before implementation.

Failure modes: skipping review because the change is "simple"; blindly implementing review suggestions that conflict with requirements; treating self-review as independent review.

## 12 Reflection

Purpose: turn the run into future leverage without polluting always-loaded context.

```markdown
# Reflection: <Run Name>

## Session Summary
- Tasks completed / requiring rework:
- Plan regenerations / spec updates:

## What Worked

## Friction Points and Root Causes

## Instruction Updates (AGENTS.md / OPS.md)

## Cross-Project Learnings

## Follow-Up Tasks
```

What goes where:

| Learning Type | Destination |
| --- | --- |
| Project commands and validation | `OPS.md` (or the repo's operational guide) |
| Live task status | the tier's canonical state file only |
| Design rationale | `docs/decisions/*` |
| Completed run summary | `.workflow/<slug>/final-report.md` or archive |
| Cross-project pattern | `~/AI_RETRO.md` |
| Bulky history | archive files, never always-loaded instructions |

Rules: keep always-loaded files short; add only knowledge that will change future behavior; archive stale notes; be honest about failures and rework.

Failure modes: "everything went well" reflections; bloated bootloaders that load status history every session; cross-project memory filled with project trivia.

## 13 Archive

Purpose: close the loop and make the run discoverable later.

```markdown
# Task Archive: <Task Name>

## Metadata
| Field | Value |
| --- | --- |
| Task ID / Tier / Dates | |
| Base SHA / Final SHA | |

## Summary

## Requirements and Decisions

## Verification

## Reviews

## Lessons Learned

## References
```

The archive links the spec, plan, decision docs, run directory, verification ledger, commits or PR, and reflection. Mark the task complete in the canonical state file.

Failure modes: completed tasks lingering as active; archives without verification evidence; future agents unable to find why a decision was made.

## 14 Finish

Purpose: choose what happens to the completed branch or artifact — keep, PR, merge, cherry-pick, discard, or publish.

```markdown
## Finish Checklist
- [ ] Requirement coverage audit complete.
- [ ] Verification ledger complete.
- [ ] Reviews complete or dispositions recorded.
- [ ] Reflection and archive complete (T2+/T3).
- [ ] Git status inspected.
- [ ] User-facing summary prepared.
- [ ] External action approval obtained, if needed.
```

Failure modes: merging without final verification; losing local changes because branch status was not inspected; presenting a PR as ready when checks were skipped.

## Requirement Traceability Matrix

The single canonical row schema for T2+ accountability. The implementation plan, verification, and review phases all update rows in this one matrix — do not maintain parallel variants.

```markdown
| Req | AC | Decision | Task | Code/Diff | Verification | Review | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | AC-001 | DEC-001 | TASK-001 | commit abc123 | VERIFY-001 | REVIEW-001 | done |
```

Status values: `proposed`, `approved`, `planned`, `in_progress`, `implemented`, `verified`, `reviewed`, `done`, `blocked`, `deferred`, `rejected`.

## Deterministic Gates

Agent self-discipline is the floor, not the ceiling. Where the harness supports it, convert "the agent should" into "the harness enforces":

- Hooks: a pre-commit or pre-stop hook that blocks completion while required checks fail, or blocks committing T2+ work with no verification evidence present.
- CI as backpressure: autonomous loops and subagent output must pass the same CI gates as human work; a loop that cannot make CI green stops and surfaces the state instead of arguing with the gate.
- Scripts over prose for fragile steps: when a step must happen exactly one way (run-directory validation, migrations), ship a script and run it rather than restating instructions each time.
- Permission modes: keep destructive and external-mutation actions behind approval prompts; never widen permissions to make a loop run smoother.

Deterministic gates do not replace review or verification; they make skipping them impossible rather than merely discouraged.

For Claude Code repos, the skill ships ready-made gates — a deterministic stop-gate hook, an optional learning gate, and focused subagents — installable via `init_agents.py --claude-kit`; see `claude-code-kit.md`.

## Autonomous Loop Policy

Use autonomous loops (Ralph-style) only when the spec and plan are strong enough that execution is mostly mechanical.

Good fit: 10+ well-defined tasks; strong acceptance criteria; low remaining design uncertainty; tests or checks provide backpressure; a sandbox or disposable branch is available.

Poor fit: the user is still exploring what they want; architecture or UX decisions remain open; fewer than five implementation tasks; the run would touch secrets, production, or external systems without approval; the repo cannot tolerate autonomous broad edits.

Loop safety:

- Use a sandbox or isolated worktree; save raw logs to `logs/`; keep the plan current.
- Design each iteration to tolerate a fresh context: progress lives in git and the state files, not the loop's memory.
- Apply the stop conditions in `orchestration.md`: machine-checkable success gate, repeated-failure circuit breaker, budget cap, and forced checkpoint before irreversible actions.
- Run reflection after the loop. Never use loop output as final proof without an independent fresh-context verification pass.

## Memory Hygiene

Always-loaded files are expensive. They contain durable instructions, not diaries.

- Keep short: `AGENTS.md`, `CLAUDE.md`, `OPS.md`, project rules.
- Live status: the tier's canonical state file only (see State Ownership).
- History: archives, final reports, reflection docs.
- Cross-project memory (`~/AI_RETRO.md`): a user-owned markdown file, one bullet per pattern that applies beyond one repo, created on first use; archive one-off notes rather than letting them accumulate.

## Minimal Workflow by Tier

T0:

```text
Inspect -> act -> verify if claiming -> final answer
```

T1:

```text
Inspect instructions -> durable goal note -> edit -> focused verification -> summary
```

T2:

```text
Intake -> context -> spec -> plan -> optional creative -> branch -> TDD execution -> verification -> fresh-context review -> reflection
```

T3:

```text
Intake -> context -> spec -> creative -> .workflow orchestration -> isolated worktree ->
implementation plan -> packets/subagents or loop -> integration -> verification ->
fresh-context reviews -> reflection -> archive -> finish
```

## Adoption Plan

To add this workflow to a repo:

1. Run `scripts/init_agents.py` to generate the bootloader and `OPS.md`.
2. Add `specs/` and `docs/decisions/` when the first T2 task appears.
3. Create `.workflow/<slug>/` when the first T3 run starts; validate it with `scripts/verify_run.py`.
4. Add `logs/` to `.gitignore`.
5. Add loop scaffolding (`loop.sh`, `prompts/`) only for projects that will actually run autonomous loops.
6. Run a small dry-run task end to end and archive it to validate the process.

## Anti-Patterns

- Applying T3 ceremony to a typo fix.
- Skipping spec approval for architecture work.
- Treating generated plans as proof of completion.
- Accepting subagent reports without diff and verification checks.
- Running a loop while design decisions are still open.
- Putting task status history in always-loaded instruction files.
- Creating artifacts that no later phase reads.
- Maintaining parallel state files that can disagree instead of one canonical owner with projections.
- Making final claims without a fresh verification ledger row.
- Fan-out for work one agent could do, or for tightly coupled authoring.
- Self-review presented as independent review.
- Updating cross-project memory with one-off project details.

## Final Accountability Standard

A run is complete only when all of the following are true:

- The original goal is preserved and satisfied, or unsatisfied parts are explicitly deferred by the user.
- Every requirement has an acceptance criterion, and every acceptance criterion has verification evidence.
- Every risky action has approval evidence.
- Every design decision has rationale and rejected alternatives.
- Every packet has an integration decision.
- Every review finding has a disposition.
- Reflection captured useful learning; the archive links the important artifacts.
- The final answer states only what the evidence supports.
