# Claude Executive Report: Large-Codebase Workflow Research

## Purpose

This report is a handoff for a downstream Claude research pass. It summarizes
what this repository already covers, what changed in the large-codebase
readiness work, and which external claims still need validation against current
primary sources.

The goal is to prevent the next agent from rediscovering this small repo from
scratch. Start from the local file pointers below, then validate only the
external surfaces that can drift.

## Repo Baseline

The repository ships one portable skill:

- `ultimate-agentic-workflow/SKILL.md`: the short skill entrypoint.
- `ultimate-agentic-workflow/references/workflow.md`: detailed lifecycle,
  traceability, review, context-loading, and archive policy.
- `ultimate-agentic-workflow/scripts/init_agents.py`: deterministic generation
  of tiny Codex or Claude bootloaders.
- `ultimate-agentic-workflow/assets/templates/`: generated `AGENTS.md`,
  `CLAUDE.md`, and `OPS.md` templates.

The workflow already covers:

- tiny bootloaders instead of huge always-loaded instruction files;
- T0-T3 task classification;
- source ledgers, risk registers, claim ledgers, verification ledgers, review
  records, reflection, and archive notes;
- packet ownership for multi-agent work;
- progressive context hydration instead of broad upfront file loading;
- permission-gated setup for dependency installs, `.codex`, `.claude`, MCP
  config, and dependent GitHub clones.

## Large-Codebase Additions

The large-codebase layer adds:

- `ultimate-agentic-workflow/references/large-codebase.md`
- `ultimate-agentic-workflow/references/pilot-measurement.md`
- `ultimate-agentic-workflow/scripts/large_codebase_tools.py`

The readiness script is intentionally read-only. It counts repo/language
signals, checks `PATH` for tools, recommends whether Serena-like symbol tooling
is worth considering, and emits approval-request text with exact setup commands
when a missing tool appears useful.

It does not install Serena, edit `.codex`, edit `.claude`, mutate MCP config,
run package managers, or clone repositories.

## Post-Research Corrections

Treat these as corrections to over-broad or stale claims that appeared during
the research phase:

- Ponytail should not be presented as a default recommendation without current
  primary-source validation and a clear fit against this workflow's needs.
- Serena is useful for symbol navigation on large or unfamiliar codebases, but
  it should stay optional and permission-gated until the target repo shape
  justifies it.
- The semantic search path is a fallback for vocabulary mismatch, not a first
  retrieval step. Exact search, symbol navigation, and structural search should
  come first.
- WarpGrep/Morph is hosted tooling. Any recommendation must include data-path,
  API-key, and code-leaves-machine considerations.
- Efficiency claims are hypotheses until measured with the pilot protocol in
  `ultimate-agentic-workflow/references/pilot-measurement.md`.

## External Validation Targets

Claude should validate these against current primary sources before repeating
them:

- Serena install and client setup, including Codex and Claude Code contexts.
- Codex MCP configuration, approvals, and tool filtering.
- Claude Code MCP scopes, permissions, and skills behavior.
- ast-grep install options and structural-search behavior.
- grepai local-index behavior and Ollama embedding setup.
- Ollama install and model pull commands.
- WarpGrep/Morph MCP setup, hosted data path, and API-key requirements.
- Any current claims about Ponytail or alternative context/code-search tools.

## Suggested Claude Prompt

```text
Read README.md, ultimate-agentic-workflow/SKILL.md,
ultimate-agentic-workflow/references/workflow.md,
ultimate-agentic-workflow/references/large-codebase.md,
ultimate-agentic-workflow/references/pilot-measurement.md, and
ultimate-agentic-workflow/scripts/large_codebase_tools.py.

Then validate the external tool claims against current primary sources. Do not
rewrite the workflow unless the repo-local claims are wrong. Return:
1. confirmed claims,
2. stale or unsupported claims,
3. data-path or permission risks,
4. recommended doc or script changes with file:line evidence.
```

## Keep In Mind

This repository is the routing/accountability layer. Large-codebase acceleration
is an overlay. The main agent still owns requirements, risk, integration,
verification, and final claims.
