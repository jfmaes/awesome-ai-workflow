# Large Codebase Acceleration

## Contents

- Search Modality Routing
- Large-Repo Intake Checklist
- Adaptive Tool Readiness
- Tool Install Catalog
- Context-Budget Policy
- Serena Integration
- Semantic Search
- Permission-Gated Setup
- Sources

Use this reference only when the repo is large, unfamiliar, polyglot, or the task needs cross-file navigation. Keep the main agent first: it owns requirements, decisions, risk, integration, and final verification. Helper tools and subagents only narrow search space and return concise findings with `file:line` evidence.

## Search Modality Routing

| Need | First Tool | Trigger Signal | Stop Condition |
| --- | --- | --- | --- |
| Known string / literal / fast scan | `rg` | You know a symbol, phrase, route, env var, error text, or filename fragment. | A small set of files or lines is identified. |
| Definition, references, callers, or safe rename | Serena or native LSP/code-intelligence tools | You need symbol graph facts: who calls this, where defined, implementations, references, rename impact. | Symbol locations and impacted files are known. |
| Structural pattern | `ast-grep`, tree-sitter, or language-aware parser | Shape matters more than text: decorator on class, nested call, unsafe API pattern, import form. | Matching syntax nodes are identified. |
| Fuzzy concept, unknown vocabulary | semantic search such as grepai | Exact text and symbol search failed or vocabulary is unknown. This is a last resort, not a default. | Candidate files are found, then verify with source reads. |

Do not read broad files just because a search returns many hits. Narrow first, then read the smallest source span that can answer the question.

## Large-Repo Intake Checklist

- Size and languages: total files, dominant languages, generated/vendor directories, monorepo boundaries.
- Source and test roots: package/workspace layout, owners, local conventions, nested instructions.
- Index availability: existing LSP, Serena project, grepai index, ctags, generated docs, build metadata.
- Ignore policy: `node_modules`, `.venv`, `vendor`, `dist`, `build`, generated clients, snapshots, fixture dumps.
- Validation commands: focused test, wider regression check, build/typecheck/lint, known slow or flaky gates.
- Existing memory: `AGENTS.md`, `CLAUDE.md`, `OPS.md`, `memory-bank`, active plans, `.workflow` runs.

## Adaptive Tool Readiness

When a repo looks large, unfamiliar, polyglot, or cross-file navigation heavy, run the read-only readiness check before adding tools:

```bash
python3 <skill-dir>/scripts/large_codebase_tools.py --project-root . --json
```

The script:

- counts codebase signals while ignoring generated/vendor directories;
- checks whether `uv`, `rg`, Serena, `ast-grep`, grepai, Ollama, and hosted WarpGrep/Morph setup are available or relevant;
- recommends Serena only when large-codebase signals overlap with Serena-supported languages;
- drafts an approval request when Serena appears useful but is missing;
- documents install/config commands for each identified tool;
- executes no install, MCP config, package-manager, or `git clone` command.

The agent should read the JSON, decide whether the task actually needs the missing tool, and ask the user before running any listed install or configuration command.

## Tool Install Catalog

These commands are documentation and approval-plan inputs. Do not run them until the user approves the exact commands and write/network targets. The authoritative machine-readable catalog is `TOOL_CATALOG` in `scripts/large_codebase_tools.py`; if this table and the script disagree, trust the script.

| Tool | Use When | Install / Setup |
| --- | --- | --- |
| `uv` | Serena install path needs the Python tool manager. | `curl -LsSf https://astral.sh/uv/install.sh \| sh`; `brew install uv`; or `pipx install uv`. |
| `rg` / ripgrep | Default exact-text search. | `brew install ripgrep`; `sudo apt-get install ripgrep`; or `cargo install ripgrep`. |
| Serena | Large/unfamiliar codebase symbol navigation. | `uv tool install -p 3.13 serena-agent`; `serena init`; then Codex/Claude MCP setup below. |
| `ast-grep` | Structural search or safe syntax-shaped rewrites. | `npm install --global @ast-grep/cli`; `pip install ast-grep-cli`; `brew install ast-grep`; or `cargo install ast-grep --locked`. |
| grepai | Local semantic search after exact/symbol/structural search fails. | `brew install yoanbernabeu/tap/grepai` or `curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh \| sh`; then `ollama pull nomic-embed-text`, `grepai init`, `grepai watch`. |
| Ollama | Local embedding provider for grepai. | `curl -fsSL https://ollama.com/install.sh \| sh`; then `ollama pull nomic-embed-text`. |
| WarpGrep / Morph MCP | Hosted search only when local search is insufficient and the data path is approved. | `codex mcp add morph --env MORPH_API_KEY=YOUR_API_KEY -- npx --prefer-offline -y @morphllm/morphmcp` or Claude equivalent. |

