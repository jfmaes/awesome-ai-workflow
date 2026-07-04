import importlib.util
import json
import subprocess
import sys
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "ultimate-agentic-workflow" / "assets" / "claude"
HOOKS = KIT / "hooks"
INIT_SCRIPT = ROOT / "ultimate-agentic-workflow" / "scripts" / "init_agents.py"

EXPECTED_AGENTS = {
    "code-reviewer",
    "skeptic-verifier",
    "test-runner",
    "researcher",
    "implementer",
}


def load_init_module():
    spec = importlib.util.spec_from_file_location("init_agents", INIT_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "---", f"{path.name} must start with YAML frontmatter"
    fields = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    raise AssertionError(f"{path.name} frontmatter never closed")


def run_hook(script: str, event: dict, cwd: Path, project_dir: Path | None = None) -> subprocess.CompletedProcess:
    import os

    env = {**os.environ}
    if project_dir is None:
        env.pop("CLAUDE_PROJECT_DIR", None)  # isolate from the test runner's own session
    else:
        env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    return subprocess.run(
        [sys.executable, str(HOOKS / script)],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        cwd=cwd,
        env=env,
    )


def test_agent_files_have_required_frontmatter_and_safe_tools():
    agent_files = {p.stem: p for p in (KIT / "agents").glob("*.md")}
    assert set(agent_files) == EXPECTED_AGENTS

    for name, path in agent_files.items():
        fields = parse_frontmatter(path)
        assert fields.get("name") == name
        description = fields.get("description", "")
        assert len(description) > 40
        # what + when: every description must say when to invoke, not just what it is
        assert "Use " in description, f"{name} description lacks a when-to-use clause"

    # Reviewers and verifiers must be read-only: no Edit/Write tools.
    for read_only in ["code-reviewer", "skeptic-verifier", "test-runner", "researcher"]:
        tools = parse_frontmatter(agent_files[read_only])["tools"]
        assert "Edit" not in tools and "Write" not in tools


def test_skills_have_valid_frontmatter():
    skill_dirs = {p.parent.name for p in (KIT / "skills").glob("*/SKILL.md")}
    assert skill_dirs == {"retro", "mint-skill"}

    mint = parse_frontmatter(KIT / "skills" / "mint-skill" / "SKILL.md")
    assert mint.get("disable-model-invocation") == "true"


def test_settings_template_is_valid_json_and_wires_stop_gate():
    settings = json.loads((KIT / "settings.json.template").read_text(encoding="utf-8"))
    stop_hooks = settings["hooks"]["Stop"][0]["hooks"]
    assert any("stop_gate.py" in hook["command"] for hook in stop_hooks)
    assert any("Read(./.env)" in rule for rule in settings["permissions"]["deny"])


def test_stop_gate_noop_without_config(tmp_path):
    result = run_hook("stop_gate.py", {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_stop_gate_blocks_on_failing_check_and_respects_active_flag(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "stop-gate.json").write_text(
        json.dumps({"checks": [{"name": "boom", "command": "echo broken >&2; exit 1"}]}),
        encoding="utf-8",
    )

    result = run_hook("stop_gate.py", {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["decision"] == "block"
    assert "boom" in output["reason"]
    assert "broken" in output["reason"]

    # A hook-driven continuation must always be allowed to finish.
    result = run_hook("stop_gate.py", {"cwd": str(tmp_path), "stop_hook_active": True}, tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_stop_gate_anchors_on_claude_project_dir_not_session_cwd(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "stop-gate.json").write_text(
        json.dumps({"checks": [{"name": "boom", "command": "exit 1"}]}), encoding="utf-8"
    )
    elsewhere = tmp_path / "some" / "subdir"
    elsewhere.mkdir(parents=True)

    # Session drifted into a subdirectory via cd; the gate must still find the
    # project-root config through CLAUDE_PROJECT_DIR.
    result = run_hook(
        "stop_gate.py",
        {"cwd": str(elsewhere), "stop_hook_active": False},
        cwd=elsewhere,
        project_dir=tmp_path,
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["decision"] == "block"


def test_settings_template_hook_command_uses_project_dir_anchor():
    settings = json.loads((KIT / "settings.json.template").read_text(encoding="utf-8"))
    command = settings["hooks"]["Stop"][0]["hooks"][0]["command"]
    assert "CLAUDE_PROJECT_DIR" in command


def test_stop_gate_allows_stop_when_checks_pass(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "stop-gate.json").write_text(
        json.dumps({"checks": [{"name": "ok", "command": "true"}]}), encoding="utf-8"
    )

    result = run_hook("stop_gate.py", {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_learn_gate_fires_exactly_once_per_session(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text("{}\n" * 100, encoding="utf-8")
    event = {
        "cwd": str(tmp_path),
        "stop_hook_active": False,
        "session_id": f"test-{uuid.uuid4().hex}",
        "transcript_path": str(transcript),
    }

    first = run_hook("learn_gate.py", event, tmp_path)
    assert first.returncode == 0
    assert json.loads(first.stdout)["decision"] == "block"

    second = run_hook("learn_gate.py", event, tmp_path)
    assert second.returncode == 0
    assert second.stdout.strip() == ""


def test_learn_gate_skips_trivial_sessions(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text("{}\n" * 3, encoding="utf-8")
    event = {
        "cwd": str(tmp_path),
        "stop_hook_active": False,
        "session_id": f"test-{uuid.uuid4().hex}",
        "transcript_path": str(transcript),
    }

    result = run_hook("learn_gate.py", event, tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_claude_kit_installs_into_dot_claude(tmp_path):
    module = load_init_module()
    files = module.plan_claude_kit(tmp_path)
    module.write_files(files, force=False)

    for agent in EXPECTED_AGENTS:
        assert (tmp_path / ".claude" / "agents" / f"{agent}.md").is_file()
    assert (tmp_path / ".claude" / "hooks" / "stop_gate.py").is_file()
    assert (tmp_path / ".claude" / "skills" / "retro" / "SKILL.md").is_file()
    # Template becomes the live settings.json when none exists.
    assert (tmp_path / ".claude" / "settings.json").is_file()
    assert not (tmp_path / ".claude" / "settings.json.template").exists()


def test_claude_kit_never_replaces_existing_settings(tmp_path):
    module = load_init_module()
    existing = tmp_path / ".claude" / "settings.json"
    existing.parent.mkdir(parents=True)
    existing.write_text('{"permissions": {}}', encoding="utf-8")

    files = module.plan_claude_kit(tmp_path)
    module.write_files(files, force=False)

    assert existing.read_text(encoding="utf-8") == '{"permissions": {}}'
    assert (tmp_path / ".claude" / "settings.json.template").is_file()


def test_stop_gate_reports_malformed_check_entry_instead_of_crashing(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "stop-gate.json").write_text(
        json.dumps({"checks": ["not-an-object", {"name": "ok", "command": "true"}]}),
        encoding="utf-8",
    )

    result = run_hook("stop_gate.py", {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["decision"] == "block"
    assert "invalid entry" in output["reason"]


def test_learn_gate_marker_is_scoped_per_project(tmp_path):
    session = f"test-{uuid.uuid4().hex}"
    for project in ["proj_a", "proj_b"]:
        root = tmp_path / project
        root.mkdir()
        transcript = root / "transcript.jsonl"
        transcript.write_text("{}\n" * 100, encoding="utf-8")
        event = {
            "cwd": str(root),
            "stop_hook_active": False,
            "session_id": session,
            "transcript_path": str(transcript),
        }
        result = run_hook("learn_gate.py", event, root, project_dir=root)
        assert json.loads(result.stdout)["decision"] == "block", f"gate did not fire in {project}"
