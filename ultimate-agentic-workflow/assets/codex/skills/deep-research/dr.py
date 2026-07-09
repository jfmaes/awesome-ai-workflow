#!/usr/bin/env python3
"""dr - deterministic enforcement for the deep-research skill.

The two disciplines a model is most likely to fudge are the verification tally
and the claim-preservation invariant. This makes both mechanical, so the run
can't *say* it verified without a ledger that proves it did.

  dr tally  <claims.jsonl>               compute verdict + confidence from recorded
                                         votes (no model arithmetic), write back.
  dr audit  <claims.jsonl> <report.md>   gate before delivery. Fails (exit 1) if:
                                           - a confirmed claim's source is absent from
                                             the report (silent claim drop),
                                           - the report cites a URL not in the ledger
                                             (fabricated / unfetched citation),
                                           - a required section is missing.

Claims ledger = one JSON object per line (claims.jsonl):
  {"id":"c1","claim":"...","source_url":"https://...","quote":"...",
   "load_bearing":true,"single_source":false,"votes":[true,false,false]}
votes = each independent verifier's `refuted` boolean (true = refuted the claim).
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["confirmed", "unverified", "gap", "source"]
_URL = re.compile(r"https?://\S+")


def load(path: str) -> list[dict]:
    rows = []
    for i, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"dr: {path}:{i}: invalid JSON ({e})")
    return rows


def tally_one(row: dict) -> dict:
    """Deterministic verdict + confidence from the recorded refute-votes."""
    votes = row.get("votes") or []
    n = len(votes)
    refuted = sum(1 for v in votes if v)
    if n == 0:
        row["verdict"], row["confidence"] = "unverified", "low"
    elif refuted * 2 > n:  # majority refuted
        row["verdict"], row["confidence"] = "dropped", "n/a"
    else:
        row["verdict"] = "confirmed"
        row["confidence"] = "high" if refuted == 0 else "medium"
    if row.get("single_source") and row.get("confidence") == "high":
        row["confidence"] = "medium"  # a single source never earns high confidence
    return row


def _clean_url(u: str) -> str:
    return u.rstrip(".,);]>\"'")


def audit_violations(rows: list[dict], report_text: str) -> list[str]:
    rows = [tally_one(r) if r.get("verdict") is None else r for r in rows]
    v = []
    confirmed = [r for r in rows if r.get("verdict") == "confirmed"]

    # 1. claim-preservation: every confirmed claim's source must appear in the report
    for r in confirmed:
        u = (r.get("source_url") or "").strip()
        if u and u not in report_text:
            v.append(f"SILENT-DROP: confirmed claim {r.get('id')} source {u} is not cited in the report")

    # 2. no fabrication: every URL the report cites must exist in the ledger
    ledger_urls = {(r.get("source_url") or "").strip() for r in rows}
    ledger_urls |= {(r.get("better_source_url") or "").strip() for r in rows}
    ledger_urls = {u for u in ledger_urls if u}
    for raw in set(_URL.findall(report_text)):
        u = _clean_url(raw)
        if u and not any(u in lu or lu in u for lu in ledger_urls):
            v.append(f"FABRICATED-OR-UNFETCHED: report cites {u}, which is not in the claims ledger")

    # 3. required sections present
    heads = [h.strip().lower() for h in re.findall(r"^#{1,6}\s+(.*)$", report_text, re.M)]
    for sec in REQUIRED_SECTIONS:
        if not any(sec in h for h in heads):
            v.append(f"MISSING-SECTION: no heading covers '{sec}'")
    return v


def cmd_tally(claims: str) -> int:
    rows = [tally_one(r) for r in load(claims)]
    Path(claims).write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    conf = [r for r in rows if r["verdict"] == "confirmed"]
    dropped = sum(1 for r in rows if r["verdict"] == "dropped")
    high = sum(1 for r in conf if r.get("confidence") == "high")
    med = sum(1 for r in conf if r.get("confidence") == "medium")
    unv = sum(1 for r in rows if r["verdict"] == "unverified")
    print(f"tally: {len(conf)} confirmed ({high} high / {med} medium), {dropped} dropped, {unv} unverified")
    return 0


def cmd_audit(claims: str, report: str) -> int:
    rows = load(claims)
    text = Path(report).read_text(encoding="utf-8")
    violations = audit_violations(rows, text)
    if violations:
        print("AUDIT FAILED - the report is not ready to deliver:")
        for x in violations:
            print("  -", x)
        return 1
    n_conf = sum(1 for r in rows if r.get("verdict") == "confirmed")
    n_url = len(set(_URL.findall(text)))
    print(f"AUDIT PASSED: {n_conf} confirmed claims all cited, {n_url} report URLs all in ledger, sections present.")
    return 0


def main(argv: list[str] | None = None) -> int:
    a = argv if argv is not None else sys.argv[1:]
    if len(a) >= 2 and a[0] == "tally":
        return cmd_tally(a[1])
    if len(a) >= 3 and a[0] == "audit":
        return cmd_audit(a[1], a[2])
    sys.stderr.write(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
