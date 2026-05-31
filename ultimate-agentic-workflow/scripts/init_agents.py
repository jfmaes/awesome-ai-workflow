#!/usr/bin/env python3
"""Initialize tiny agent bootloader files for the Ultimate Agentic Workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def command_from_package(package: dict, names: list[str], fallback: str) -> str:
    scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
    for name in names:
        if name in scripts:
            return f"npm run {name}"
    return fallback


def detect_context(root: Path) -> dict[str, str]:
    package = load_json(root / "package.json")
    project_name = package.get("name") or root.name

    source_dir = next((p for p in ["src", "app", "apps", "lib"] if (root / p).exists()), "src")
    tests_dir = next((p for p in ["tests", "test", "__tests__", "spec"] if (root / p).exists()), "tests")

    if package:
        build = command_from_package(package, ["build"], "npm run build")
        run = command_from_package(package, ["dev", "start"], "npm run dev")
        test = command_from_package(package, ["test", "check"], "npm test")
        lint = command_from_package(package, ["lint"], "npm run lint")
        typecheck = command_from_package(package, ["typecheck", "check"], "npm run typecheck")
    elif (root / "pyproject.toml").exists():
        build = "python -m build"
        run = "python -m <module>"
        test = "pytest"
        lint = "ruff check ."
        typecheck = "mypy ."
    else:
        build = "not configured"
        run = "not configured"
        test = "not configured"
        lint = "not configured"
        typecheck = "not configured"

    return {
        "project_name": str(project_name),
        "source_dir": source_dir,
        "tests_dir": tests_dir,
        "build_command": build,
        "run_command": run,
        "test_command": test,
        "lint_command": lint,
        "typecheck_command": typecheck,
    }


def render(template_name: str, context: dict[str, str]) -> str:
    template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
    return template.format(**context).rstrip() + "\n"


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"{path} already exists. Re-run with --force to overwrite.")
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", choices=["codex", "claude"], default="codex")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.exists():
        raise SystemExit(f"Project root does not exist: {root}")

    context = detect_context(root)

    if args.cli == "codex":
        write_file(root / "AGENTS.md", render("AGENTS.md.codex.template", context), args.force)
        write_file(root / "OPS.md", render("OPS.md.template", context), args.force)
    else:
        write_file(root / "CLAUDE.md", render("CLAUDE.md.template", context), args.force)
        write_file(root / "AGENTS.md", render("OPS.md.template", context), args.force)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
