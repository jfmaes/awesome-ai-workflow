# Ultimate Traceability Agentic Workflow

This workflow combines the strongest parts of:

- Cursor Memory Bank: command phases, persistent task memory, adaptive complexity, progressive rule loading, creative decision records, reflection, and archive.
- Superpowers: mandatory skill-trigger discipline, brainstorming before implementation, worktree isolation, TDD, subagent-driven development, code review gates, and verification before completion.
- awesome-ai-workflow: T0-T3 ceremony scaling, Ralph-style autonomous loops, project bootstrap templates, AI_RETRO cross-project learning, and explicit prompt modes.
- DannyMac180 skills: workflow run directories, machine-readable orchestration state, risk gates, packet ownership, integration policy, and verification scripts.

The design goal is not maximum ceremony. The goal is maximum accountability at the minimum useful ceremony for the task's risk.

## Evidence Snapshot

This synthesis is based on the current local checkouts and a fresh clone of the external skills repo on 2026-05-31.

| Source | Evidence Read |
| --- | --- |
| `cursor-memory-bank` | `README.md`, `COMMANDS_README.md`, `MEMORY_BANK_OPTIMIZATIONS.md`, `.cursor/commands/{van,plan,creative,build,reflect,archive}.md`, `.cursor/rules/isolation_rules/main.mdc`, `creative_mode_think_tool.md`, `optimization-journey/11-methodological-integration.md` |
| `../superpowers` | `README.md`, `AGENTS.md`, `skills/{brainstorming,writing-plans,subagent-driven-development,test-driven-development,requesting-code-review,receiving-code-review,verification-before-completion,dispatching-parallel-agents}/SKILL.md` |
| `../awesome-ai-workflow` | `README.md`, `project-init/SKILL.md`, `starter-kit/prompts/{PROMPT_plan,PROMPT_build,PROMPT_reflect}.md` |
| `https://github.com/DannyMac180/skills` | Fresh shallow clone at HEAD `5695fa19b9d39b8270025e79633b49a8b863f9a2`; `README.md`, `codex-dynamic-workflows/SKILL.md`, `references/{plan-schema,risk-gates,validation-examples}.md`, `agents/openai.yaml` |

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

- One source of truth per concern. Do not duplicate status across many files unless one file clearly owns the live state and the others are historical records.
- Requirement IDs are stable. Use IDs such as `REQ-001`, `AC-001`, `DEC-001`, `TASK-001`, `VERIFY-001`.
- Every acceptance criterion maps to at least one verification check.
- Every design decision records considered alternatives and rationale.
- Every implementation task maps back to requirements or explicit maintenance work.
- Every final claim cites fresh evidence from commands, files, tests, diffs, or review output.
- Every subagent or simulated packet has an owner, scope, constraints, expected output, and integration decision.
- Every risky action has an approval record before execution.
- Reflection updates operational knowledge only when it will affect future work.

## Repository Layout

Use this as the default layout for a project that wants the full workflow:

```text
project/
|-- AGENTS.md or CLAUDE.md
|-- OPS.md or AGENTS.md
|-- IMPLEMENTATION_PLAN.md
|-- REFLECTION.md
|-- specs/
|   |-- _TEMPLATE.md
|   `-- <topic>.md
|-- memory-bank/
|   |-- tasks.md
|   |-- activeContext.md
|   |-- progress.md
|   |-- projectbrief.md
|   |-- creative/
|   |-- reflection/
|   `-- archive/
|-- docs/
|   |-- decisions/
|   `-- superpowers/
|       |-- specs/
|       `-- plans/
|-- .workflow/
|   |-- recipes/
|   `-- <run-slug>/
|       |-- plan.md
|       |-- state.json
|       |-- orchestration.md
|       |-- packets/
|       |-- results/
|       `-- final-report.md
|-- prompts/
|   |-- PROMPT_plan.md
|   |-- PROMPT_build.md
|   |-- PROMPT_plan_work.md
|   `-- PROMPT_reflect.md
|-- logs/
`-- src/
```

