# Adversarial Claim Verification (the 3-vote protocol)

This is the step that separates a research report from a confident hallucination.
It productizes a verified result: on a real run, 25 extracted claims went through
this protocol and 24 survived, 1 was refuted — with confidence tags kept honest.

## What gets verified

Not every sentence — only **load-bearing claims**: facts a reader would act on, or
that the report's conclusion depends on. Typically 10-30 per deep report. Background
and clearly-hedged statements don't need a vote; a decision-driving number does.

## The protocol

For each load-bearing claim:

1. Spawn **3 independent verifier agents** (Codex: `spawn_agent`, explorer type, no
   shared context between them — independence is the point). Each gets ONLY the
   claim and its cited source(s), not the surrounding report or the other verifiers'
   views.
2. Each verifier's instruction is adversarial by construction:
   > "Try to REFUTE this claim: '<claim>'. It cites <source_url>. Fetch the source
   > and check the claim is actually supported by it, not just adjacent to it. Search
   > for contradicting evidence. Default to `refuted: true` if the source does not
   > clearly support the claim or if you find credible contradiction. Return
   > `{refuted: bool, reason: str, better_source_url: str|null}`."
3. **Tally:** ≥2 of 3 `refuted` → the claim is **dropped** from the confirmed set
   (may move to "unverified/contested" with a note). 0-1 refuted → **confirmed**.
4. **Confidence tag** from the margin: 3-0 keep → `high`; 2-1 keep → `medium`;
   anything refuted or single-source → `low` / move to the unverified section.

## Why adversarial, not "check if true"

A verifier asked to "confirm" finds confirmation. A verifier told to REFUTE, with the
default set to refuted-on-doubt, surfaces the failure modes: source doesn't actually
say it, source is the claim's own vendor, number is stale, quote is out of context.
Perspective-diverse verification (give each verifier a different lens — does the
source support it / is the source credible / does it reproduce elsewhere) catches
more than three identical skeptics when a claim can fail in more than one way.

## Cost control

Verification is the expensive stage (3× agent calls per claim). Bound it:
- Only load-bearing claims get the full 3-vote. Others: single re-fetch check.
- `quick` tier: skip multi-vote; the orchestrator re-fetches and sanity-checks the
  2-3 claims the answer rests on.
- `deep`: 3-vote on all load-bearing claims.
- `max`: 3-vote plus a second round on any 2-1 split (add 2 more verifiers → best of 5).

## The claim-preservation invariant

After verification, the synthesis step must carry EVERY surviving claim into the
report. A synthesis that silently drops verified claims, or invents a citation to
smooth the prose, has failed — this is a real observed failure mode (one run's
synthesis dropped 17 verified claims and fabricated a source). If the report can't
fit every claim, cut by relevance explicitly, never silently, and never fabricate a
source to cover a gap — an honest "no source found for X" is the correct output.
