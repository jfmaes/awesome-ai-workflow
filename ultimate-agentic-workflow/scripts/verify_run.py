#!/usr/bin/env python3
"""Validate a .workflow/<run-slug>/ directory before execution.

Read-only. Checks that plan.md has the required sections and that state.json
parses and carries the keys the workflow depends on. Exits non-zero with a
list of problems so it can serve as a deterministic gate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PLAN_REQUIRED_SECTIONS = [
    "## Goal",
    "## Success Criteria",
    "## Constraints",
    "## Risks",
    "## Work Packets",
    "## Verification",
]

STATE_REQUIRED_KEYS = ["goal", "success_criteria", "packets", "verification"]
PACKET_REQUIRED_KEYS = ["id", "objective", "ownership", "status"]
VERIFICATION_REQUIRED_KEYS = ["check", "required", "status"]


def read_utf8(path: Path) -> tuple[str | None, list[str]]:
    try:
        return path.read_text(encoding="utf-8"), []
    except UnicodeDecodeError:
        return None, [f"{path.name} is not valid UTF-8"]
    except OSError as error:
        return None, [f"{path.name} could not be read: {error}"]


def markdown_headings(content: str) -> set[str]:
    """Heading lines outside code fences, so fenced examples don't count."""
    headings: set[str] = set()
    in_fence = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence and stripped.startswith("#"):
            headings.add(stripped)
    return headings


def check_plan(run_dir: Path) -> list[str]:
    plan = run_dir / "plan.md"
    if not plan.is_file():
        return [f"missing {plan}"]
    content, problems = read_utf8(plan)
    if content is None:
        return problems
    headings = markdown_headings(content)
    return [
        f"plan.md missing section: {section}"
        for section in PLAN_REQUIRED_SECTIONS
        if section not in headings
    ]


def check_items(state: dict, key: str, required_keys: list[str]) -> list[str]:
    if key not in state:
        return []  # the missing key is already reported by the caller
    items = state[key]
    if not isinstance(items, list):
        return [f"{key} must be a list, got {type(items).__name__}"]
    problems = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            problems.append(f"{key}[{index}] must be an object")
            continue
        problems.extend(
            f"{key}[{index}] missing key: {field}" for field in required_keys if field not in item
        )
    return problems


def check_state(run_dir: Path) -> list[str]:
    state_path = run_dir / "state.json"
    if not state_path.is_file():
        return [f"missing {state_path}"]
    content, problems = read_utf8(state_path)
    if content is None:
        return problems
    try:
        state = json.loads(content)
    except json.JSONDecodeError as error:
        return [f"state.json is not valid JSON: {error}"]
    if not isinstance(state, dict):
        return ["state.json must be a JSON object"]

    problems = [f"state.json missing key: {key}" for key in STATE_REQUIRED_KEYS if key not in state]
    problems += check_items(state, "packets", PACKET_REQUIRED_KEYS)
    problems += check_items(state, "verification", VERIFICATION_REQUIRED_KEYS)
    return problems


def verify_run(run_dir: Path) -> list[str]:
    if not run_dir.is_dir():
        return [f"run directory does not exist: {run_dir}"]
    return check_plan(run_dir) + check_state(run_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="Path to .workflow/<run-slug>/")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    problems = verify_run(Path(args.run_dir))
    if args.json:
        print(json.dumps({"ok": not problems, "problems": problems}, indent=2))
    elif problems:
        for problem in problems:
            print(f"FAIL: {problem}")
    else:
        print("ok: run directory has required plan sections and state keys")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