Use CLI-aware instruction names:

| Purpose | Claude Code | Codex |
| --- | --- | --- |
| Project instructions | `CLAUDE.md` | `AGENTS.md` |
| Operational guide | `AGENTS.md` | `OPS.md` |

`logs/` should usually be gitignored. `.workflow/<run-slug>/` should be committed only when it contains useful audit artifacts rather than bulky transcripts.

## What Each System Contributes

| Source | Keep | Adaptation |
| --- | --- | --- |
| Cursor Memory Bank | `/van -> /plan -> /creative -> /build -> /reflect -> /archive`; `tasks.md` as active source of truth; adaptive levels; creative decision docs; reflection/archive | Use Memory Bank as the live task memory and lifecycle record, not as a replacement for specs, plans, or verification evidence |
| Superpowers | Skill-trigger discipline; brainstorming and approval before implementation; worktree isolation; TDD; fresh subagent per task; spec review then code quality review; verification before completion | Treat Superpowers as the behavior contract for agents and reviewers |
| awesome-ai-workflow | T0-T3 ceremony scaling; Ralph loop for large batches; `AI_RETRO.md`; project-init templates; prompt modes; cross-project learning | Use the tier model to decide how much of the lifecycle is required |
| DannyMac180 skills | `.workflow/<slug>/` run directory; `state.json`; packet schema; approval gates; integration policy; verification artifact checks | Use this as the orchestration and accountability ledger, especially for multi-agent or multi-track runs |

## Tier Model

The workflow uses a merged tier model. The tier is assessed at intake and can be overridden by the user.

| Tier | Cursor Memory Bank Level | Use When | Required Artifacts | Normal Flow |
| --- | --- | --- | --- | --- |
| T0: Just Do It | Level 1 subset | One answer, one obvious edit, low risk, easy rollback | None beyond final answer or tiny diff | Do the work, verify if a claim is made |
| T1: Think Aloud | Level 1 | One to three files, clear intent, modest risk | Short approach note; command evidence if edited | Inspect -> act -> verify -> summarize |
| T2: Spec and Plan | Level 2-3 | Multi-file change, design choices, other contributors affected | `specs/<topic>.md`, `IMPLEMENTATION_PLAN.md` or `docs/superpowers/plans/*`, `memory-bank/tasks.md` | Intake -> plan -> optional creative -> build -> verify -> reflect |
| T3: Full Accountable Loop | Level 4 | Architecture, migration, high risk, multi-session, 10+ tasks, autonomous loop candidate | Full repo layout, `.workflow/<slug>/`, specs, plan, risk gates, packet results, verification ledger, reflection/archive | Intake -> spec -> creative -> orchestration -> isolated execution -> reviews -> verification -> archive -> memory update |

Escalate the tier when any of these are true:

- The task touches security, payments, production data, user accounts, secrets, migrations, deployment, or public publishing.
- The agent would need broad edits, destructive commands, or long-running expensive jobs.
- Requirements are ambiguous or conflict.
- Verification requires multiple layers beyond unit tests.
- The user asks for a loop, swarm, subagents, or sustained autonomous execution.

De-escalate only when the user explicitly asks for a quick fix and the risk is genuinely low.

## Lifecycle Overview

```text
00 Intake
01 Context Hydration
02 Scope and Risk Gate
03 Spec
04 Creative Design
05 Orchestration Plan
06 Isolation
07 Implementation Plan
08 Execution
09 Integration
10 Verification
11 Review
12 Reflection
13 Archive
14 Finish
```

Each phase below lists entry criteria, required actions, exit evidence, and failure modes.

## 00 Intake

Purpose: convert the user's request into a tracked goal without losing the original wording.

Actions:

