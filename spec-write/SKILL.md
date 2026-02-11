---
name: spec-write
description: "Write a specification through structured exploration and validation. Use when: (1) Starting a new feature or system, (2) User says 'write a spec', 'create spec for X', 'need requirements for Y', (3) Before running plan mode - specs are input to planning. Produces a complete spec in specs/ directory following JTBD template with testable acceptance criteria."
---

# Spec Write

Write a specification through structured exploration. This is the **input quality gate** — ensuring the spec is solid before plan → build → review.

Bad specs cause vague acceptance criteria → vague tests → wasted loop iterations. This skill prevents that by forcing the hard questions upfront.

## When to Use

- Before starting a T2 or T3 task
- When the user describes a feature but hasn't written a spec yet
- When existing specs are vague and causing plan/build problems

## Workflow

### Step 0: Prepare

Read the spec template structure:
- Study `specs/_TEMPLATE.md` or `project-init/SPEC_TEMPLATE.md` to understand the expected format
- This gives you the structure to fill in during the interview

### Step 1: Explore the Codebase (if applicable)

Before interviewing, understand what already exists. Use up to 250 parallel subagents to:
- Study existing code in the relevant area
- Identify current patterns, conventions, utilities
- Find related functionality that might constrain or inform this spec
- Check if any of this feature already exists (avoid duplicating work)
- **Check if a spec already exists for this feature in `specs/`** — if so, read it to understand current coverage, then ask the user: "A spec for [topic] already exists. Do you want to (1) update it to add missing details, (2) create a new separate spec for a different aspect, or (3) regenerate it completely?"

This context helps you ask smarter questions in the interview.

### Step 2: Interview - Job To Be Done

Ask the user to describe the job in one sentence:

**"When [situation], the user wants to [motivation], so they can [expected outcome]."**

If they use "and" in their description, **stop and split** — this should be multiple specs, not one. Apply the one-sentence test:

> "Can you describe this in one sentence without using 'and'?"

If no, it's multiple jobs. Help them identify the separate specs needed.

### Step 3: Interview - Context & Scope

Ask in order:
1. **Why does this matter?** What's the problem today?
2. **What exists already?** (You studied the code — confirm with the user)
3. **What's broken or missing?** Why can't users do this job today?
4. **Who are the users?** (Developers? End users? External systems?)
5. **What's the scope?** What's explicitly OUT of scope for this spec?

### Step 4: Interview - Requirements

For each requirement the user mentions, probe deeper:

**"You said [X]. Let me make sure I understand:"**
- What does success look like for this requirement?
- How would we verify it works?
- Is this a must-have (blocks launch) or nice-to-have (can defer)?

If a requirement is vague (e.g., "auth should work"), **push back**:
- "What specific auth scenarios need to work?"
- "What happens if auth fails?"
- "How do we know it's working?"

Force them to make it testable. If they can't articulate how to verify it, it's not a real requirement yet.

### Step 5: Interview - Edge Cases (Critical Section)

**This is where most specs fail.** The user describes the happy path, you nod, and the spec ships with no edge case coverage.

Ask systematically:
- **"What happens when [input] is invalid?"** (Empty string? Null? Wrong type?)
- **"What happens when [external system] is down?"** (API timeout? Database unavailable?)
- **"What happens when [resource] is exhausted?"** (Out of memory? Disk full? Rate limit hit?)
- **"What happens when [concurrent operations] conflict?"** (Two users editing the same thing?)
- **"What about the reverse operation?"** (If you can add, can you delete? If you can create, can you update?)

For each edge case, ask: **"What should the system do?"**
- Return an error? (What error? What HTTP status?)
- Retry? (How many times? Exponential backoff?)
- Fall back to a default? (What default?)
- Log and continue?

**If the user says "I don't know"** → flag it as `OPEN_QUESTION:` in the spec. Don't guess.

### Step 6: Interview - Data Model & APIs (if applicable)

If this spec involves data or APIs, ask:
- **What entities are involved?** (User? Session? Product? Order?)
- **What are the key fields?** (Required? Optional? Constraints?)
- **What endpoints/methods are needed?** (REST? GraphQL? Internal function?)
- **What's the request/response contract?** (Inputs? Outputs? Errors?)

If the user hasn't thought this through, help them sketch it, but **flag unresolved details** as `OPEN_QUESTION:`.

