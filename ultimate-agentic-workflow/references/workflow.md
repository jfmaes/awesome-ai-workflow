# Ultimate Traceability Agentic Workflow

The goal is not maximum ceremony. The goal is maximum accountability at the minimum useful ceremony for the task's risk. T0/T1 work skips this file entirely (see the Fast Path in SKILL.md); the machinery below is for T2, and most of the heavy artifacts are T3-only.

Where a Superpowers skill owns a phase's mechanics, this file states only the UAW delta — tier gates and required artifacts — and defers everything else to that skill.

## Contents

Core Contract · Traceability Invariants · State Ownership · Repository Layout · Tier Model · Lifecycle Phases 00-14 · Requirement Traceability Matrix (T3) · Deterministic Gates (T3) · Autonomous Loop Policy · Memory Hygiene · Minimal Workflow by Tier · Anti-Patterns · Final Accountability Standard

Related references, loaded on demand:

- `orchestration.md`: subagents, fan-out sizing, packet contract, verification patterns, loop stop conditions.
- `context-engineering.md`: context budget, durable notes, compaction survival, subagent isolation.
- `large-codebase.md`: search routing, tool readiness, permission-gated setup.
- `pilot-measurement.md`: measuring acceleration tools before trusting them.

## Core Contract

Every non-trivial agent run must leave behind enough evidence that another agent or human can answer: what was requested and assumed; what sources were inspected; what decisions were made and what alternatives were rejected; what exact work was planned and who owned each packet; what changed and what proved the result; what remains unresolved and what future sessions should remember. If the record cannot answer those questions, the run is not accountable.

## Traceability Invariants

These invariants apply to T2+; the full ID discipline (stable `REQ-001`, `AC-001`, `DEC-001`, `TASK-001`, `VERIFY-001`, `REVIEW-001` identifiers) is required at T3:

- One source of truth per concern; other files are projections or history (see State Ownership).
- Every acceptance criterion maps to at least one verification check.
- Every design decision records considered alternatives and rationale.
- Every final claim cites fresh evidence: no claim stronger than a verification ledger row.
- Every subagent packet has an owner, scope, constraints, expected output, and integration decision.
- Every risky action has an approval record before execution.

## State Ownership

Exactly one file owns live task state at any time. Everything else is a projection or historical record. Drift between state files is a process failure.

| Tier | Canonical live state | Projections / history |
| --- | --- | --- |
| T0 | none (the final answer is the record) | — |
| T1 | none by default; a one-line goal note only if the work could span a compaction | — |
| T2 | the implementation plan (`IMPLEMENTATION_PLAN.md`) | `memory-bank/tasks.md` mirrors it if the repo uses that pattern |
| T3 | `.workflow/<slug>/state.json` | `plan.md` is the human-readable view; `memory-bank/*` and `IMPLEMENTATION_PLAN.md` are projections |

Update the canonical file first; sync projections after, or mark them stale. After compaction or session resume, re-anchor from the canonical file before acting (see `context-engineering.md`).

## Repository Layout

Create directories when a tier first requires them, not upfront:

