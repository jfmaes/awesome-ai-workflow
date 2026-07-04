import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "ultimate-agentic-workflow"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_skill_routes_to_every_reference_one_level_deep():
    content = read("ultimate-agentic-workflow/SKILL.md")
    references = sorted(p.name for p in (SKILL / "references").glob("*.md"))

    assert references, "expected reference files to exist"
    for name in references:
        assert f"references/{name}" in content, f"SKILL.md does not route to {name}"


def test_skill_body_respects_progressive_disclosure_budget():
    lines = read("ultimate-agentic-workflow/SKILL.md").splitlines()
    assert len(lines) < 500


def test_long_references_carry_a_table_of_contents():
    for path in (SKILL / "references").glob("*.md"):
        content = path.read_text(encoding="utf-8")
        if len(content.splitlines()) > 100:
            assert "## Contents" in content, f"{path.name} needs a Contents section"


def test_workflow_defines_single_state_owner_per_tier():
    content = read("ultimate-agentic-workflow/references/workflow.md")

    assert "## State Ownership" in content
    assert "state.json" in content
    # The old contradiction: multiple live-state files with no assigned owner.
    assert "canonical" in content.lower()


def test_workflow_has_no_provenance_bloat_and_no_dead_script_references():
    content = read("ultimate-agentic-workflow/references/workflow.md")

    assert "Evidence Snapshot" not in content
    assert "What Each System Contributes" not in content
    assert "verify_workflow.py" not in content
    assert "verify_run.py" in content


def test_workflow_keeps_simplicity_gate_claim_gate_and_loop_stop_conditions():
    content = read("ultimate-agentic-workflow/references/workflow.md")

    required = [
        "Simplicity gate",
        "already exist in the repo",
        "smallest safe diff",
        "Completion claim gate",
        "fresh context",
        "Deterministic Gates",
        "stop conditions",
        "circuit breaker",
    ]
    for phrase in required:
        assert phrase in content, f"workflow.md missing: {phrase}"


def test_single_search_routing_table_lives_in_large_codebase_reference():
    large = read("ultimate-agentic-workflow/references/large-codebase.md")
    workflow = read("ultimate-agentic-workflow/references/workflow.md")
    readme = read("README.md")

    assert "Search Modality Routing" in large
    # The other documents point at it instead of duplicating the table.
    for content, name in [(workflow, "workflow.md"), (readme, "README.md")]:
        assert "Search Modality Routing" not in content, f"{name} duplicates the routing table"
        assert "large-codebase.md" in content


def headings(path: str) -> set[str]:
    return {
        line.strip()
        for line in read(path).splitlines()
        if line.strip().startswith("##")
    }


def test_orchestration_reference_keeps_its_section_contract():
    # Structural contract: SKILL.md routes agents here for these concerns, so
    # the sections must exist as real headings, not just mentioned words.
    found = headings("ultimate-agentic-workflow/references/orchestration.md")
    for section in [
        "## Fan-Out Sizing",
        "## Packet Contract",
        "## Worker Rules",
        "## Model and Effort Tiering",
        "## Verification Patterns",
        "## Judge Panel for Design Selection",
        "## Loop-Until-Dry Discovery",
        "## Autonomous Loop Stop Conditions",
    ]:
        assert section in found, f"orchestration.md lost section: {section}"


def test_context_engineering_reference_keeps_its_section_contract():
    found = headings("ultimate-agentic-workflow/references/context-engineering.md")
    for section in [
        "## Loading Policy",
        "## Durable Notes",
        "## Compaction Survival",
        "## Subagent Context Isolation",
        "## Tool-Output Hygiene",
        "## Altitude Control",
    ]:
        assert section in found, f"context-engineering.md lost section: {section}"


def test_tool_catalog_and_large_codebase_doc_stay_in_sync():
    spec = importlib.util.spec_from_file_location(
        "large_codebase_tools", SKILL / "scripts" / "large_codebase_tools.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    doc = read("ultimate-agentic-workflow/references/large-codebase.md").lower()
    aliases = {"uv": "uv", "ripgrep": "ripgrep", "warpgrep": "warpgrep"}
    for name in module.TOOL_CATALOG:
        assert aliases.get(name, name).lower() in doc, f"{name} missing from large-codebase.md"
    assert "tool_catalog" in doc, "doc must name TOOL_CATALOG as the authoritative source"


def test_generated_templates_include_permissioned_setup_and_durable_state():
    bootloader = read("ultimate-agentic-workflow/assets/templates/BOOTLOADER.md.template")
    ops = read("ultimate-agentic-workflow/assets/templates/OPS.md.template")

    assert "Permissioned Setup" in bootloader
    assert "user approval" in bootloader
    assert "rollback" in bootloader
    assert "compaction" in bootloader
    assert "fresh" in bootloader
    assert re.search(r"\{config_dir\}", bootloader)
    assert re.search(r"\{ops_file\}", bootloader)

    assert "Dependency And Repo Setup" in ops
    assert ".codex" in ops
    assert ".claude" in ops
    assert "git clone" in ops


def test_pilot_reference_keeps_efficiency_claims_hypotheses_until_measured():
    content = read("ultimate-agentic-workflow/references/pilot-measurement.md")

    for phrase in ["A/B", "baseline", "treatment", "wall-clock", "hypotheses"]:
        assert phrase in content


def test_skill_advertises_and_routes_v1_migration():
    content = read("ultimate-agentic-workflow/SKILL.md")
    frontmatter = content.split("---")[1]

    # Trigger vocabulary: "migrate/upgrade" requests must fire the skill.
    assert "migrating or upgrading" in frontmatter
    # And the body routes the agent to the mechanism that handles it.
    assert "migration steps" in content
    assert "git mv AGENTS.md OPS.md" in content