## Context-Budget Policy

The general policy (who keeps what, bounded questions in, `file:line` summaries out) lives in `context-engineering.md`. Specific to large repos:

- Prefer `rg` output, symbol summaries, and line-scoped reads before full-file reads.
- Do not load MCP servers or semantic indexes by default. Add them only when the routing table says they are useful.

## Serena Integration

Use Serena as an optional LSP-backed navigation layer for large or unfamiliar codebases. Start read-first: navigation and symbol-overview tools are acceptable earlier than refactor/edit tools. Do not use Serena write/refactor tools until the task plan names them and the normal edit/test workflow is in place.

Install Serena:

```bash
uv tool install -p 3.13 serena-agent
serena init
```

### Codex

Fast path:

```bash
serena setup codex
```

Manual `~/.codex/config.toml` or trusted project `.codex/config.toml`:

```toml
[mcp_servers.serena]
startup_timeout_sec = 15
command = "serena"
args = ["start-mcp-server", "--project-from-cwd", "--context=codex"]
default_tools_approval_mode = "prompt"
```

Codex supports MCP `enabled_tools` and `disabled_tools`; use those when you need a read-first allow list. Keep write-capable MCP tools prompting by default.

### Claude Code

Global user setup:

```bash
claude mcp add --scope user serena -- serena start-mcp-server --context claude-code --project-from-cwd
```

Project-pinned setup:

```bash
claude mcp add serena -- serena start-mcp-server --context claude-code --project "$(pwd)"
```

Claude Code supports permission settings, skill `allowed-tools`/`disallowed-tools`, and subagent tool fields. Treat those as guardrails, not as a reason to bypass review or tests.

### Caveats

- Launching a user-scoped `--project-from-cwd` server from `$HOME` can make Serena scan the home directory and time out. Prefer starting from the repo root or using a project-pinned config.
- Do not cite token-savings numbers for Serena until this repo runs the pilot in `pilot-measurement.md`.
- Prefer the client-specific context (`codex`, `claude-code`) so duplicate or irrelevant tools are stripped.

## Semantic Search

Use semantic search only after exact text, symbol graph, and structural search fail or when the task is genuinely vocabulary-mismatched.

### grepai Privacy Default

grepai is the default semantic option because it is local-first and can use Ollama embeddings.

Typical setup:

```bash
ollama pull nomic-embed-text
grepai init
grepai watch
grepai mcp-serve
```

The index must exist before an agent can rely on semantic results. Treat results as candidates and verify by reading source.

### WarpGrep Hosted Alternative

WarpGrep is useful when hosted agentic search is acceptable, but it requires Morph setup and an API key. For local code search, ripgrep is still a prerequisite. Its GitHub search can inspect public repositories without cloning, but code or query context may leave the machine. Use it only after explicit user approval for that data path.

## Permission-Gated Setup

Agents may prepare dependency and repo setup plans autonomously, but must ask before executing any command that mutates `.codex`, `.claude`, home config, global tools, package caches, or external GitHub checkouts.

The approval request must name:

- exact commands, including `pip`, `uv`, `npm`, `brew`, `ollama`, `claude mcp`, `codex mcp`, or `git clone`;
- exact write targets such as `~/.codex/config.toml`, `.codex/config.toml`, `~/.claude.json`, `.claude/settings.local.json`, `.mcp.json`, or `.workflow/deps/<repo>`;
- network destinations and whether code leaves the machine;
- credentials or API keys required, if any;
- rollback steps, including config backup paths and how to remove cloned repos.

Default clone location for dependent GitHub repos is `.workflow/deps/<owner>-<repo>/` unless the user names another directory. Never clone into source roots or overwrite an existing checkout without approval.

Safe pattern:

```text
1. Detect missing tool or repo.
2. Draft exact install or git clone commands.
3. Ask for user approval with paths, network, risk, and rollback.
4. Execute only the approved commands.
5. Verify tool availability or checkout SHA.
6. Record evidence in the source or verification ledger.
```

## Sources

- Serena client setup: https://oraios.github.io/serena/02-usage/030_clients.html
- Serena `--project-from-cwd` caveat: https://github.com/oraios/serena/issues/979
- Codex MCP config and tool filters: https://developers.openai.com/codex/mcp
- Codex approvals and security: https://developers.openai.com/codex/agent-approvals-security
- Claude Code MCP and scopes: https://code.claude.com/docs/en/mcp
- Claude Code feature/context model: https://code.claude.com/docs/en/features-overview
- Claude Code permissions and skills: https://code.claude.com/docs/en/permissions and https://code.claude.com/docs/en/skills
- grepai: https://github.com/yoanbernabeu/grepai
- WarpGrep and Morph MCP: https://docs.morphllm.com/sdk/components/warp-grep and https://docs.morphllm.com/mcpquickstart
