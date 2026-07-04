# Context Engineering

Read this when a task is long enough to risk context compaction, when working in a large repo, or when dispatching subagents. Context is a finite attention budget: model precision degrades as the window fills, long before the nominal limit. Every token loaded must earn its place.

## Contents

- Loading Policy
- Durable Notes
- Compaction Survival
- Subagent Context Isolation
- Tool-Output Hygiene
- Altitude Control

## Loading Policy

- Default to just-in-time retrieval. Store lightweight identifiers — file paths, requirement IDs, stored queries, URLs — and load content only when a decision needs it.
- Load progressively: always-loaded instructions first, tier-specific references next, specialized material only when the current phase needs it.
- Prefer line-scoped reads and search-result excerpts over full-file reads. Narrow with search first, then read the smallest span that answers the question.
- Do not pre-load specs, plans, or reference docs "for completeness". Load the one the current phase consumes.
- Prefer fresh repo evidence over assistant memory, and primary docs over recollection for external APIs.

## Durable Notes

State that must survive the session lives in files, not in conversation history.

- For any task that could span a compaction (most T1+ work), write the goal, constraints, and current position to a durable file before doing anything expensive: the active plan file, `memory-bank/tasks.md` if the repo uses that pattern, or `.workflow/<slug>/plan.md` for T3.
- At each milestone, update the note with: decisions made (with rationale), unresolved bugs or open questions, what is verified vs merely written, and the next concrete step.
- Write notes as if the reader is a fresh agent with zero conversation history — because after compaction or handoff, it is.

## Compaction Survival

- Files, plans, and repo instructions are re-read after compaction; chat history is not reliable. Anything only said in conversation is at risk.
- Before context runs low, prefer the cheapest reduction first: discard stale tool output and raw logs (summarize anything load-bearing into the source or verification ledger first), then compact.
- Never let compaction be the only copy of: the original user goal, tier decision, requirement IDs, approval records, or verification status. Those live in the tier's canonical state file.
- After a compaction or session resume, re-anchor: re-read the canonical state file for the run before taking the next action.

## Subagent Context Isolation

Subagents exist to spend context so the orchestrator does not have to.

- Give each worker a bounded question or work packet with explicit scope, output format, and boundaries — not an open-ended "look into X".
- Workers may burn tens of thousands of tokens exploring; they must return a distilled summary (roughly 1-2k tokens) with `file:line` evidence, not raw logs or file dumps.
- The orchestrator keeps: decisions, requirement IDs, risk state, integration judgments, and verification claims. Workers keep: exploration detail, dead ends, raw search output.
- Never paste raw worker output into the final answer; integrate it.

## Tool-Output Hygiene

- Treat noisy tool output as disposable: extract the finding into a ledger row, drop the rest.
- Do not re-run searches or re-read files to "confirm" facts already recorded in a ledger with evidence.
- When a command produces bulky output needed as evidence, save it to a file under the run directory and reference the path.

## Altitude Control

- The orchestrating agent stays at decision altitude: what must be true, what was chosen, what proves it.
- Push exploration, bulk edits, and mechanical verification down to workers, scripts, or deterministic gates.
- If you notice the main context filling with exploration detail, that work belonged in a worker or a note file. Correct course: summarize, persist, discard.
