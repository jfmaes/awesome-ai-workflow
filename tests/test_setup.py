import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "ultimate-agentic-workflow" / "scripts" / "setup.py"


def run_setup(args: list[str], cwd: Path, stdin: str = "") -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SETUP), *args],
        input=stdin,
        text=True,
        capture_output=True,
        cwd=cwd,
    )


def test_yes_bootstraps_empty_repo_end_to_end(tmp_path):
    result = run_setup(["--project-root", str(tmp_path), "--yes"], cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    for name in ["AGENTS.md", "CLAUDE.md", "OPS.md"]:
        assert (tmp_path / name).is_file()
    assert (tmp_path / ".claude" / "agents" / "code-reviewer.md").is_file()
    assert (tmp_path / ".claude" / "hooks" / "stop_gate.py").is_file()

    # Second run is a no-op that reports completion.
    again = run_setup(["--project-root", str(tmp_path), "--yes"], cwd=tmp_path)
    assert again.returncode == 0
    assert "Nothing to bootstrap" in again.stdout


def test_foreign_bootloader_gets_merge_advice_and_no_writes(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# my own file\n", encoding="utf-8")

    result = run_setup(["--project-root", str(tmp_path), "--yes"], cwd=tmp_path)

    assert result.returncode == 0
    assert "--stdout" in result.stdout
    assert "nothing was written" in result.stdout
    assert not (tmp_path / "OPS.md").exists()
    assert not (tmp_path / ".claude").exists()


def test_interactive_decline_writes_nothing(tmp_path):
    result = run_setup(["--project-root", str(tmp_path)], cwd=tmp_path, stdin="n\n")

    assert result.returncode == 0
    assert "Aborted" in result.stdout
    assert not (tmp_path / "OPS.md").exists()
    assert not (tmp_path / ".claude").exists()


def test_no_stdin_aborts_cleanly_instead_of_crashing(tmp_path):
    result = run_setup(["--project-root", str(tmp_path)], cwd=tmp_path, stdin="")

    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stderr
    assert "--yes" in result.stdout
    assert not (tmp_path / "OPS.md").exists()
