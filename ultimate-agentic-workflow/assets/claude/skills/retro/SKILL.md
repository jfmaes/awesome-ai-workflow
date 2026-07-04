---
name: retro
description: Session retrospective that turns this session's friction and discoveries into durable improvements — OPS.md notes, new skill or subagent candidates, and tracked debt. Use at the end of substantive sessions, when the learning Stop hook fires, or when the user asks what was learned.
disable-model-invocation: false
---

# Retro

Turn this session into compounding leverage. The output is a small number of durable changes, not a diary.

Concept credit: session-learning loop popularized by the community `/reflect` and `/teach` skills and compound engineering's `/compound` step; this is an original implementation.

## Steps

1. **Scan the session** for: corrections the user made, wrong turns and their root causes, hard-won facts (commands, flags, gotchas, environment quirks), and any multi-step workflow performed more than once.
2. **Classify each candidate lesson:**

   | Lesson shape | Destination |
   | --- | --- |
   | Repo command, validation quirk, environment fact | `OPS.md` operational notes (one line each) |
   | Repeated multi-step workflow | Skill candidate — propose `/mint-skill` |
   | Recurring delegate-able role (review, research, verbose checks) | Subagent candidate under `.claude/agents/` |
   | Check that should be enforced, not remembered | Hook candidate (`stop-gate.json` entry or PreToolUse guard) |
   | Deliberate shortcut taken this session | Debt entry: file an issue or add to the plan's follow-ups |
   | Design rationale | `docs/decisions/` |
   | One-off trivia | Nowhere — drop it |

3. **Apply the cheap ones** (OPS.md one-liners, debt entries) after showing the user the exact lines. Propose the expensive ones (new skills, subagents, hooks) with a one-line pitch each and let the user choose.
4. **Honesty rule:** if the session taught nothing durable, say exactly that in one line and stop. A forced lesson is worse than none.

## Quality bar

- Each OPS.md addition must change future agent behavior; no status history, no praise.
- Never duplicate an existing note — check before appending.
- Three strong lessons beat ten weak ones.
