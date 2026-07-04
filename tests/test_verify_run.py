import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ultimate-agentic-workflow" / "scripts" / "verify_run.py"


def load_module():
    spec = importlib.util.spec_from_file_location("verify_run", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_valid_run(run_dir: Path) -> None:
    run_dir.mkdir(parents=True)
    (run_dir / "plan.md").write_text(
        "# Workflow Plan\n\n## Goal\n\n## Success Criteria\n\n## Constraints\n\n"
        "## Risks\n\n## Work Packets\n\n## Verification\n",
        encoding="utf-8",
    )
    (run_dir / "state.json").write_text(
        json.dumps(
            {
                "goal": "demo",
                "success_criteria": ["done"],
                "packets": [
                    {"id": "01", "objective": "x", "ownership": "agent", "status": "pending"}
                ],
                "verification": [{"check": "tests", "required": True, "status": "pending"}],
            }
        ),
        encoding="utf-8",
    )


def test_valid_run_directory_passes(tmp_path):
    run_dir = tmp_path / ".workflow" / "demo"
    make_valid_run(run_dir)
    module = load_module()

    assert module.verify_run(run_dir) == []


def test_missing_plan_section_and_state_keys_fail(tmp_path):
    run_dir = tmp_path / ".workflow" / "demo"
    make_valid_run(run_dir)
    (run_dir / "plan.md").write_text("## Goal\n", encoding="utf-8")
    (run_dir / "state.json").write_text(
        json.dumps({"goal": "demo", "packets": [{"id": "01"}]}), encoding="utf-8"
    )
    module = load_module()

    problems = module.verify_run(run_dir)
    assert any("## Work Packets" in problem for problem in problems)
    assert any("missing key: verification" in problem for problem in problems)
    assert any("packets[0] missing key: ownership" in problem for problem in problems)


def test_cli_exits_nonzero_on_missing_run_dir(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--run-dir", str(tmp_path / "nope"), "--json"],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["ok"] is False
    assert report["problems"]


def test_wrong_typed_packets_and_null_are_single_clear_problems(tmp_path):
    run_dir = tmp_path / ".workflow" / "demo"
    make_valid_run(run_dir)
    module = load_module()

    state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
    for bad_value, expected_type in [(None, "NoneType"), ("not-a-list", "str")]:
        state["packets"] = bad_value
        (run_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
        problems = module.verify_run(run_dir)
        assert problems == [f"packets must be a list, got {expected_type}"]


def test_invalid_utf8_is_reported_not_crashed(tmp_path):
    run_dir = tmp_path / ".workflow" / "demo"
    make_valid_run(run_dir)
    (run_dir / "state.json").write_bytes(b"\xff\xfe{}")
    module = load_module()

    problems = module.verify_run(run_dir)
    assert problems == ["state.json is not valid UTF-8"]


def test_sections_inside_code_fences_do_not_count(tmp_path):
    run_dir = tmp_path / ".workflow" / "demo"
    make_valid_run(run_dir)
    fenced = "# Plan\n\n```markdown\n" + "\n".join(
        ["## Goal", "## Success Criteria", "## Constraints", "## Risks", "## Work Packets", "## Verification"]
    ) + "\n```\n"
    (run_dir / "plan.md").write_text(fenced, encoding="utf-8")
    module = load_module()

    problems = module.verify_run(run_dir)
    assert any("## Goal" in problem for problem in problems)
