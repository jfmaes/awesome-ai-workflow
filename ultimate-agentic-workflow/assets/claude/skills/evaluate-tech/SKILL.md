---
name: evaluate-tech
description: Use when deciding whether to adopt, migrate to, or reject a new tool, framework, model, library, or technique — triggered by a news brief, an HN/Twitter/Reddit release, a "should I switch to X?" or "is X better than what I use?" question, or FOMO about a trendy tool. Also when recording where a technology sits on a tech radar (assess/trial/adopt/hold) or deciding when to revisit one.
---

# Evaluate Tech

## Overview

A new tool looks better than what you run. Deciding is usually the easy part — the reasoning is often obvious to a capable advisor. What's missing is that the decision **leaves no trace**: next release you re-litigate it from scratch, and everything you meant to "revisit in a quarter" silently vanishes. Meanwhile you armchair-reason from the vendor's README instead of testing on your own data.

**Core principle: every evaluation ends in two written artifacts — a dated decision record (ADR) and a radar entry with a revisit trigger.** The opinion is not the deliverable; the artifacts are. Advice evaporates; artifacts compound.

## The recipe — produce each artifact in order

1. **Frame (one line).** What would this *replace*, and what specifically is wrong with the incumbent? If the honest answer is "nothing, it's just trending," the verdict is `assess` — track it, don't act — record that and stop. Name the real blast radius: a reranker swap is not a retrieval-layer swap; a framework backbone is a database-migration-grade change, not a linter upgrade.
2. **Research — verify the claim, don't inherit it.** Invoke the `deep-research` skill on the candidate (on Codex, the equivalent research skill). Read *how* any benchmark was measured and against what baseline; check maintainer and commit history past launch week; check license and lineage (a "v2" may be a different team borrowing a recognizable name). Launch-week stars / HN rank / Twitter buzz are attention signals, not production-readiness signals.
3. **Spike — trial in isolation, never in the incumbent's place.** Use the `using-git-worktrees` skill for a throwaway branch and wire the candidate behind an adapter/interface so the incumbent still runs untouched. Reversibility first: if you cannot back it out in an afternoon, it is not a spike, it is a migration — and migrations do not belong in an evaluation.
4. **Eval — score both on YOUR data, not the vendor's README.** If no golden eval set exists for this surface, building the smallest useful one (20–50 real cases with known-good outcomes) *is* the deliverable — it pays for itself the next time a brief like this shows up. Run the same harness over both options; put the numbers side by side.
5. **Decide + ADR.** Write an ADR (template: `references/adr-template.md`): context, the claim, what you measured, the verdict, and the **trigger that would flip the verdict**. A "no" with a revisit trigger is a complete answer; a "no" with nothing written down is how you re-argue the same thing next month.
6. **Radar.** Update `~/AI_RADAR.yaml` (schema below): move the entry to its state and set `revisit`. This is the portfolio view that stops silent forgetting and caps how much you have in flight.

## Radar states + WIP limits

Track every evaluated technology in `~/AI_RADAR.yaml` (cross-project, parallels `~/AI_RETRO.md`). Seed template: `radar-template.yaml`.

- **assess** — worth watching, not acting. Cheap; unlimited.
- **trial** — actively spiking behind an adapter. **WIP limit: 3.** More than three trials at once means you are context-thrashing, not evaluating — finish or park one before starting another.
- **adopt** — in production. Each adopt entry names the ADR that justified it.
- **hold** — evaluated and rejected, or deliberately frozen. Records *why* plus the revisit trigger, so it is not re-litigated on the next release.

Every entry carries a `revisit:` date or trigger. **An entry with no revisit trigger is a leak** — it will be silently forgotten or endlessly re-argued.

## When NOT to use

- Reversible, cheap, single-file swaps — just do it (T0/T1 in ultimate-agentic-workflow terms).
- A candidate already on the radar as `hold` whose revisit trigger has not fired — check the radar first; not re-deciding is the whole point.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Ending with a recommendation but no ADR/radar entry | The artifacts are the deliverable. An un-recorded decision is re-run next release. |
| Spiking in the incumbent's place | Adapter/interface + worktree, so the trial is reversible in an afternoon. |
| Trusting the vendor's benchmark | Score on your own golden set; read the vendor's methodology before believing the number. |
| Treating it as binary adopt/reject | `assess` (track, don't act) and `trial` (adapter, not commitment) are usually the honest state. |
| "Revisit in a quarter" said as advice | Put it in the radar `revisit:` field, or nothing resurfaces it. |
