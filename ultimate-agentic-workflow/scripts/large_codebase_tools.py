#!/usr/bin/env python3
"""Assess large-codebase tool readiness without installing anything."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Callable


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

LANGUAGE_BY_SUFFIX = {
    ".c": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".kt": "kotlin",
    ".py": "python",
    ".rb": "ruby",
    ".rs": "rust",
    ".swift": "swift",
    ".ts": "typescript",
    ".tsx": "typescript",
}

SERENA_LANGUAGES = {
    "c",
    "cpp",
    "csharp",
    "go",
    "java",
    "javascript",
    "kotlin",
    "python",
    "ruby",
    "rust",
    "swift",
    "typescript",
}

TOOL_CATALOG: dict[str, dict[str, list[str] | str]] = {
    "uv": {
        "commands": ["uv"],
        "purpose": "Python tool manager required by Serena's recommended installation path.",
        "install": [
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
            "brew install uv",
            "pipx install uv",
        ],
        "configure": [],
        "risk": ["Installs a local Python package/tool manager and may update shell startup instructions."],
    },
    "ripgrep": {
        "commands": ["rg"],
        "purpose": "Fast exact-text and filename search. This is the default first search tool.",
        "install": [
            "brew install ripgrep",
            "sudo apt-get install ripgrep",
            "cargo install ripgrep",
        ],
        "configure": [],
        "risk": ["Installs a local search binary. No code leaves the machine."],
    },
    "serena": {
        "commands": ["serena"],
        "purpose": "LSP-backed symbol navigation for large or unfamiliar codebases.",
        "install": [
            "uv tool install -p 3.13 serena-agent",
            "serena init",
        ],
        "configure_codex": [
            "serena setup codex",
            "or edit ~/.codex/config.toml / .codex/config.toml with an [mcp_servers.serena] entry",
        ],
        "configure_claude": [
            "claude mcp add --scope user serena -- serena start-mcp-server --context claude-code --project-from-cwd",
            "claude mcp add serena -- serena start-mcp-server --context claude-code --project \"$(pwd)\"",
        ],
        "risk": [
            "Installs a local Python tool through uv.",
            "May edit Codex or Claude MCP configuration after approval.",
            "Read/write-capable Serena tools must stay approval-gated until a task plan permits them.",
        ],
    },
    "ast-grep": {
        "commands": ["ast-grep"],
        "purpose": "Structural code search and rewrite when syntax shape matters more than text.",
        "install": [
            "npm install --global @ast-grep/cli",
            "pip install ast-grep-cli",
            "brew install ast-grep",
            "cargo install ast-grep --locked",
        ],
        "configure": [],
        "risk": ["Installs a local structural search binary. Rewrite usage needs normal review and tests."],
    },
    "grepai": {
        "commands": ["grepai"],
        "purpose": "Local semantic code search for vocabulary-mismatched discovery.",
        "install": [
            "brew install yoanbernabeu/tap/grepai",
            "curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh | sh",
        ],
        "configure": [
            "ollama pull nomic-embed-text",
            "grepai init",
            "grepai watch",
        ],
        "risk": [
            "Builds a local code index.",
            "OpenAI or hosted embedding providers are optional; use Ollama for local-only indexing.",
        ],
    },
    "ollama": {
        "commands": ["ollama"],
        "purpose": "Local model and embedding runtime used by grepai's default local setup.",
        "install": ["curl -fsSL https://ollama.com/install.sh | sh"],
        "configure": ["ollama pull nomic-embed-text"],
        "risk": ["Installs a local model runtime and downloads embedding model weights."],
    },
    "warpgrep": {
        "commands": [],
        "purpose": "Hosted Morph code-search/MCP option for fuzzy discovery when local options are insufficient.",
        "install": [
            "codex mcp add morph --env MORPH_API_KEY=YOUR_API_KEY -- npx --prefer-offline -y @morphllm/morphmcp",
            "claude mcp add morph --scope user -e MORPH_API_KEY=YOUR_API_KEY -- npx --prefer-offline -y @morphllm/morphmcp",
        ],
        "configure": ["Create a Morph API key and expose it as MORPH_API_KEY."],
        "risk": [
            "Requires a hosted service and API key.",
            "code leaves the machine for hosted analysis unless limited to public GitHub search.",
        ],
    },
}


def collect_project_signals(root: Path, large_file_threshold: int) -> dict:
    file_count = 0
    source_file_count = 0
    language_counts: dict[str, int] = {}

    # Prune ignored directories during the walk instead of filtering after the
    # fact, so huge node_modules/vendor trees are never descended into.
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIRS]
        for filename in filenames:
            # os.walk yields dangling symlinks as "files"; keep rglob's
            # is_file() semantics and skip them.
            if not (Path(dirpath) / filename).is_file():
                continue
            file_count += 1
            language = LANGUAGE_BY_SUFFIX.get(Path(filename).suffix.lower())
            if language:
                source_file_count += 1
                language_counts[language] = language_counts.get(language, 0) + 1

    monorepo_dirs = [
        name
        for name in ["apps", "packages", "services", "libs", "crates"]
        if (root / name).is_dir()
    ]
    reasons: list[str] = []
    if file_count >= large_file_threshold:
        reasons.append("file-count-threshold")
    if source_file_count >= max(100, large_file_threshold // 3):
        reasons.append("source-file-count")
    if len(language_counts) >= 3:
        reasons.append("polyglot")
    if monorepo_dirs:
        reasons.append("monorepo-layout")

    languages = sorted(language_counts)
    would_benefit_from_serena = bool(reasons and SERENA_LANGUAGES.intersection(languages))

    return {
        "root": str(root),
        "file_count": file_count,
        "source_file_count": source_file_count,
        "languages": languages,
        "language_counts": dict(sorted(language_counts.items())),
        "monorepo_dirs": monorepo_dirs,
        "large_codebase": bool(reasons),
        "large_codebase_reasons": reasons,
        "would_benefit_from_serena": would_benefit_from_serena,
    }


def default_command_resolver(names: list[str]) -> str | None:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def command_version(path: str) -> str | None:
    try:
        result = subprocess.run(
            [path, "--version"],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except Exception:
        return None
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else None


def preferred_uv_install_command() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "brew install uv"
    if system == "linux":
        return "curl -LsSf https://astral.sh/uv/install.sh | sh"
    return "pipx install uv"


def check_tools(command_resolver: Callable[[list[str]], str | None] = default_command_resolver) -> dict:
    statuses = {}
    for name, metadata in TOOL_CATALOG.items():
        commands = list(metadata.get("commands", []))
        path = command_resolver(commands) if commands else None
        statuses[name] = {
            # Hosted/MCP tools without a local binary cannot be detected via
            # PATH; mark them uncheckable instead of implying "checked, absent".
            "checkable": bool(commands),
            "installed": bool(path),
            "path": path,
            "version": command_version(path) if path else None,
            "purpose": metadata["purpose"],
        }
    return statuses


def build_serena_approval_request(project: dict, tools: dict) -> dict:
    serena = TOOL_CATALOG["serena"]
    commands = []
    if not tools["uv"]["installed"]:
        commands.append(preferred_uv_install_command())
    commands.extend(serena["install"])
    commands.append(serena["configure_codex"][0])
    commands.append(serena["configure_claude"][0])
    return {
        "tool": "serena",
        "prompt": (
            "This repository shows large-codebase signals "
            f"({', '.join(project['large_codebase_reasons'])}). Serena may help with symbol-level navigation, "
            "but it is not installed. May I install/configure Serena for Codex and/or Claude?"
        ),
        "commands": commands,
        "writes": [
            "uv tool installation directory and cache",
            "~/.codex/config.toml or trusted project .codex/config.toml",
            "~/.claude.json, .mcp.json, or .claude/settings.local.json depending on Claude Code scope",
        ],
        "network": [
            "Downloads serena-agent through uv if not already cached.",
            "May contact package registries during install.",
        ],
        "rollback": [
            "Remove the uv-installed serena-agent tool.",
            "Delete or disable the [mcp_servers.serena] Codex config entry.",
            "Remove the Claude Code Serena MCP entry.",
        ],
    }


def build_report(
    root: Path,
    large_file_threshold: int = 1000,
    command_resolver: Callable[[list[str]], str | None] = default_command_resolver,
) -> dict:
    root = root.resolve()
    project = collect_project_signals(root, large_file_threshold)
    tools = check_tools(command_resolver)

    serena_installed = tools["serena"]["installed"]
    if project["would_benefit_from_serena"] and not serena_installed:
        serena_action = "ask-to-install"
    elif project["would_benefit_from_serena"]:
        serena_action = "consider-using"
    else:
        serena_action = "not-needed-yet"

    approval_requests = []
    if serena_action == "ask-to-install":
        approval_requests.append(build_serena_approval_request(project, tools))

    return {
        "mode": "read-only-readiness",
        "project": project,
        "tools": tools,
        "recommendations": {
            "ripgrep": {
                "action": "use" if tools["ripgrep"]["installed"] else "ask-to-install-core-search",
                "reason": "Exact-text search is the default first retrieval step.",
            },
            "serena": {
                "action": serena_action,
                "reason": "Large or unfamiliar codebases benefit from symbol-level navigation before broad file reads.",
            },
            "ast-grep": {
                "action": "use-when-structural-search-needed"
                if tools["ast-grep"]["installed"]
                else "optional-install-when-structural-search-needed",
                "reason": "Use when syntax shape matters more than text.",
            },
            "grepai": {
                "action": "use-as-last-resort-semantic-search"
                if tools["grepai"]["installed"]
                else "optional-install-when-vocabulary-search-fails",
                "reason": "Use after exact, symbol, and structural search fail.",
            },
            "warpgrep": {
                "action": "hosted-explicit-approval-only",
                "reason": "Requires Morph/API-key setup and may send code/query context to a hosted service.",
            },
        },
        "approval_requests": approval_requests,
        "tool_catalog": TOOL_CATALOG,
        "safety": "No commands were executed. This script only inspected files and PATH.",
    }


def print_human(report: dict) -> None:
    project = report["project"]
    print("Large-codebase readiness")
    print(f"- Root: {project['root']}")
    print(f"- Files: {project['file_count']} ({project['source_file_count']} source)")
    print(f"- Languages: {', '.join(project['languages']) or 'none detected'}")
    print(f"- Large-codebase signals: {', '.join(project['large_codebase_reasons']) or 'none'}")
    print(f"- Serena fit: {project['would_benefit_from_serena']}")
    print()
    print("Tool status")
    for name, status in report["tools"].items():
        if not status["checkable"]:
            installed = "not PATH-checkable (hosted/MCP tool)"
        elif status["installed"]:
            installed = "installed"
        else:
            installed = "missing"
        version = f" ({status['version']})" if status["version"] else ""
        print(f"- {name}: {installed}{version}")
    print()
    print("Recommendations")
    for name, recommendation in report["recommendations"].items():
        print(f"- {name}: {recommendation['action']} - {recommendation['reason']}")
    if report["approval_requests"]:
        print()
        print("Approval request draft")
        for request in report["approval_requests"]:
            print(f"- {request['prompt']}")
            print("  Commands:")
            for command in request["commands"]:
                print(f"  - {command}")
    print()
    print(report["safety"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--large-file-threshold", type=int, default=1000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root)
    if not root.is_dir():
        raise SystemExit(f"Project root does not exist or is not a directory: {root}")

    report = build_report(root, args.large_file_threshold)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
