# Claims ledger + deterministic audit (`dr.py`)

The verify tally and the claim-preservation invariant are the two disciplines a
model is most likely to fudge under budget pressure. `dr.py` (in this skill dir)
makes both mechanical, so a run can't *claim* it verified without a ledger that
proves it. Run it with `python3 <skill-dir>/dr.py …` (stdlib only, no deps).

## The ledger — `claims.jsonl`

While reading sources and running verification, append one JSON object per
load-bearing claim to a run file, e.g. `deep-research-runs/<slug>/claims.jsonl`:

```json
{"id":"c1","claim":"A2A reached a stable v1.0 spec in 2026","source_url":"https://a2a-protocol.org/latest/announcing-1.0/","quote":"the first stable spec … v1.0","load_bearing":true,"single_source":false,"votes":[false,false,false]}
```

- `quote` is text you read on the fetched page, not a snippet.
- `votes` is the list of each independent verifier's **`refuted`** boolean
  (`true` = that skeptic refuted the claim). Three entries for a `deep` run, five
  for a `max` second round.
- `single_source: true` marks a claim resting on one source; it can never earn
  high confidence.

## Step A — tally (replaces model arithmetic)

```
python3 <skill-dir>/dr.py tally deep-research-runs/<slug>/claims.jsonl
```

Writes `verdict` (`confirmed` / `dropped` / `unverified`) and `confidence`
(`high` / `medium` / `low`) back into each row, deterministically: a claim is
**dropped** when a majority of its verifiers refuted it, **confirmed** otherwise;
confidence is `high` only for a unanimous keep on more than one source. You do not
compute this by hand — the script does, so the tally can't drift.

## Step B — audit (the delivery gate)

After writing the report, and **before delivering it**:

```
python3 <skill-dir>/dr.py audit deep-research-runs/<slug>/claims.jsonl report.md
```

It exits non-zero and lists violations if:

- **SILENT-DROP** — a confirmed claim's source is not cited anywhere in the report
  (the claim-preservation invariant, mechanically).
- **FABRICATED-OR-UNFETCHED** — the report cites a URL that is not in the ledger
  (i.e. a source you never actually fetched; the single worst failure mode).
- **MISSING-SECTION** — the report lacks a Confirmed / Unverified / Gaps / Sources
  heading (see `report-format.md`).

**The run is not complete until `dr audit` exits 0.** Fix the report (or the
ledger, if a claim genuinely belongs somewhere else) and re-run.

These are heuristic guards, not proofs — the URL checks match on the cited link,
so a claim represented without its source link will trip SILENT-DROP (cite it) and
a legitimately fetched source must be in the ledger to satisfy the fabrication
check (add it). That friction is the point: it forces the ledger and the report to
agree.

## Step C — completeness critic (before the audit)

Spend one final pass asking the questions a lazy run skips:

- Which sub-question got the thinnest coverage, and is one more search worth it?
- Which confirmed claims rest on a single source? (They belong in the unverified /
  single-source section, not among the high-confidence ones.)
- What did the search *not* surface — a modality, a primary source, a dissenting
  view, a more recent date — that a reader would expect?

Anything this turns up either becomes one more targeted search or an explicit line
in the Gaps section. An honest gap beats a confident guess.