- Restate the goal in one sentence.
- Preserve the original objective verbatim in `memory-bank/tasks.md` or `.workflow/<slug>/plan.md` for T2+.
- Identify stakeholders, user-visible outcomes, and non-goals.
- Assign a tier and explain why.
- Record explicit constraints, such as "do not run pytest" or "static review only".

Exit evidence:

- Goal statement.
- Tier decision.
- Initial success criteria.
- Known constraints.

Failure modes:

- The agent shrinks the goal to the easiest subset.
- The agent treats a vague request as implementation-ready.
- The original request is lost after context compaction.

## 01 Context Hydration

Purpose: load only the context needed for the current tier.

T0-T1:

- Read nearby instructions such as `AGENTS.md`, `CLAUDE.md`, `OPS.md`, `README.md`.
- Inspect directly relevant files.

T2-T3:

- Read project instructions.
- Read specs, Memory Bank files, active plans, recent commits, and relevant source files.
- Search for existing implementation before assuming a gap.
- Load cross-project memory selectively, such as `AI_RETRO.md` rules and the matching stack section.

Context loading policy:

- Prefer progressive rule loading from Cursor Memory Bank: core first, mode-specific next, specialized only when needed.
- Prefer local repo evidence over assistant memory.
- Prefer primary source docs for external APIs.
- Record sources read in a source ledger for T2+.

Search routing policy:

| Need | Tool | Trigger Signal |
| --- | --- | --- |
| Known string / literal / fast scan | `rg` | You roughly know the text, filename, error, route, config key, or symbol. |
| Definition, references, callers, or safe rename | LSP/code-intelligence tools such as Serena | You need symbol graph facts across files. |
| Structural pattern | `ast-grep`, tree-sitter, or a language parser | Code shape matters more than exact text. |
| Fuzzy concept | semantic search such as grepai | Exact text, symbol, and structural searches failed. Use as a last resort. |

For large or unfamiliar codebases, read `references/large-codebase.md` before adding MCP/search tools or cloning dependent repos.
If large-codebase signals are present, run `python3 ultimate-agentic-workflow/scripts/large_codebase_tools.py --project-root . --json` to check tool readiness and generate approval text before installing Serena or related tools.

Exit evidence:

