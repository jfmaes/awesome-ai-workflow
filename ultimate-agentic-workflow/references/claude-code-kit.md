# Claude Code Starter Kit

The skill ships an installable `.claude/` kit: five subagents, two Stop hooks, two skills, and a settings template. Install it into a target repo with:

```bash
python3 ultimate-agentic-workflow/scripts/init_agents.py --cli claude --claude-kit --project-root .
```

(`--claude-kit` also works with `--cli both`.) The installer copies `assets/claude/` into the target's `.claude/` directory and refuses to overwrite existing files unless `--force` is passed. Everything is optional and individually deletable.

## Contents

- Subagents
- Hooks
- Skills
- Settings Template
- Goal Loops
- Context Meter

## Subagents

Installed to `.claude/agents/`. Each is deliberately narrow; delegation is driven by the `description` field.

| Agent | Role | Tools |
| --- | --- | --- |
| `code-reviewer` | Spec-compliance, correctness, security, simplicity review of diffs | read-only + Bash |
| `skeptic-verifier` | Adversarially refutes "done" claims and load-bearing findings | read-only + Bash |
| `test-runner` | Runs checks, absorbs verbose output, returns failures only (haiku-class) | read-only + Bash |
| `researcher` | Bounded read-only discovery with `file:line` evidence | read-only + web |
| `implementer` | One approved task, TDD, disjoint write scope | full |

These map onto the execution modes in `workflow.md` and the patterns in `orchestration.md`: implementer + code-reviewer + skeptic-verifier is subagent-driven development with fresh-context review; test-runner and researcher are context-isolation workers.

Worktree isolation for parallel implementers is the dispatcher's job: create the worktree (`git worktree add`) and name it in the packet before dispatch. The implementer's rules tell it to refuse parallel edits without one. (Frontmatter-level isolation fields are not portable across Claude Code versions, so the kit does not rely on them.)

## Hooks

Installed to `.claude/hooks/`. Both honor `stop_hook_active`, and Claude Code's built-in cap (a Stop hook is overridden after 8 consecutive blocks without progress) is the runaway backstop.

**`stop_gate.py` — deterministic completion gate.** Wired in the settings template. Reads `.claude/stop-gate.json`; with no config it is a no-op. When checks are configured, the agent cannot stop while they fail:

```json
{
  "checks": [
    {"name": "tests", "command": "npm test"},
    {"name": "lint", "command": "npm run lint"}
  ]
}
```

Use it for anything a script can verify exactly. This converts "the agent should verify before claiming completion" into "the harness will not let it stop otherwise" — the deterministic-gates principle from `workflow.md`.

**`learn_gate.py` — optional learning gate.** Not wired by default. Once per substantive session, it blocks the first stop and asks the agent to run the `/retro` skill, so lessons get captured before the session ends instead of never. (Original implementation of the session-learning concept popularized by the community `/teach` and `/reflect` skills and compound engineering's `/compound` step.) Enable it by adding a second Stop entry to `.claude/settings.json`:

```json
{"type": "command", "command": "python3 \"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/learn_gate.py\""}
```

(Hook commands run from the session's current directory, which drifts when the agent uses `cd` — always anchor hook paths on `CLAUDE_PROJECT_DIR`, as the shipped template does.)

## Skills

Installed to `.claude/skills/`.

- **`/retro`** — session retrospective: mines the session for durable lessons, routes each to the right home (OPS.md one-liners, skill/subagent/hook candidates, debt entries, decision docs), applies the cheap ones with approval, and is honest when there is nothing worth keeping. This is the compounding step: repos that run it get smarter every session.
- **`/mint-skill`** — creates a new skill or subagent from a repeated workflow: picks the right primitive (skill vs subagent vs hook vs MCP), enforces the authoring quality bar, and tunes the trigger description against realistic should/should-not-fire prompts. Manual-invocation only.

## Settings Template

`settings.json.template` is a minimal committed-`settings.json` starting point: safe read-only git allowances, `.env`/secrets deny rules, and the stop gate wired. Machine-specific overrides belong in `.claude/settings.local.json` (gitignored). The installer will not replace an existing `settings.json`; it writes the template alongside as `settings.json.template` for manual merge instead.

## Goal Loops

Three tools, in order of preference:

1. **Deterministic conditions** ("tests pass", "lint clean") → `stop_gate.py`. A script checks it exactly; no model judgment, no token cost.
2. **Judgment conditions** ("the README explains X clearly", "all review comments addressed") → the built-in `/goal` command. It wires a prompt-based Stop hook judged by a small model that re-injects the unmet condition as guidance each turn. Do not hand-roll this; the built-in handles loop safety.
3. **Batch mechanical work over a strong plan** → an autonomous loop per the policy in `workflow.md`, with the stop conditions from `orchestration.md`. The stop gate doubles as the loop's success gate.

Write goal conditions so evidence appears in the transcript (the judge sees only what the agent surfaced), and give every loop a budget cap.

## Context Meter

If context pressure is a recurring problem in long sessions, a statusline that reads real token usage from the session transcript (rather than estimating) is a cheap addition — see the community `headroom` statusline hook for a reference implementation, and `context-engineering.md` for the behavioral half of the fix.
