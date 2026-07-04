#!/usr/bin/env python3
"""Optional learning Stop gate for Claude Code.

Once per session, before the agent finishes, this hook blocks the stop one
time and asks the agent to run a lesson-capture pass (the /retro skill): pull
durable lessons out of the session and persist them where future sessions
will actually read them.

Concept credit: this is an original implementation of the session-learning
idea popularized by the community `/teach` and `/reflect` skills
(github.com/alexknowshtml/claude-skills) and Every's compound-engineering
`/compound` step. No text or code is copied from those projects.

Sessions shorter than MIN_TRANSCRIPT_LINES are let through without a prompt —
trivial sessions have no lessons worth a forced extra turn.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

MIN_TRANSCRIPT_LINES = 40

REASON = (
    "Learning gate (fires once per session): before finishing, run a short "
    "retrospective — the /retro skill if installed, otherwise inline. "
    "Capture at most a few durable lessons from this session: corrections the "
    "user made, commands or facts that were hard-won, friction that a skill, "
    "subagent, or OPS.md note would remove next time. Persist them where a "
    "future session will read them (OPS.md operational notes, docs/lessons/, "
    "or propose a new skill/subagent to the user). If the session genuinely "
    "taught nothing durable, say so in one line. Then finish normally."
)


def marker_path(session_id: str) -> Path:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_") or "unknown"
    return Path(tempfile.gettempdir()) / f"claude-learn-gate-{safe}"


def transcript_is_substantive(transcript_path: str) -> bool:
    if not transcript_path:
        return True
    try:
        with open(transcript_path, "r", encoding="utf-8") as handle:
            for count, _ in enumerate(handle, start=1):
                if count >= MIN_TRANSCRIPT_LINES:
                    return True
    except OSError:
        return True
    return False


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if event.get("stop_hook_active"):
        return 0

    marker = marker_path(str(event.get("session_id") or ""))
    if marker.exists():
        return 0

    if not transcript_is_substantive(str(event.get("transcript_path") or "")):
        return 0

    try:
        marker.touch()
    except OSError:
        return 0  # cannot track one-shot behavior; fail open rather than loop

    print(json.dumps({"decision": "block", "reason": REASON}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
