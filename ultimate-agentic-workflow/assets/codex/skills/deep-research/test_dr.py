#!/usr/bin/env python3
"""Self-test for dr.py (stdlib only; run: python3 test_dr.py)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("dr", Path(__file__).with_name("dr.py"))
dr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dr)


def _t(votes, single=False):
    return dr.tally_one({"votes": votes, "single_source": single})


def test_tally():
    assert _t([False, False, False])["verdict"] == "confirmed"
    assert _t([False, False, False])["confidence"] == "high"
    assert _t([True, False, False])["verdict"] == "confirmed"        # 1/3 refuted -> keep, medium
    assert _t([True, False, False])["confidence"] == "medium"
    assert _t([True, True, False])["verdict"] == "dropped"                  # 2/3 refuted -> drop
    assert _t([True, True, False, False, False])["verdict"] == "confirmed"  # 2/5 refuted -> keep
    assert _t([True, True, True, False, False])["verdict"] == "dropped"     # 3/5 refuted -> drop
    assert _t([])["verdict"] == "unverified"
    assert _t([False, False, False], single=True)["confidence"] == "medium"  # single source caps at medium


CLEAN_LEDGER = [
    {"id": "c1", "claim": "X", "source_url": "https://a.com/x", "votes": [False, False, False]},
    {"id": "c2", "claim": "Y", "source_url": "https://b.com/y", "votes": [True, True, False]},  # dropped
]
CLEAN_REPORT = """# Q
## Answer
X holds.
## Confirmed findings
- X [a](https://a.com/x)
## Unverified / contested
- (none)
## Gaps
- none
## Sources
- https://a.com/x
"""


def test_audit_clean_passes():
    assert dr.audit_violations([dict(r) for r in CLEAN_LEDGER], CLEAN_REPORT) == []


def test_audit_catches_silent_drop():
    # confirmed claim c1's source is NOT in the report -> silent drop
    report = CLEAN_REPORT.replace("https://a.com/x", "https://a.com/OTHER")
    v = dr.audit_violations([dict(r) for r in CLEAN_LEDGER], report)
    assert any("SILENT-DROP" in x and "c1" in x for x in v)


def test_audit_catches_fabricated_citation():
    report = CLEAN_REPORT + "\nAlso see https://fabricated.example/made-up\n"
    v = dr.audit_violations([dict(r) for r in CLEAN_LEDGER], report)
    assert any("FABRICATED" in x and "fabricated.example" in x for x in v)


def test_audit_catches_missing_section():
    report = "# Q\n## Answer\nX.\n"  # no Confirmed/Unverified/Gaps/Sources headings
    v = dr.audit_violations([dict(r) for r in CLEAN_LEDGER], report)
    assert sum(1 for x in v if "MISSING-SECTION" in x) >= 3


if __name__ == "__main__":
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            passed += 1
            print(f"  ok {name}")
    print(f"\n{passed} tests passed")
