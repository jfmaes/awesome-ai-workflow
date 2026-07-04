#!/usr/bin/env python3
"""Initialize tiny agent bootloader files for the Ultimate Agentic Workflow.

File roles:
- AGENTS.md: bootloader for Codex (and any CLI that reads AGENTS.md).
- CLAUDE.md: bootloader for Claude Code.
- OPS.md: shared operational guide (commands, validation, durable lessons).

The same filename never plays a different role per CLI, so initializing both
CLIs on one repo is safe. All target paths are checked before anything is
written; without --force the script refuses to touch an existing file and
writes nothing at all.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"
CLAUDE_KIT_DIR = SKILL_DIR / "assets" / "claude"

CLI_CONFIG_DIRS = {
    "codex": "`.codex` (or your harness's config directory)",
    "claude": "`.claude`",
    "both": "`.codex` / `.claude` (or your harness's config directory)",
}


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def detect_node_runner(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
        return "bun"
    return "npm"


def command_from_package(package: dict, runner: str, names: list[str], fallback: str) -> str:
    scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
    for name in names:
        if name in scripts:
            return f"{runner} run {name}"
    return fallback


def detect_commands(root: Path) -> dict[str, str]:
    if (root / "package.json").exists():
        package = load_json(root / "package.json")
        runner = detect_node_runner(root)
        test_fallback = "npm test" if runner == "npm" else f"{runner} test"
        return {
            "build_command": command_from_package(package, runner, ["build"], f"{runner} run build"),
            "run_command": command_from_package(package, runner, ["dev", "start"], f"{runner} run dev"),
            "test_command": command_from_package(package, runner, ["test"], test_fallback),
            "lint_command": command_from_package(package, runner, ["lint"], f"{runner} run lint"),
            "typecheck_command": command_from_package(
                package, runner, ["typecheck", "tsc"], f"{runner} run typecheck"
            ),
        }
    if (root / "Cargo.toml").exists():
        return {
            "build_command": "cargo build",
            "run_command": "cargo run",
            "test_command": "cargo test",
            "lint_command": "cargo clippy -- -D warnings",
            "typecheck_command": "cargo check",
        }
    if (root / "go.mod").exists():
        return {
            "build_command": "go build ./...",
            "run_command": "go run .",
            "test_command": "go test ./...",
            "lint_command": "go vet ./...",
            "typecheck_command": "go build ./...",
        }
    if (root / "pyproject.toml").exists() or (root / "setup.py").exists():
        return {
            "build_command": "python -m build",
            "run_command": "python -m <module>",
            "test_command": "pytest",
            "lint_command": "ruff check .",
            "typecheck_command": "mypy .",
        }
    if (root / "pom.xml").exists():
        return {
            "build_command": "mvn compile",
            "run_command": "mvn exec:java",
            "test_command": "mvn test",
            "lint_command": "not configured",
            "typecheck_command": "mvn compile",
        }
    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        return {
            "build_command": "./gradlew build",
            "run_command": "./gradlew run",
            "test_command": "./gradlew test",
            "lint_command": "./gradlew check",
            "typecheck_command": "./gradlew compileJava",
        }
    if (root / "Gemfile").exists():
        return {
            "build_command": "bundle install",
            "run_command": "bundle exec rake",
            "test_command": "bundle exec rspec",
            "lint_command": "bundle exec rubocop",
            "typecheck_command": "not configured",
        }
    return {
        "build_command": "not configured",
        "run_command": "not configured",
        "test_command": "not configured",
        "lint_command": "not configured",
        "typecheck_command": "not configured",
    }


def detect_context(root: Path) -> dict[str, str]:
    package = load_json(root / "package.json")
    project_name = package.get("name") or root.name

    source_candidates = ["src", "app", "apps", "lib", "cmd", "pkg", "internal", "packages", "services"]
    tests_candidates = ["tests", "test", "__tests__", "spec"]
    fallback = "no standard directory detected (repo root?)"
    source_dir = next((p for p in source_candidates if (root / p).exists()), fallback)
    tests_dir = next((p for p in tests_candidates if (root / p).exists()), fallback)

    context = {
        "project_name": str(project_name),
        "source_dir": source_dir,
        "tests_dir": tests_dir,
    }
    context.update(detect_commands(root))
    return context


def render(template_name: str, context: dict[str, str]) -> str:
    template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
    return template.format(**context).rstrip() + "\n"


def plan_files(cli: str, root: Path, context: dict[str, str]) -> dict[Path, str]:
    """Return the full {path: content} plan for one init invocation."""
    files: dict[Path, str] = {root / "OPS.md": render("OPS.md.template", context)}

    def bootloader(config_dir: str) -> str:
        return render(
            "BOOTLOADER.md.template",
            {**context, "config_dir": config_dir, "ops_file": "OPS.md"},
        )

    config_dir = CLI_CONFIG_DIRS[cli]
    if cli in ("codex", "both"):
        files[root / "AGENTS.md"] = bootloader(config_dir)
    if cli in ("claude", "both"):
        files[root / "CLAUDE.md"] = bootloader(config_dir)
    return files


def plan_claude_kit(root: Path) -> dict[Path, str]:
    """Return the {path: content} plan for installing assets/claude -> .claude/."""
    target = root / ".claude"
    files: dict[Path, str] = {}
    for source in sorted(CLAUDE_KIT_DIR.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(CLAUDE_KIT_DIR)
        # Skip dev artifacts that can appear next to the hook scripts.
        if "__pycache__" in relative.parts or relative.suffix == ".pyc":
            continue
        if relative.name == "settings.json.template":
            # Never replace an existing settings.json; leave the template
            # alongside for a manual merge instead.
            dest = target / "settings.json"
            if dest.exists():
                dest = target / "settings.json.template"
        else:
            dest = target / relative
        files[dest] = source.read_text(encoding="utf-8")
    return files


def write_files(files: dict[Path, str], force: bool, skip_existing: bool = False) -> None:
    # All-or-nothing: every unwritable target is detected before any write,
    # with or without --force.
    directories = sorted(str(path) for path in files if path.is_dir())
    if directories:
        raise SystemExit(
            "refusing to overwrite directories (no files were written): " + ", ".join(directories)
        )
    if skip_existing:
        skipped = sorted(path.name for path in files if path.exists())
        files = {path: content for path, content in files.items() if not path.exists()}
        if skipped:
            print(f"skipping existing: {', '.join(skipped)}")
    elif not force:
        existing = sorted(str(path) for path in files if path.exists())
        if existing:
            raise SystemExit(
                "refusing to overwrite existing files (no files were written): "
                + ", ".join(existing)
                + ". Re-run with --force to overwrite everything, or --skip-existing to write only the missing files."
            )
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", choices=["codex", "claude", "both"], default="codex")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--claude-kit",
        action="store_true",
        help="Also install the .claude/ starter kit (subagents, hooks, skills, settings).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the rendered files instead of writing them (for merging into existing repos).",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Write only the missing files; leave every existing file untouched.",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.exists():
        raise SystemExit(f"Project root does not exist: {root}")

    context = detect_context(root)
    files = plan_files(args.cli, root, context)
    if args.claude_kit:
        files.update(plan_claude_kit(root))
    if args.stdout:
        try:
            for path, content in files.items():
                print(f"===== {path.relative_to(root)} =====")
                print(content)
        except BrokenPipeError:  # piped through head/less and closed early
            sys.stderr.close()
        return 0
    write_files(files, args.force, args.skip_existing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
