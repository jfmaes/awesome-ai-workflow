#!/usr/bin/env python3
"""Deterministic Stop gate for Claude Code.

Blocks the agent from stopping while configured checks fail. Configure checks
in .claude/stop-gate.json:

    {
      "checks": [
        {"name": "tests", "command": "npm test"},
        {"name": "lint", "command": "npm run lint"}
      ],
      "timeout_seconds": 600
    }

With no config file (or an empty "checks" list) the hook is a no-op, so it is
safe to wire up before deciding which checks to enforce. Claude Code's
built-in cap (a Stop hook is overridden after 8 consecutive blocks without
progress) is the runaway backstop; this script additionally honors
stop_hook_active so a hook-driven continuation can always finish.

For fuzzy, judgment-based completion conditions use the built-in /goal
command instead — this gate is for checks a script can verify exactly.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

TAIL_LINES = 15


def project_root(event: dict) -> Path:
    """The session cwd drifts with `cd`; CLAUDE_PROJECT_DIR stays anchored."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")


def read_config(root: Path) -> dict:
    config_path = root / ".claude" / "stop-gate.json"
    if not config_path.is_file():
        return {}
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("stop_gate: could not parse .claude/stop-gate.json; allowing stop", file=sys.stderr)
        return {}
    return config if isinstance(config, dict) else {}


def run_check(command: str, cwd: Path, timeout: int) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    if result.returncode == 0:
        return True, ""
    output = (result.stdout + "\n" + result.stderr).strip().splitlines()
    return False, "\n".join(output[-TAIL_LINES:])


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    # A Stop-hook-driven continuation is already running; let it finish.
    if event.get("stop_hook_active"):
        return 0

    root = project_root(event)
    config = read_config(root)
    checks = config.get("checks") or []
    if not checks:
        return 0
    timeout = int(config.get("timeout_seconds") or 600)

    failures = []
    for check in checks:
        if not isinstance(check, dict):
            failures.append(f"[config] invalid entry in stop-gate.json (expected an object): {check!r}")
            continue
        name = str(check.get("name") or check.get("command") or "check")
        command = check.get("command")
        if not command:
            continue
        passed, detail = run_check(str(command), root, timeout)
        if not passed:
            failures.append(f"[{name}] `{command}` failed:\n{detail}")

    if failures:
        reason = (
            "Stop gate: required checks are failing. Fix them (or explain to the "
            "user why they cannot pass) before finishing.\n\n" + "\n\n".join(failures)
        )
        print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
