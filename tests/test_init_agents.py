import importlib.util
import string
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ultimate-agentic-workflow" / "scripts" / "init_agents.py"
TEMPLATE_DIR = ROOT / "ultimate-agentic-workflow" / "assets" / "templates"


def load_module():
    spec = importlib.util.spec_from_file_location("init_agents", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def template_placeholders(template_name: str) -> set[str]:
    content = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
    return {
        field
        for _, field, _, _ in string.Formatter().parse(content)
        if field
    }


def test_template_placeholders_match_detect_context_contract():
    module = load_module()
    context_keys = set(module.detect_context(ROOT))
    bootloader_extra = {"config_dir", "ops_file"}

    assert template_placeholders("OPS.md.template") <= context_keys
    assert template_placeholders("BOOTLOADER.md.template") <= context_keys | bootloader_extra


def test_codex_init_writes_agents_and_ops(tmp_path):
    module = load_module()
    module.write_files(module.plan_files("codex", tmp_path, module.detect_context(tmp_path)), force=False)

    assert (tmp_path / "AGENTS.md").is_file()
    assert (tmp_path / "OPS.md").is_file()
    assert not (tmp_path / "CLAUDE.md").exists()
    assert ".codex" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")


def test_claude_init_does_not_touch_agents_md(tmp_path):
    module = load_module()
    module.write_files(module.plan_files("claude", tmp_path, module.detect_context(tmp_path)), force=False)

    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / "OPS.md").is_file()
    assert not (tmp_path / "AGENTS.md").exists()


def test_dual_cli_init_refuses_collision_and_writes_nothing(tmp_path):
    module = load_module()
    context = module.detect_context(tmp_path)
    module.write_files(module.plan_files("codex", tmp_path, context), force=False)
    agents_before = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    # Second init collides on OPS.md; it must refuse and leave everything untouched.
    with pytest.raises(SystemExit) as exc:
        module.write_files(module.plan_files("claude", tmp_path, context), force=False)
    assert "no files were written" in str(exc.value)
    assert not (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == agents_before

    # With --force it succeeds, and AGENTS.md keeps its bootloader role.
    module.write_files(module.plan_files("claude", tmp_path, context), force=True)
    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == agents_before


def test_both_writes_all_three_files(tmp_path):
    module = load_module()
    module.write_files(module.plan_files("both", tmp_path, module.detect_context(tmp_path)), force=False)

    for name in ["AGENTS.md", "CLAUDE.md", "OPS.md"]:
        assert (tmp_path / name).is_file()


def test_detects_rust_project(tmp_path):
    (tmp_path / "Cargo.toml").write_text("[package]\nname = \"demo\"\n", encoding="utf-8")
    module = load_module()
    context = module.detect_context(tmp_path)

    assert context["test_command"] == "cargo test"
    assert context["build_command"] == "cargo build"


def test_detects_go_project(tmp_path):
    (tmp_path / "go.mod").write_text("module demo\n", encoding="utf-8")
    (tmp_path / "cmd").mkdir()
    module = load_module()
    context = module.detect_context(tmp_path)

    assert context["test_command"] == "go test ./..."
    assert context["source_dir"] == "cmd"


def test_detects_pnpm_runner_and_does_not_conflate_check_script(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"name": "demo", "scripts": {"check": "tsc", "build": "vite build"}}',
        encoding="utf-8",
    )
    (tmp_path / "pnpm-lock.yaml").write_text("", encoding="utf-8")
    module = load_module()
    context = module.detect_context(tmp_path)

    assert context["build_command"] == "pnpm run build"
    # A lone "check" script must not silently become both test and typecheck.
    assert context["test_command"] != "pnpm run check"
    assert context["typecheck_command"] != "pnpm run check"


def test_non_object_package_json_does_not_crash(tmp_path):
    (tmp_path / "package.json").write_text("[]", encoding="utf-8")
    module = load_module()
    context = module.detect_context(tmp_path)

    assert context["project_name"] == tmp_path.name


def test_empty_object_package_json_still_detected_as_node(tmp_path):
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    (tmp_path / "pnpm-lock.yaml").write_text("", encoding="utf-8")
    module = load_module()
    context = module.detect_context(tmp_path)

    assert context["build_command"] == "pnpm run build"


def test_undetected_dirs_are_reported_honestly(tmp_path):
    module = load_module()
    context = module.detect_context(tmp_path)

    assert context["source_dir"] == "no standard directory detected (repo root?)"
    assert context["tests_dir"] == "no standard directory detected (repo root?)"


def test_force_refuses_directory_targets_before_writing_anything(tmp_path):
    (tmp_path / "CLAUDE.md").mkdir()
    module = load_module()
    context = module.detect_context(tmp_path)

    with pytest.raises(SystemExit) as exc:
        module.write_files(module.plan_files("claude", tmp_path, context), force=True)
    assert "no files were written" in str(exc.value)
    assert not (tmp_path / "OPS.md").exists()


def test_skip_existing_writes_only_missing_files(tmp_path):
    module = load_module()
    (tmp_path / "OPS.md").write_text("# my own ops\n", encoding="utf-8")
    context = module.detect_context(tmp_path)

    module.write_files(module.plan_files("claude", tmp_path, context), force=False, skip_existing=True)

    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / "OPS.md").read_text(encoding="utf-8") == "# my own ops\n"
