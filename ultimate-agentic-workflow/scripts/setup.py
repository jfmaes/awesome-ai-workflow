#!/usr/bin/env python3
"""One-command guided setup: preflight, then bootstrap with confirmation.

    python3 <skill-dir>/scripts/setup.py --project-root .          # interactive
    python3 <skill-dir>/scripts/setup.py --project-root . --yes    # no prompt

Runs the read-only preflight first, shows what exists and what is missing,
then (only with confirmation or --yes) writes the missing bootstrap files.
It never overwrites anything: repos with their own CLAUDE.md/AGENTS.md get
merge advice instead of writes.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def plan_bootstrap(root: Path, cli: str, claude_kit: bool, repo: dict, init) -> dict[Path, str]:
    """Only files that are safe to create: never anything that exists."""
    context = init.detect_context(root)
    files: dict[Path, str] = {}

    bootloaders_missing = repo["bootloader_claude"] == "missing" and repo["bootloader_codex"] == "missing"
    if bootloaders_missing:
        files.update(init.plan_files(cli, root, context))
    if claude_kit and not repo["kit_agents_present"]:
        files.update(init.plan_claude_kit(root))
    return {path: content for path, content in files.items() if not path.exists()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument(
        "--cli",
        choices=["codex", "claude", "both"],
        default="both",
        help="codex = universal AGENTS.md harnesses (Codex, OpenCode, Cursor, Gemini CLI, ...); default: both",
    )
    parser.add_argument("--no-claude-kit", action="store_true", help="Skip the .claude/ starter kit.")
    parser.add_argument("--yes", action="store_true", help="Apply without prompting.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root does not exist or is not a directory: {root}")

    preflight = load_sibling("preflight")
    init = load_sibling("init_agents")

    report = preflight.build_report(root)
    preflight.print_human(report)
    print()

    repo = report["repo"]
    if repo.get("v1_claude_layout"):
        print(
            "v1 layout detected — nothing was written. Follow the migration step printed "
            "above (git mv AGENTS.md OPS.md, then re-run init with --skip-existing)."
        )
        return 0
    if repo["bootloader_claude"] == "foreign" or repo["bootloader_codex"] == "foreign":
        print(
            "This repo already has its own CLAUDE.md/AGENTS.md — nothing was written.\n"
            "Merge manually instead:\n"
            f"  python3 {Path(__file__).parent / 'init_agents.py'} --cli {args.cli} --claude-kit --stdout --project-root {root}"
        )
        return 0

    claude_kit = not args.no_claude_kit and args.cli in ("claude", "both")
    files = plan_bootstrap(root, args.cli, claude_kit, repo, init)
    if not files:
        print("Nothing to bootstrap — setup already complete. Next: run /retro at session end; use /mint-skill when a workflow repeats.")
        return 0

    print("Will create:")
    for path in sorted(files):
        print(f"  {path.relative_to(root)}")
    if not args.yes:
        try:
            answer = input(f"\nWrite {len(files)} files? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nNo interactive input available — nothing was written. Re-run with --yes to apply.")
            return 0
        if answer not in ("y", "yes"):
            print("Aborted — nothing was written.")
            return 0

    init.write_files(files, force=False)
    print("\nDone. Follow the remaining preflight next-steps above (tool/framework installs stay approval-first).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