```text
project/
|-- AGENTS.md or CLAUDE.md      # bootloader (short, always loaded)
|-- OPS.md                      # operational guide: commands, validation, durable lessons
|-- IMPLEMENTATION_PLAN.md      # only while T2+ work is active
|-- specs/<topic>.md            # T2+ specs
|-- docs/decisions/             # design decision records
|-- .workflow/<run-slug>/       # T3 run evidence
|-- logs/                       # gitignored raw logs
`-- src/
```

`memory-bank/` and `prompts/` + `loop.sh` are compatibility patterns, used only where the target repo already adopted them. `.workflow/<run-slug>/` is committed only when it contains useful audit artifacts rather than bulky transcripts.

## Tier Model

Assess the tier at intake; the user can override it.

| Tier | Use When | Required Artifacts | Normal Flow |
| --- | --- | --- | --- |
| T0: Just Do It | One answer, one obvious edit, low risk, easy rollback | None beyond the answer or tiny diff | Do the work; verify if a claim is made |
| T1: Think Aloud | One to three files, clear intent, modest risk | Command evidence if edited; goal note only if spanning compaction | Inspect -> act -> verify -> summarize |
| T2: Spec and Plan | Multi-file change, design choices, other contributors affected | Spec, implementation plan | Intake -> plan -> optional creative -> build -> verify -> review -> reflect |
| T3: Full Accountable Loop | Architecture, migration, high risk, multi-session, 10+ tasks, loop or swarm candidate | `.workflow/<slug>/`, spec, plan, risk gates, packet results, verification ledger, reflection/archive | Full lifecycle below |

Escalate the tier when any of these are true:

- The task touches security, payments, production data, user accounts, secrets, migrations, deployment, or public publishing.
- The agent would need broad edits, destructive commands, or long-running expensive jobs.
- Requirements are ambiguous or conflict, or verification needs multiple layers beyond unit tests.
- The user asks for a loop, swarm, subagents, or sustained autonomous execution.

De-escalate only when the user explicitly asks for a quick fix and the risk is genuinely low. Ceremony maps to fragility: low tiers get judgment and prose; high tiers get exact artifacts, gates, and scripts. Do not apply T3 ceremony to T1 work.

## Lifecycle Overview

Phases 00-14 follow in order: Intake, Context Hydration, Scope and Risk Gate, Spec, Creative Design, Orchestration Plan, Isolation, Implementation Plan, Execution, Integration, Verification, Review, Reflection, Archive, Finish. Lower tiers skip phases per the Minimal Workflow by Tier section.

## 00 Intake

Restate the goal in one sentence; preserve the original wording verbatim in the tier's canonical state file (T2+). Identify outcomes, non-goals, and explicit constraints ("do not run pytest"). Assign a tier and say why. Failure modes: shrinking the goal to the easiest subset; treating a vague request as implementation-ready; losing the original request to compaction.

## 01 Context Hydration

Load only what the tier needs (full policy: `context-engineering.md`). T2-T3: read specs, active plans, recent commits, and relevant source; search for existing implementation before assuming a gap. Use the cheapest reliable retrieval mode first — exact text (`rg`), then symbol, structural, semantic; the routing table lives in `large-codebase.md`. T3 exit evidence: a Source Ledger table (Source | Why Read | Findings | Used For).

## 02 Scope and Risk Gate

Decide whether work can proceed without additional approval. Approval is required before:

- deleting, overwriting, mass-renaming, force-pushing, or rewriting history
- deploying, publishing, emailing, posting, or mutating external systems
- running database migrations, broad codemods, or dependency upgrades
- touching credentials, secrets, billing, production data, user accounts, or private customer data
- spawning many agents, running expensive jobs, or editing outside the requested workspace

Safe without extra approval: reading local files in the workspace; drafting specs, plans, packets, and local workflow artifacts; narrow tests, linters, typechecks, builds, dry runs; non-destructive `.workflow/` directories. T3 exit evidence: a Risk Register table (Risk | Approval Required | Mitigation | Status). Never bury several risky actions in one broad approval.

## 03 Spec

T2 minimum spec: Goal, Non-Goals, Requirements table (stable IDs), Acceptance Criteria table (each mapped to a verification), Constraints, Open Questions. Acceptance criteria describe observable behavior, not implementation. Unknowns are marked `OPEN_QUESTION`, not silently guessed. Specs are approved before implementation for T2+ unless the user explicitly chooses a lower-ceremony path; requirements discovered during implementation are added back to the spec.

## 04 Creative Design

Mechanics: `superpowers:brainstorming`. UAW delta: when real alternatives exist and reversal is expensive, record the outcome as `docs/decisions/DEC-<id>-<name>.md` with options, decision, rationale, and discarded alternatives; wide solution spaces can use a judge panel over independent candidates (`orchestration.md`). "We chose X" without why, or without the rejected alternatives, fails review.

## 05 Orchestration Plan

T3 only: create the run-level accountability shell. Subagent mechanics live in `orchestration.md`.

```text
.workflow/<run-slug>/
|-- plan.md          # human source of truth: Goal, Success Criteria, Constraints,
|                    # Risks, Approval Required, Work Packets, Integration Policy, Verification
|-- state.json       # canonical machine state: goal, success_criteria, constraints, risks,
|                    # agent caps, packets (id/objective/ownership/status), verification checks
|-- orchestration.md # dispatch decisions
|-- packets/  results/  final-report.md
```

Before execution, validate the run directory — it enforces the exact schema:

```bash
python3 <skill-dir>/scripts/verify_run.py --run-dir .workflow/<run-slug>
```

Failure modes: orchestration that does not drive actual work; `state.json` drifting from `plan.md`; results dumped without integration decisions.

## 06 Isolation

Mechanics: `superpowers:using-git-worktrees`. UAW delta (T2+ code work): record an Isolation Record — base branch, work branch, base SHA, initial status, baseline checks — before editing. Never revert user changes unrelated to the task; if the workspace is dirty, distinguish user changes from agent changes; do not start implementation on `main` unless the user explicitly accepts that risk.

## 07 Implementation Plan

Mechanics: `superpowers:writing-plans`. UAW delta: every task has exact files and maps back to requirement IDs or explicit maintenance rationale (T3: rows in the Requirement Traceability Matrix); behavior tasks start with tests and state expected red/green outcomes; tasks get commit boundaries unless too small to be useful. Exit gate: no placeholders (`TBD`, "add appropriate tests", "handle edge cases"); another agent could execute the plan without the author's chat context.

## 08 Execution

Mechanics: `superpowers:executing-plans`, `superpowers:subagent-driven-development`, `superpowers:test-driven-development`. UAW delta — pick the execution mode and its accountability controls:

| Mode | Use When | Accountability Controls |
| --- | --- | --- |
| Inline execution | T0-T2, tightly coupled changes | Task checklist, focused commits, verification ledger |
| Subagent-driven | Approved plan with independent tasks | Packet contract, disjoint write scopes, structured results, fresh reviewers (`orchestration.md`) |
| Autonomous loop | T3, 10+ mechanical tasks, low remaining design uncertainty | Stop conditions, circuit breakers, budget caps (`orchestration.md`) |

Multi-agent fan-out is for discovery, review, and verification by default; authoring stays single-agent unless tasks are genuinely independent with disjoint write scopes. Route mechanical packets to cheaper models; keep orchestration, design, integration, and verification on the strongest model. The controller checks worker claims against diffs and command output before integrating.

## 09 Integration

T3 / multi-agent only: record an Integration table (Packet | Result | Decision | Reason | Follow-Up). If two packets disagree, inspect the authoritative source; rejected findings include a reason; conflicts are resolved before final verification; update the plan or spec if discoveries changed scope.

## 10 Verification

Mechanics: `superpowers:verification-before-completion` — evidence before assertions, always. UAW delta: T2+ runs keep a single verification ledger, and final claims cite its rows.

```markdown
## Verification Ledger
| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-001 | REQ-001 | Unit test | `npm test -- auth.test.ts` | pass | pass, 8/8 | pass |
```

Completion claim gate — before claiming anything is done:

1. Identify which ledger row proves the claim; add the row if missing.
2. Run or inspect the evidence fresh; read the actual output.
3. Confirm the evidence covers the full claim, and ask whether the check could pass without the task genuinely being done (gamed tests, weakened assertions — see the reward-hack check in `orchestration.md`).
4. Report skipped checks honestly.

No final claim is stronger than its ledger row.

## 11 Review

Mechanics: `superpowers:requesting-code-review` and `superpowers:receiving-code-review`. UAW delta: for T2+, review comes from a fresh context, not the author — the reviewer gets the spec, the diff, and the verification commands, not the author's reasoning. When no subagent runner exists, label the review as self-review and weight it accordingly. Human review is required before merge, PR, external publishing, or irreversible operations. Critical findings block; important findings are fixed unless the user accepts the tradeoff; minor findings are tracked.

Simplicity gate:

- Does the needed behavior already exist in the repo before writing new code?
- Can stdlib, native platform APIs, or an already installed dependency solve it?
- Is the custom code the smallest safe diff that preserves correctness, security, tests, and user scope?
- Did the change avoid new dependencies, MCP tools, generated code, or external repos unless the user approved the added setup?

T3 exit evidence: a Review Record table (ID | Review | Reviewer | Scope | Findings | Decision).

## 12 Reflection

T2+: capture only learning that will change future behavior. Destinations: project commands and validation -> `OPS.md`; live status -> the canonical state file only; design rationale -> `docs/decisions/*`; completed run summary -> `.workflow/<slug>/final-report.md`; cross-project patterns -> `~/AI_RETRO.md`; bulky history -> archives, never always-loaded instructions. Be honest about failures and rework; "everything went well" reflections are a failure mode.

## 13 Archive

T3: write a task archive linking the spec, plan, decision docs, run directory, verification ledger, commits or PR, and reflection; record base and final SHAs; mark the task complete in the canonical state file. Completed tasks lingering as active is a process failure.

## 14 Finish

Mechanics: `superpowers:finishing-a-development-branch` — keep, PR, merge, cherry-pick, discard, or publish. UAW delta before choosing:

- Requirement coverage audit and verification ledger complete; reviews complete or dispositions recorded.
- Reflection and archive complete (T3); git status inspected; external-action approval obtained if needed.
- If this work executed a plan document: close it now — `plan-close <plan> --status complete --commit` (or `plan-supersede <old> --by <new>` when a new plan replaces it). A finished task with an open plan file is not finished.

## Requirement Traceability Matrix

T3 only. The single canonical row schema for full accountability; the plan, verification, and review phases all update rows in this one matrix — do not maintain parallel variants.

```markdown
| Req | AC | Decision | Task | Code/Diff | Verification | Review | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | AC-001 | DEC-001 | TASK-001 | commit abc123 | VERIFY-001 | REVIEW-001 | done |
```

Status values: `proposed`, `approved`, `planned`, `in_progress`, `implemented`, `verified`, `reviewed`, `done`, `blocked`, `deferred`, `rejected`.

## Deterministic Gates

T3 only (and any repo that opts in via the installed kit). Agent self-discipline is the floor, not the ceiling — where the harness supports it, convert "the agent should" into "the harness enforces":

- Hooks: a pre-commit or pre-stop hook that blocks completion while required checks fail or verification evidence is missing.
- CI as backpressure: loops and subagent output pass the same CI gates as human work; a loop that cannot make CI green stops and surfaces the state instead of arguing with the gate.
- Scripts over prose for fragile steps (run-directory validation, migrations): ship a script and run it.
- Permission modes: keep destructive and external-mutation actions behind approval prompts; never widen permissions to make a loop run smoother.

Deterministic gates do not replace review or verification; they make skipping them impossible rather than merely discouraged. For Claude Code repos the kit ships ready-made gates via `init_agents.py --claude-kit`; see `claude-code-kit.md`.

## Autonomous Loop Policy

Use autonomous loops (Ralph-style) only when the spec and plan are strong enough that execution is mostly mechanical: 10+ well-defined tasks, strong acceptance criteria, low design uncertainty, tests as backpressure, a sandbox or disposable branch. Poor fit: the user is still exploring; architecture or UX decisions remain open; fewer than five tasks; secrets, production, or external systems without approval.

Loop safety: isolated worktree; raw logs to `logs/`; each iteration tolerates a fresh context (progress lives in git and the state files, not the loop's memory); apply the stop conditions in `orchestration.md` — machine-checkable success gate, repeated-failure circuit breaker, budget cap, forced checkpoint before irreversible actions. Never use loop output as final proof without an independent fresh-context verification pass.

## Memory Hygiene

Always-loaded files are expensive: they contain durable instructions, not diaries. Keep `AGENTS.md`, `CLAUDE.md`, and `OPS.md` short; live status goes only in the tier's canonical state file; history goes in archives. Cross-project memory (`~/AI_RETRO.md`) gets one bullet per pattern that applies beyond one repo — archive one-off notes rather than letting them accumulate.

## Minimal Workflow by Tier

T0:

```text
Inspect -> act -> verify if claiming -> final answer
```

T1:

```text
Inspect instructions -> edit -> focused verification -> summary
(add a one-line goal note only if the work could span a compaction)
```

T2:

```text
Intake -> context -> spec -> plan -> optional creative -> branch -> TDD execution ->
verification -> fresh-context review -> reflection
```

T3:

```text
Intake -> context -> spec -> creative -> .workflow orchestration -> isolated worktree ->
implementation plan -> packets/subagents or loop -> integration -> verification ->
fresh-context reviews -> reflection -> archive -> finish
```

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

A run is complete only when: the original goal is preserved and satisfied, or unsatisfied parts are explicitly deferred by the user; every acceptance criterion has verification evidence; every risky action has approval evidence; every design decision has rationale and rejected alternatives; every packet has an integration decision; every review finding has a disposition; and the final answer states only what the evidence supports.
