---
name: deep-research
description: Use when a question needs a thorough, multi-source, fact-checked research report instead of a single-pass answer — evaluating a technology/protocol/vendor, "what is the current state of X", comparing options, verifying a claim before acting on it, or any research where sources should be cited and claims verified. For Codex and other harnesses without a built-in deep-research mode.
---

# Deep Research

## Overview

A model answering from memory hallucinates and cannot cite. This skill runs the loop the strongest deep-research systems use — decompose, search per sub-question, read sources, verify claims adversarially, synthesize with citations — using the host's native agents for parallel fan-out. Grounded in cross-validated meta-research (5 angles → 25 sources → 24/25 claims survived 3-vote verification).

**Core principle: every claim in the final report traces to a source you actually fetched, and every load-bearing claim survived an explicit attempt to refute it.** Unverified claims are flagged, never hidden among confirmed ones.

## First: clarify before spending budget

If the question is underspecified — unclear scope, timeframe, or what decision it feeds — ask 2-3 clarifying questions FIRST, then proceed. A large search budget spent on the wrong question is the most expensive failure mode. Skip this only when the question is already sharp.

## Pick a depth tier (it bounds the fan-out)

- **quick** — ~5-10 searches, single pass, light verification. A factual lookup.
- **deep** (default) — ~30-80 searches, full fan-out + adversarial verification. Decision-grade.
- **max** — ~150+ searches, multiple rounds until new searches stop surfacing new claims. High-stakes.

## The loop — orchestrator is this session, workers are native agents

1. **Decompose** into independent sub-questions (Self-Ask). The compositionality gap is real and does not shrink with model size: a model can answer each part yet fail to compose them. Decomposition + per-sub-question retrieval is the structural edge over a solo agent, not a workaround.
2. **Fan out search** — one worker per sub-question (Codex: `spawn_agent`, explorer type — see `references/codex-agents.md`). Each worker runs a ReAct loop: search → read → identify gap → search again. Workers return structured findings `{claim, source_url, supporting_quote}` — never snippet-only. Bound to 2-5 concurrent workers; keep integration in the parent.
3. **Fetch, don't snippet** — a claim backed only by a search-result snippet is unverified. The worker opens the actual page and quotes the passage that supports the claim.
4. **Verify adversarially** — the differentiator. For each load-bearing claim, spawn an independent skeptic instructed to REFUTE it (3-vote protocol in `references/verification.md`). ≥2 of 3 refute → drop or downgrade the claim. This is what separates a report from a plausible-sounding hallucination; it is mandatory for deep and max tiers.
5. **Synthesize** — cited report (`references/report-format.md`): confirmed claims with citations and a confidence tag, a SEPARATE section for single-source/unverified claims, and an explicit list of gaps. Claim-preservation is an invariant: synthesis that silently drops a verified claim or invents a source is the failure to guard against (a real lesson from a run whose synthesis stage dropped 17 verified claims and fabricated a source).

## When NOT to use

- A quick factual lookup a single search answers — just search.
- Inside Claude Code, which has its own built-in deep-research — use that. This skill exists for Codex and other AGENTS.md harnesses that lack one.

## Fallback — no native agents available

Run the loop sequentially: decompose, search each sub-question in turn, verify the top claims yourself by re-fetching and actively trying to refute, then synthesize. Same discipline, slower. State in the report that it ran degraded (no parallel fan-out).

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Citing a snippet you did not open | Fetch the page; quote the supporting passage. |
| Skipping refutation because claims "look right" | Plausible-and-wrong is exactly what verification catches. Mandatory for deep/max. |
| One mega-search instead of decomposition | The compositionality gap will not close on its own. Decompose. |
| Burying unverified claims among confirmed ones | Separate, explicitly labeled section. |
| Spending budget before scoping | 2-3 clarifying questions first when underspecified. |
| Fan-out larger than needed | 2-5 workers; more amplifies error and cost without improving coverage. |