### Step 7: Interview - Acceptance Criteria

For each requirement, derive testable acceptance criteria. These must be **observable and verifiable**.

**Bad acceptance criteria:**
- "Auth should work" — Too vague
- "The system should be fast" — Not measurable
- "It should handle errors gracefully" — Not specific

**Good acceptance criteria:**
- "Given invalid credentials, the API returns 401 with error code `INVALID_CREDENTIALS`"
- "Login endpoint responds within 500ms at p95 under normal load"
- "When the database is unreachable, the system retries 3 times with exponential backoff, then returns 503"

For each acceptance criterion, ask:
- **How would we write a test for this?** If you can't describe the test, the criterion isn't specific enough.

### Step 8: Validate Completeness

Before writing the spec, check:
- ✅ **JTBD is a single sentence** (no "and")
- ✅ **Requirements are testable** (you can describe how to verify each one)
- ✅ **Edge cases are identified** (at least 3-5 edge cases, with expected behavior)
- ✅ **Acceptance criteria are observable** (you know what "done" looks like)
- ✅ **Open questions are flagged** (anything unresolved is explicitly marked)

If any of these are missing, **go back and interview more**. Don't write the spec until it's complete.

### Step 9: Write the Spec

Create `specs/[topic-name].md` using the template structure:

```markdown
# Spec: [Topic Name]

## Job To Be Done

When [situation], the user wants to [motivation], so they can [expected outcome].

## Context

[Why this matters, what exists today, what's broken/missing — from Step 3]

## Requirements

### Must Have
- [ ] [Requirement 1 with testable success criteria]
- [ ] [Requirement 2 with testable success criteria]

### Nice to Have
- [ ] [Optional enhancement]

## Data Model / APIs

[Entities, fields, endpoints, contracts — from Step 6, or "Not applicable"]

## Edge Cases

- [Edge case 1: what happens? Expected behavior.]
- [Edge case 2: what happens? Expected behavior.]
- [Edge case 3: what happens? Expected behavior.]

## Acceptance Criteria

- [ ] [Observable outcome 1 — describe how to test]
- [ ] [Observable outcome 2 — describe how to test]
- [ ] [Performance requirement, if any — with numbers]

## Constraints

- [Budget/time/technical constraints, if any]
- [Dependencies on other specs or external systems]

## Open Questions

- OPEN_QUESTION: [Unresolved decision 1]
- OPEN_QUESTION: [Unresolved decision 2]
```

### Step 10: Review With User

Present the spec and ask:
1. **"Does this match what you had in mind?"**
2. **"Are there edge cases I missed?"**
3. **"Can we verify all these acceptance criteria?"**
4. **"Do the open questions need answers before we plan, or can we defer them?"**

Iterate until the user confirms the spec is ready.

### Step 11: Next Steps

Tell the user:
- **If there are no `OPEN_QUESTION:` items** → "Ready to plan. Run `./loop.sh plan` to generate the implementation plan."
- **If there are unresolved questions** → "Resolve these open questions first, then re-run `/spec-write` to update the spec, or answer them now and I'll update it."

## Key Rules

- **Force the one-sentence test.** If the JTBD uses "and", it's multiple specs. Split them.
- **Edge cases are mandatory.** A spec with only happy-path coverage is incomplete. Push for at least 3-5 edge cases with expected behavior.
- **Testability is the bar.** If you can't describe how to verify a requirement, it's not specific enough. Keep probing.
- **Flag unknowns explicitly.** `OPEN_QUESTION:` is better than a guess. The plan/build steps will surface if these block progress.
- **Don't implement.** This skill writes specs only. The build loop implements them.
- **Compare against existing code.** If Step 1 found that part of this already exists, make sure the spec acknowledges it (either "extend existing X" or "this is greenfield").

## Anti-Patterns to Avoid

❌ **Accepting vague requirements** — "It should be secure" → What does secure mean? Auth? Encryption? Input validation?

❌ **Skipping edge cases** — User describes happy path, you write it down, done. Wrong. Force the failure scenarios.

❌ **Writing acceptance criteria that aren't testable** — "The user should be happy" vs "The user sees a success message within 2 seconds."

❌ **Guessing at unknowns** — If the user doesn't know what should happen when X fails, write `OPEN_QUESTION:`, don't invent an answer.

❌ **Bundling multiple jobs** — "User auth and session management and password reset" → Three specs, not one.
