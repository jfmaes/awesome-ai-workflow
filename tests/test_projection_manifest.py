from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ultimate-agentic-workflow" / "artifact-manifest.json"
PLUGIN = ROOT / "ultimate-agentic-workflow" / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

EXPECTED_EXPORTS = [
    {
        "exportName": "ultimate-agentic-workflow",
        "exportRootRelativePath": "ultimate-agentic-workflow",
        "harnesses": ["claude", "codex"],
    },
    {
        "exportName": "evaluate-tech",
        "exportRootRelativePath": "ultimate-agentic-workflow/assets/claude/skills/evaluate-tech",
        "harnesses": ["claude", "codex"],
    },
    {
        "exportName": "deep-research",
        "exportRootRelativePath": "ultimate-agentic-workflow/assets/codex/skills/deep-research",
        "harnesses": ["codex"],
    },
]


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, member in pairs:
        if key in value:
            raise ValueError("duplicate key")
        value[key] = member
    return value


def load_strict(path: Path) -> object:
    raw = path.read_bytes()
    assert raw.endswith(b"\n") and not raw.startswith(b"\xef\xbb\xbf")
    return json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=unique_object)


def test_manifest_declares_exact_owned_exports_and_real_skill_roots() -> None:
    manifest = load_strict(MANIFEST)
    assert manifest == {
        "schemaVersion": 1,
        "owner": "awesome-ai-workflow",
        "exports": EXPECTED_EXPORTS,
    }
    for export in manifest["exports"]:
        root = ROOT / export["exportRootRelativePath"]
        assert root.is_dir()
        assert (root / "SKILL.md").is_file()
        assert ".codex" not in root.parts and "plugins/cache" not in root.as_posix()


def test_release_manifests_bind_the_same_explicit_version() -> None:
    plugin = load_strict(PLUGIN)
    marketplace = load_strict(MARKETPLACE)
    entry = next(row for row in marketplace["plugins"] if row["name"] == plugin["name"])
    assert plugin["version"] == "0.1.0"
    assert entry["version"] == plugin["version"]


def test_readme_uses_supported_codex_root_and_preserves_legacy_for_rollback() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "$HOME/.agents/skills" in readme
    assert "${CODEX_HOME:-$HOME/.codex}/skills" not in readme
    assert "legacy `~/.codex/skills`" in readme
    assert "read-only" in readme