```markdown
## Source Ledger
| Source | Why Read | Findings | Used For |
| --- | --- | --- | --- |
| `AGENTS.md` | Project instructions | Test command is `npm test` | Verification plan |
| `src/auth/*` | Existing auth flow | Session middleware exists | Scope decision |
```

Failure modes:

- Reading everything and wasting context.
- Reading too little and duplicating existing work.
- Using stale memory as if it were current evidence.

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

Exit evidence:

```markdown
## Risk Register
| Risk | Approval Required | Mitigation | Status |
| --- | --- | --- | --- |
| Broad codemod across API clients | Yes | Draft exact command first | Pending approval |
| Unit test run | No | Narrow command, local only | Approved by policy |
```

Failure modes:

- Burying several risky actions in one broad approval.
- Treating "agentic" as permission for external mutation.
- Running destructive commands because they are reversible in theory.

## 03 Spec

Purpose: establish what must be true before planning implementation.

T2 minimum spec:

```markdown
# <Topic> Spec

## Goal

## Jobs To Be Done

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
- Unknowns are marked as `OPEN_QUESTION`, not silently guessed.
- Requirement IDs are stable for the rest of the run.
- Specs are approved before implementation for T2+ unless the user explicitly chooses a lower-ceremony path.

Exit evidence:

- Approved spec or user-approved inline equivalent.
- Requirement and acceptance criterion IDs.

Failure modes:

- A plan that contains requirements not present in the spec.
- Acceptance criteria with no verification path.
- Hidden requirements discovered during implementation but never added back to the spec.

## 04 Creative Design

Purpose: make major design choices explicit before code exists.

Use this phase when:

- architecture, UX, algorithms, data models, or operational strategy have real alternatives
- the wrong choice is expensive to reverse
- multiple agents need one shared design decision

Template:

```markdown
# Design Decision: DEC-001 <Name>

## Problem

## Requirements
- REQ-001

## Options
| Option | Summary | Strengths | Weaknesses | Risk |
| --- | --- | --- | --- | --- |
| A | ... | ... | ... | ... |
| B | ... | ... | ... | ... |

## Decision

## Rationale

## Discarded Alternatives

## Implementation Guidance

## Verification Impact
```

Store decisions in one of:

- `memory-bank/creative/creative-<feature>.md`
- `docs/decisions/DEC-001-<name>.md`
- `docs/superpowers/specs/<date>-<topic>-design.md`

Exit evidence:

- Decision document with alternatives and rationale.
- Design-to-requirement mapping.

Failure modes:

- "We chose X" without why.
- No record of rejected alternatives.
- A later implementer reopens the same decision because it was not discoverable.

## 05 Orchestration Plan

Purpose: create a run-level accountability shell for T3 and multi-agent work.

Create:

```text
.workflow/<run-slug>/
|-- plan.md
|-- state.json
|-- orchestration.md
|-- packets/
|-- results/
`-- final-report.md
```

`plan.md` is the human source of truth:

```markdown
# Workflow Plan: <Run Name>

## Goal

## Success Criteria

## Current Context

## Constraints

## Risks

## Approval Required

## Work Packets

## Integration Policy

## Verification

## Reusable Artifacts
```

`state.json` is machine-readable coordination state:

```json
{
  "goal": "string",
  "success_criteria": ["string"],
  "constraints": ["string"],
  "risks": [
    {
      "risk": "string",
      "approval_required": true,
      "mitigation": "string"
    }
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
    {
      "check": "string",
      "command": "string or null",
      "required": true,
      "status": "pending"
    }
  ]
}
```

Use DannyMac's `verify_workflow.py` pattern to check for missing sections before execution.

Exit evidence:

- Workflow run directory.
- Packet list.
- Risk and approval state.
- Verification checklist.

Failure modes:

- Orchestration exists but does not drive actual work.
- `state.json` drifts from `plan.md`.
- Results are dumped without integration decisions.

## 06 Isolation

Purpose: protect the main workspace and make diffs attributable.

For T2+ code work:

- Prefer a git worktree or feature branch.
- Verify initial git status.
- Record base commit.
- Confirm test baseline when practical.

Template:

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

- Never revert user changes that are unrelated to the task.
- If the workspace is dirty, distinguish user changes from agent changes.
- Do not start implementation on `main` unless the user explicitly accepts that risk.

Exit evidence:

- Branch or worktree path.
- Base SHA.
- Initial status.

Failure modes:

- Agent edits mixed into unrelated local changes.
- No stable base for review.
- Subagents overwrite each other because ownership was not assigned.

## 07 Implementation Plan

Purpose: convert approved requirements into testable, bite-sized tasks.

Plan requirements:

- Every task has exact files.
- Every task maps to requirements or maintenance rationale.
- Every behavior task starts with tests.
- Every test command includes expected red and green outcomes when practical.
- Every task has a commit boundary unless the work is too small for that to be useful.

Template:

```markdown
# <Feature> Implementation Plan

> For agentic workers: execute task-by-task. Do not skip verification gates.

## Goal

## Architecture

## Traceability Matrix
| Requirement | Acceptance Criteria | Task | Verification |
| --- | --- | --- | --- |
| REQ-001 | AC-001 | TASK-001 | VERIFY-001 |

## Files
| Path | Action | Responsibility |
| --- | --- | --- |
| `src/example.ts` | Modify | TASK-001 |

### TASK-001: <Name>

**Requirements:** REQ-001

**Files:**
- Modify: `src/example.ts`
- Test: `tests/example.test.ts`

- [ ] Step 1: Write failing test for AC-001.
- [ ] Step 2: Run test and confirm expected failure.
- [ ] Step 3: Implement minimal code.
- [ ] Step 4: Run focused test and confirm pass.
- [ ] Step 5: Run required regression checks.
- [ ] Step 6: Update traceability ledger.
- [ ] Step 7: Commit with message `<type>: <summary>`.
```

Exit evidence:

- Plan self-review passes.
- No placeholders such as `TBD`, `TODO`, "add appropriate tests", or "handle edge cases".
- Requirement coverage matrix is complete.

Failure modes:

- Plan is too vague for another agent to execute.
- Test strategy is "write tests later".
- Plan requires reading hidden context from the controller's chat.

## 08 Execution

Purpose: do the planned work while preserving ownership and evidence.

Execution modes:

| Mode | Use When | Accountability Controls |
| --- | --- | --- |
| Inline execution | T0-T2, tightly coupled changes, no subagent authorization | Local checklist, focused commits, verification ledger |
| Subagent-driven execution | Approved plan with independent tasks and available subagent tools | Fresh implementer per task; spec reviewer; code quality reviewer; controller integrates |
| Simulated packet execution | No subagent runner, but independent tracks still need separation | Write packet notes under `.workflow/<slug>/results/`; integrate explicitly |
| Ralph loop | T3, 10+ clear tasks, low creativity remaining, sandbox acceptable | `loop.sh`, prompt modes, logs, plan updates, reflection |

Subagent packet template:

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

## Status
```

Rules:

- Give each worker a disjoint write scope.
- Tell workers they are not alone in the codebase.
- Workers must not revert others' edits.
- Workers must ask for context instead of guessing.
- The controller does not paste raw worker output into the final answer; it integrates results.
- Parallel implementation is allowed only when write scopes do not overlap.
- Parallel research is allowed when questions are distinct.

TDD execution rule:

```text
Write failing test -> run and see correct failure -> minimal implementation -> run and see pass -> refactor while green.
```

Exit evidence:

- Task checklist updates.
- Test red/green evidence.
- Diff or commit evidence.
- Packet results.

Failure modes:

- Agent writes code before tests for behavior changes.
- Controller trusts subagent success claims without checking.
- Parallel agents touch the same files without coordination.

## 09 Integration

Purpose: decide what to accept, reject, or revise from each work packet.

Integration report:

```markdown
## Integration
| Packet | Result | Decision | Reason | Follow-Up |
| --- | --- | --- | --- | --- |
| 01-discovery | Found existing auth middleware | Accepted | Authoritative source verified | Scope adjusted |
| 02-ui | Added form changes | Revise | Missing AC-004 | Send back to worker |

## Conflicts

## Decisions

## Final Changes

## Remaining Risks
```

Rules:

- If two packets disagree, inspect the authoritative source.
- Accepted findings must map to source evidence.
- Rejected findings must include a reason.
- Conflicts are resolved before verification.

Exit evidence:

- Integration report.
- Updated plan or spec if discoveries changed scope.

Failure modes:

- Combining all packet outputs as if they are equally true.
- Losing rejected alternatives and conflict rationale.
- Running final verification before integration is complete.

## 10 Verification

Purpose: prove the result against the original requirements, not against vibes.

Verification ladder:

1. Static checks for changed files.
2. Focused unit tests.
3. Integration tests for touched paths.
4. Typecheck/lint/build.
5. UI or browser smoke tests when visual behavior changed.
6. Security checks when egress, auth, secrets, or parsing changed.
7. Manual checklist for non-code or documentation deliverables.
8. Requirement-by-requirement audit.

Verification ledger:

```markdown
## Verification Ledger
| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-001 | REQ-001 | Unit test | `npm test -- auth.test.ts` | pass | pass, 8/8 | pass |
| VERIFY-002 | REQ-002 | Manual doc audit | `rg "REQ-002" docs specs` | mapped | mapped in plan | pass |
```

Completion claim gate:

Before claiming completion:

1. Identify what proves the claim.
2. Run or inspect the evidence fresh.
3. Read the output or file.
4. Confirm it covers the full claim.
5. Report skipped checks honestly.

Exit evidence:

- Verification ledger with statuses.
- Fresh command outputs or file references.
- Requirement coverage audit.

Failure modes:

- "Tests pass" based on an old run.
- Using a narrow test to support a broad claim.
- Treating review comments as proof.
- Ignoring skipped checks.

## 11 Review

Purpose: catch spec drift and implementation defects before the work is considered ready.

Review stages:

1. Spec compliance review: did the work implement exactly the approved requirements?
2. Code quality review: is the implementation maintainable, simple, and consistent?
3. Risk review: did the work introduce security, reliability, data, or operational hazards?
4. Human review: required before merge, PR, external publishing, or irreversible operations.

Simplicity gate:

- Check whether the needed behavior already exists in the repo before writing new code.
- Can stdlib, native platform APIs, or an already installed dependency solve it?
- Is the custom code the smallest safe diff that preserves correctness, security, tests, and user scope?
- Did the change avoid new dependencies, MCP tools, generated code, or external repos unless the user approved the added setup?

Review record:

```markdown
## Review Record
| Review | Reviewer | Scope | Findings | Decision |
| --- | --- | --- | --- | --- |
| Spec compliance | agent/spec-reviewer | TASK-001 | No gaps | Approved |
| Code quality | agent/quality-reviewer | TASK-001 | Important: duplicate helper | Revise |
```

Rules:

- Critical findings block.
- Important findings are fixed before proceeding unless the user accepts the tradeoff.
- Minor findings are tracked or fixed opportunistically.
- External review feedback is evaluated against the codebase before implementation.

Exit evidence:

- Review findings.
- Fixes or explicit dispositions.

Failure modes:

- Skipping review because the change is "simple".
- Blindly implementing review suggestions that conflict with requirements.
- Treating self-review as independent review.

## 12 Reflection

Purpose: turn the run into future leverage without polluting always-loaded context.

Reflection template:

```markdown
# Reflection: <Run Name>

## Session Summary
- Tasks completed:
- Tasks requiring rework:
- Plan regenerations:
- Spec updates:

## What Worked

## Friction Points

## Root Causes

## AGENTS.md or OPS.md Updates

## Cross-Project Learnings

## Process Improvements

## Follow-Up Tasks
```

What goes where:

| Learning Type | Destination |
| --- | --- |
| Project commands and validation | `AGENTS.md` or `OPS.md` |
| Current task status | `memory-bank/tasks.md` or `IMPLEMENTATION_PLAN.md` |
| Current focus | `memory-bank/activeContext.md` |
| Implementation observations | `memory-bank/progress.md` |
| Design rationale | `memory-bank/creative/*` or `docs/decisions/*` |
| Completed run summary | `memory-bank/archive/*` |
| Cross-project pattern | `~/AI_RETRO.md` |
| Bulky history | archive files, not always-loaded instructions |

Rules:

- Keep always-loaded project instructions short.
- Add only operational knowledge that will change future agent behavior.
- Archive stale or one-off notes.
- Be honest about failures and rework.

Exit evidence:

- Reflection document.
- Minimal instruction updates.
- Cross-project learning update when applicable.

Failure modes:

- "Everything went well" reflection with no useful learning.
- Bloated `AGENTS.md` that loads status history every session.
- Cross-project memory filled with project-specific trivia.

## 13 Archive

Purpose: close the loop and make the run discoverable later.

Archive template:

```markdown
# Task Archive: <Task Name>

## Metadata
| Field | Value |
| --- | --- |
| Task ID | |
| Tier | |
| Dates | |
| Base SHA | |
| Final SHA | |

## Summary

## Requirements

## Decisions

## Implementation

## Verification

## Reviews

## Lessons Learned

## References
```

Archive should link:

- spec
- implementation plan
- decision docs
- workflow run directory
- verification ledger
- commits or PR
- reflection

Exit evidence:

- Archive file.
- `memory-bank/tasks.md` reset or marked complete.
- `memory-bank/activeContext.md` prepared for next task.

Failure modes:

- Completed tasks linger as active.
- Archive lacks verification evidence.
- Future agents cannot find why a decision was made.

## 14 Finish

Purpose: choose what happens to the completed branch or artifact.

Options:

- Keep branch for more work.
- Open PR.
- Merge.
- Cherry-pick.
- Discard experimental work.
- Publish docs or release.

Finish checklist:

```markdown
## Finish Checklist
- [ ] Requirement coverage audit complete.
- [ ] Verification ledger complete.
- [ ] Reviews complete or dispositions recorded.
- [ ] Reflection complete.
- [ ] Archive complete.
- [ ] Git status inspected.
- [ ] User-facing summary prepared.
- [ ] External action approval obtained, if needed.
```

Exit evidence:

- Final status.
- Next action.
- No open run-critical artifacts.

Failure modes:

- Merging without final verification.
- Losing local changes because branch status was not inspected.
- Presenting a PR as ready when checks were skipped.

## Claim Ledger

Use a claim ledger for high-stakes or long-running work. It prevents agents from making broad final statements unsupported by evidence.

```markdown
## Claim Ledger
| Claim | Evidence Required | Evidence Inspected | Supported? | Notes |
| --- | --- | --- | --- | --- |
| All ACs are covered | Traceability matrix | `IMPLEMENTATION_PLAN.md` lines ... | Yes | AC-001..AC-006 mapped |
| Tests pass | Fresh test run | `npm test`, exit 0 | Yes | 42/42 passed |
| Docs updated | Diff inspection | `git diff -- docs/` | Yes | README and archive updated |
```

No final claim should be stronger than its evidence.

## Requirement Traceability Matrix

This is the central accountability artifact for T2+.

```markdown
| Req | AC | Design Decision | Task | Code/Diff | Test/Check | Review | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | AC-001 | DEC-001 | TASK-001 | commit abc123 | VERIFY-001 | REVIEW-001 | done |
```

Recommended status values:

- `proposed`
- `approved`
- `planned`
- `in_progress`
- `implemented`
- `verified`
- `reviewed`
- `done`
- `blocked`
- `deferred`
- `rejected`

## Ralph Loop Policy

Use Ralph-style loops only when the spec and plan are strong enough that execution is mostly mechanical.

Good fit:

- 10+ well-defined tasks.
- Strong acceptance criteria.
- Low remaining design uncertainty.
- Tests or checks provide backpressure.
- Sandbox or disposable branch is available.

Poor fit:

- The user is still exploring what they want.
- Architecture or UX decisions remain open.
- The task is less than five implementation tasks.
- The run would touch secrets, production, or external systems without approval.
- The repo cannot tolerate autonomous broad edits.

Loop safety:

- Use a sandbox or isolated worktree.
- Require explicit mode: `plan`, `build`, `plan-work`, `reflect`.
- Save raw logs to `logs/`.
- Keep `IMPLEMENTATION_PLAN.md` current.
- Run reflection after the loop.
- Never use loop output as final proof without independent verification.

## Memory Hygiene

Always-loaded files are expensive. They should contain durable instructions, not diaries.

Keep short:

- `AGENTS.md`
- `CLAUDE.md`
- `OPS.md`
- project rules

Use task files for live status:

- `memory-bank/tasks.md`
- `IMPLEMENTATION_PLAN.md`
- `.workflow/<slug>/state.json`

Use archives for history:

- `memory-bank/archive/*`
- `REFLECTION.md`
- `.workflow/<slug>/final-report.md`

Use cross-project memory sparingly:

- `~/AI_RETRO.md` for patterns that apply beyond one repo
- archive old or one-off memories

## Minimal Workflow by Tier

T0:

```text
Inspect -> act -> verify if claiming -> final answer
```

T1:

```text
Inspect instructions -> short approach -> edit -> focused verification -> summary
```

T2:

```text
Intake -> context -> spec -> plan -> optional creative -> branch -> TDD execution -> verification -> review -> reflection
```

T3:

```text
Intake -> context -> spec -> creative -> .workflow orchestration -> isolated branch/worktree -> implementation plan -> packets/subagents or loop -> integration -> verification -> reviews -> reflection -> archive -> finish
```

## Recommended Default for "Ultimate Agentic Experience"

For serious work, use this default:

1. Start with Memory Bank `/van` behavior: classify tier, create or update `memory-bank/tasks.md`, and set active context.
2. Use Superpowers brainstorming behavior for T2+ design: clarify, compare approaches, and obtain approval before code.
3. Write a spec with stable requirement and acceptance IDs.
4. Run Cursor Memory Bank `/creative` behavior for any material design choice.
5. Create DannyMac-style `.workflow/<slug>/` orchestration for T3 or multi-agent work.
6. Use Superpowers worktree isolation before implementation.
7. Write a Superpowers-quality implementation plan with exact files, TDD steps, and verification commands.
8. Execute inline for small work, subagent-driven for independent task plans, or Ralph loop for large mechanical batches.
9. Integrate packet results explicitly.
10. Verify requirement-by-requirement using a verification ledger.
11. Run spec compliance review before code quality review.
12. Reflect, update operational knowledge minimally, archive the run, and then choose merge/PR/keep/discard.

This gives the practical flow:

```text
VAN -> SPEC -> PLAN -> CREATIVE -> ORCHESTRATE -> ISOLATE -> BUILD -> INTEGRATE -> VERIFY -> REVIEW -> REFLECT -> ARCHIVE -> FINISH
```

## Adoption Plan

To add this workflow to a repo:

1. Add project instructions: `AGENTS.md` for Codex or `CLAUDE.md` for Claude Code.
2. Add operational guide: `OPS.md` for Codex or `AGENTS.md` for Claude Code.
3. Add `specs/_TEMPLATE.md`.
4. Add `memory-bank/` with `tasks.md`, `activeContext.md`, `progress.md`, and `projectbrief.md`.
5. Add `.workflow/recipes/ultimate-agentic-workflow.md` summarizing packet and verification rules.
6. Add `IMPLEMENTATION_PLAN.md` only when there is active T2+ work.
7. Add `loop.sh`, `prompts/`, and parser scripts only for T3 projects that will actually use Ralph loops.
8. Add `logs/` to `.gitignore`.
9. Add a short "how to run checks" section to always-loaded instructions.
10. Run a small dry-run task and archive it to validate the process.

## Anti-Patterns

- Applying T3 ceremony to a typo fix.
- Skipping spec approval for architecture work.
- Treating generated plans as proof of completion.
- Accepting subagent reports without diff and verification checks.
- Running a loop while design decisions are still open.
- Putting task status history in always-loaded instruction files.
- Creating many artifacts that are not read by later phases.
- Letting `state.json`, `IMPLEMENTATION_PLAN.md`, and `memory-bank/tasks.md` disagree.
- Making final claims without a claim ledger or fresh verification.
- Updating cross-project memory with one-off project details.

## Final Accountability Standard

A run is complete only when all of the following are true:

- The original goal is preserved and satisfied, or unsatisfied parts are explicitly deferred by the user.
- Every requirement has an acceptance criterion.
- Every acceptance criterion has verification evidence.
- Every risky action has approval evidence.
- Every design decision has rationale and rejected alternatives.
- Every packet has an integration decision.
- Every review finding has a disposition.
- Reflection captured useful learning.
- Archive links the important artifacts.
- The final answer states only what the evidence supports.
