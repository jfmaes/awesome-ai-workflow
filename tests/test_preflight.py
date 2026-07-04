import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "ultimate-agentic-workflow" / "scripts"


def load_preflight(offline: bool = True):
    spec = importlib.util.spec_from_file_location("preflight", SCRIPTS / "preflight.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    if offline:
        # Deterministic: never shell out to git/claude in unit tests.
        module.run_quiet = lambda command, timeout=10: None
    return module


def load_init():
    spec = importlib.util.spec_from_file_location("init_agents", SCRIPTS / "init_agents.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_empty_repo_gets_ordered_bootstrap_steps(tmp_path):
    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    steps = "\n".join(report["next_steps"])
    assert "init_agents.py --cli both --claude-kit" in steps
    assert "git init" in steps
    assert "superpowers" in steps.lower()
    assert report["frameworks"]["superpowers"]["installed"] is False
    assert report["frameworks"]["gsd"]["installed"] is False
    # Bootstrap must come before optional framework installs.
    assert steps.index("init_agents.py") < steps.lower().index("superpowers")


def test_foreign_bootloader_gets_merge_advice_not_overwrite(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# My own instructions\n", encoding="utf-8")
    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["repo"]["bootloader_claude"] == "foreign"
    steps = "\n".join(report["next_steps"])
    assert "--stdout" in steps
    assert "Do not overwrite" in steps


def test_our_bootstrap_is_recognized_and_stop_gate_config_suggested(tmp_path):
    init = load_init()
    files = init.plan_files("claude", tmp_path, init.detect_context(tmp_path))
    files.update(init.plan_claude_kit(tmp_path))
    init.write_files(files, force=False)

    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["repo"]["bootloader_claude"] == "ours"
    assert len(report["repo"]["kit_agents_present"]) == 5
    steps = "\n".join(report["next_steps"])
    assert "stop-gate.json" in steps


def test_gsd_detected_via_planning_marker(tmp_path):
    (tmp_path / ".planning").mkdir()
    (tmp_path / ".planning" / "config.json").write_text("{}", encoding="utf-8")
    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["frameworks"]["gsd"]["installed"] is True
    assert "gsd-core" not in "\n".join(report["next_steps"])


def test_superpowers_detected_via_plugin_cache(tmp_path):
    home = tmp_path / "fakehome"
    (home / ".claude" / "plugins" / "cache" / "claude-plugins-official" / "superpowers" / "6.1.1").mkdir(
        parents=True
    )
    module = load_preflight()
    report = module.build_report(tmp_path, home=home)

    assert report["frameworks"]["superpowers"]["installed"] is True
    assert report["frameworks"]["superpowers"]["detected_via"] == "plugin cache"


def test_cli_json_mode_and_nonexistent_root(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "preflight.py"), "--project-root", str(tmp_path), "--json"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["mode"] == "read-only-preflight"
    assert report["next_steps"]

    missing = subprocess.run(
        [sys.executable, str(SCRIPTS / "preflight.py"), "--project-root", str(tmp_path / "nope")],
        text=True,
        capture_output=True,
    )
    assert missing.returncode != 0


def test_generated_ops_is_recognized_as_ours(tmp_path):
    init = load_init()
    init.write_files(init.plan_files("claude", tmp_path, init.detect_context(tmp_path)), force=False)
    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["repo"]["ops"] == "ours"


def test_unwired_stop_gate_is_flagged_when_settings_predates_kit(tmp_path):
    # A repo with a pre-existing settings.json: the kit installer must not touch
    # it, and preflight must say the gate is NOT running.
    existing = tmp_path / ".claude" / "settings.json"
    existing.parent.mkdir(parents=True)
    existing.write_text('{"permissions": {}}', encoding="utf-8")

    init = load_init()
    init.write_files(init.plan_claude_kit(tmp_path), force=False)
    (tmp_path / ".claude" / "stop-gate.json").write_text('{"checks": []}', encoding="utf-8")

    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["repo"]["stop_gate_wired"] is False
    steps = "\n".join(report["next_steps"])
    assert "NOT wired" in steps


def test_wired_stop_gate_detected_from_template_settings(tmp_path):
    init = load_init()
    init.write_files(init.plan_claude_kit(tmp_path), force=False)
    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["repo"]["stop_gate_wired"] is True


def test_v1_claude_layout_gets_migration_steps(tmp_path):
    # Faithful v1 fixture: CLAUDE.md bootloader (with skill marker) and
    # AGENTS.md in its old operational-guide role; no OPS.md.
    (tmp_path / "CLAUDE.md").write_text(
        "# Agent Autopilot\n\nThis repo uses the `ultimate-agentic-workflow` skill.\n",
        encoding="utf-8",
    )
    (tmp_path / "AGENTS.md").write_text(
        "# Operational Guide\n\nKeep this file under 60 lines.\n## Validation\n- Test: `pytest`\n",
        encoding="utf-8",
    )

    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["repo"]["v1_claude_layout"] is True
    steps = "\n".join(report["next_steps"])
    assert "git mv AGENTS.md OPS.md" in steps
    assert "--skip-existing" in steps
    # Migration guidance replaces the generic foreign-file merge advice.
    assert "Do not overwrite" not in steps


def test_v2_layouts_are_not_misdetected_as_v1(tmp_path):
    init = load_init()
    init.write_files(init.plan_files("both", tmp_path, init.detect_context(tmp_path)), force=False)

    module = load_preflight()
    report = module.build_report(tmp_path, home=tmp_path / "fakehome")

    assert report["repo"]["v1_claude_layout"] is False
