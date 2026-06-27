from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_large_codebase_reference_covers_tool_routing_and_permissioned_setup():
    content = read("ultimate-agentic-workflow/references/large-codebase.md")

    required = [
        "Search Modality Routing",
        "`rg`",
        "Serena",
        "ast-grep",
        "grepai",
        "WarpGrep",
        "read-first",
        "Permission-Gated Setup",
        "large_codebase_tools.py",
        ".codex",
        ".claude",
        "git clone",
        "code leaves the machine",
    ]

    for phrase in required:
        assert phrase in content


def test_pilot_reference_keeps_efficiency_claims_hypotheses_until_measured():
    content = read("ultimate-agentic-workflow/references/pilot-measurement.md")

    required = [
        "A/B",
        "baseline",
        "treatment",
        "tool calls",
        "files read",
        "lines read",
        "tokens",
        "wall-clock",
        "diff size",
        "hidden tests",
        "hypotheses",
    ]

    for phrase in required:
        assert phrase in content


def test_skill_points_large_unfamiliar_codebases_to_on_demand_references():
    content = read("ultimate-agentic-workflow/SKILL.md")

    assert "large or unfamiliar codebases" in content
    assert "references/large-codebase.md" in content
    assert "references/pilot-measurement.md" in content


def test_workflow_adds_retrieval_policy_and_simplicity_gate():
    content = read("ultimate-agentic-workflow/references/workflow.md")

    required = [
        "Search routing policy",
        "Known string",
        "Definition, references, callers, or safe rename",
        "Structural pattern",
        "Fuzzy concept",
        "Simplicity gate",
        "already exists in the repo",
        "smallest safe diff",
    ]

    for phrase in required:
        assert phrase in content


def test_report_records_post_research_corrections():
    content = read("CLAUDE_EXEC_REPORT.md")

    required = [
        "Post-Research Corrections",
        "Ponytail",
        "Serena",
        "semantic search",
        "hypotheses",
    ]

    for phrase in required:
        assert phrase in content


def test_generated_agent_templates_include_permissioned_dependency_protocols():
    codex = read("ultimate-agentic-workflow/assets/templates/AGENTS.md.codex.template")
    claude = read("ultimate-agentic-workflow/assets/templates/CLAUDE.md.template")
    ops = read("ultimate-agentic-workflow/assets/templates/OPS.md.template")

    for content, marker in [(codex, ".codex"), (claude, ".claude")]:
        assert "Permissioned Setup" in content
        assert marker in content
        assert "user approval" in content
        assert "GitHub" in content
        assert "rollback" in content

    assert "Dependency And Repo Setup" in ops
    assert ".codex" in ops
    assert ".claude" in ops
    assert "git clone" in ops
