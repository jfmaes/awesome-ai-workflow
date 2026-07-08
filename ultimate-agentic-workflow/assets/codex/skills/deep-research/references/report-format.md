# Deep Research Report Format

The report's structure IS its honesty: confirmed and unverified are visibly
separated, every claim carries a citation, and the evidence budget is stated so the
reader can weigh the depth.

## Structure

```markdown
# <Question>

> Depth: <quick|deep|max> · <N> searches · <M> sources fetched ·
> <K> load-bearing claims verified (<confirmed> confirmed / <dropped> dropped) ·
> <date>

## Answer
The direct answer to the question, 1-3 paragraphs. Leads with the conclusion the
reader asked for. Every factual sentence here is drawn from the Confirmed section.

## Confirmed findings
| Finding | Conf. | Source(s) |
| --- | --- | --- |
| <claim, one line> | high/med | [label](url), [label](url) |
...
(high = survived 3-0; med = 2-1 or corroborated single-vote; each links a source
you FETCHED)

## Unverified / single-source / contested
Claims that did NOT clear verification, or rest on one source, or where sources
disagree — kept because they're relevant, labeled because they're not confirmed.
- <claim> — single source [url]; not independently corroborated.
- <claim> — CONTESTED: [source A] says X, [source B] says Y.

## Gaps
What the research could not answer, and why (no source found, paywalled,
conflicting, out of scope). An explicit gap is a finding, not a failure.

## Sources
Flat list of every URL fetched, so the reader can audit.
```

## Rules

- **Confidence tag every confirmed claim** (high/med) from its verification margin.
- **Never fabricate a citation.** A claim with no fetched source goes in Gaps as
  "no source found," never dressed up with an invented link. This is the single most
  important rule — a fabricated source is worse than an admitted gap.
- **Separate confirmed from unverified visibly.** The reader must be able to act on
  the Confirmed section without re-checking, and know the rest needs their judgment.
- **State the evidence budget** in the header line. "3 searches, 2 sources" and "60
  searches, 40 sources" produce very different trust; make it legible.
- **Preserve every surviving claim** (claim-preservation invariant, verification.md).
  Cut by explicit relevance if space-bound; never drop silently.
- Lead the Answer with the conclusion; put method/evidence after, for the reader who
  wants to audit rather than just consume.
