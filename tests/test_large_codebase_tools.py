import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ultimate-agentic-workflow" / "scripts" / "large_codebase_tools.py"


def load_module():
    spec = importlib.util.spec_from_file_location("large_codebase_tools", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_repo(root: Path, file_count: int) -> None:
    src = root / "src"
    src.mkdir()
    for index in range(file_count):
        (src / f"module_{index}.py").write_text("def f():\n    return 1\n", encoding="utf-8")


def test_large_project_recommends_serena_when_missing(tmp_path):
    make_repo(tmp_path, 8)
    module = load_module()

    report = module.build_report(
        tmp_path,
        large_file_threshold=5,
        command_resolver=lambda names: None,
    )

    assert report["project"]["large_codebase"] is True
    assert "file-count-threshold" in report["project"]["large_codebase_reasons"]
    assert report["tools"]["serena"]["installed"] is False
    assert report["tools"]["serena"]["checkable"] is True
    # Hosted MCP tools have no local binary; the report must not imply
    # "checked PATH and absent".
    assert report["tools"]["warpgrep"]["checkable"] is False
    assert report["recommendations"]["serena"]["action"] == "ask-to-install"
    assert "May I install/configure Serena" in report["approval_requests"][0]["prompt"]


def test_ignored_directories_are_pruned_from_signals(tmp_path):
    make_repo(tmp_path, 3)
    vendored = tmp_path / "node_modules" / "dep"
    vendored.mkdir(parents=True)
    for index in range(50):
        (vendored / f"mod_{index}.js").write_text("module.exports = 1\n", encoding="utf-8")
    module = load_module()

    signals = module.collect_project_signals(tmp_path, large_file_threshold=1000)

    assert signals["file_count"] == 3
    assert "javascript" not in signals["languages"]


def test_tool_catalog_documents_install_instructions_for_identified_tools():
    module = load_module()

    required = ["uv", "ripgrep", "serena", "ast-grep", "grepai", "ollama", "warpgrep"]
    for name in required:
        tool = module.TOOL_CATALOG[name]
        assert tool["install"]
        assert tool["purpose"]
        assert tool["risk"]

    assert any("serena setup codex" in command for command in module.TOOL_CATALOG["serena"]["configure_codex"])
    assert any("claude mcp add" in command for command in module.TOOL_CATALOG["serena"]["configure_claude"])
    assert any("code leaves the machine" in risk for risk in module.TOOL_CATALOG["warpgrep"]["risk"])


def test_cli_json_reports_missing_serena_permission_request(tmp_path):
    make_repo(tmp_path, 4)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--project-root",
            str(tmp_path),
            "--large-file-threshold",
            "2",
            "--json",
        ],
        check=True,
        text=True,
        capture_output=True,
        env={**os.environ, "PATH": "/nonexistent"},
    )

    report = json.loads(result.stdout)

    assert report["mode"] == "read-only-readiness"
    assert report["project"]["large_codebase"] is True
    assert report["tools"]["serena"]["installed"] is False
    assert report["recommendations"]["serena"]["action"] == "ask-to-install"
    assert report["approval_requests"][0]["commands"]
    uv_commands = [
        command
        for command in report["approval_requests"][0]["commands"]
        if "install uv" in command or "uv/install.sh" in command
    ]
    assert len(uv_commands) == 1
    assert all(not command.startswith("or ") for command in report["approval_requests"][0]["commands"])
    assert report["approval_requests"][0]["writes"]
    assert "No commands were executed" in report["safety"]


def test_dangling_symlinks_are_not_counted(tmp_path):
    make_repo(tmp_path, 2)
    (tmp_path / "src" / "broken.py").symlink_to(tmp_path / "does-not-exist.py")
    module = load_module()

    signals = module.collect_project_signals(tmp_path, large_file_threshold=1000)

    assert signals["file_count"] == 2


def test_cli_rejects_nonexistent_project_root(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--project-root", str(tmp_path / "nope"), "--json"],
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "does not exist" in result.stderr
