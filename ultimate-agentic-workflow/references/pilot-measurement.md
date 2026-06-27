# Pilot Measurement

Use this protocol before recommending Serena, grepai, WarpGrep, or any other acceleration tool as default-on. Efficiency claims stay hypotheses until this pilot produces evidence on the target repo class.

## Goal

Measure whether extra retrieval tooling reduces wasted exploration without lowering correctness, increasing risk, or bloating always-loaded context.

## A/B Design

Run the same task twice on isolated workspaces from the same base commit:

| Arm | Tooling | Rules |
| --- | --- | --- |
| baseline | `rg`, native file reads, existing project instructions | No new MCP or semantic index. |
| treatment | baseline plus the candidate tool, such as Serena or grepai | Use the search routing table from `large-codebase.md`; no write/refactor MCP tools unless the task explicitly requires them. |

Both arms must receive the same prompt, success criteria, hidden tests, timeout, and allowed write scope. If a human must answer a question in one arm, record the same answer in the other arm.

## Metrics

Record these from logs, shell history, harness output, or manual counters:

- correctness: focused tests, hidden tests, build/typecheck/lint, and requirement audit;
- wall-clock time from task start to verified patch;
- tool calls by category: search, read, edit, shell, MCP, browser, subagent;
- files read and lines read;
- tokens, if the client exposes them;
- diff size: files changed and lines added/deleted;
- number of failed commands or wrong turns;
- review findings: critical, important, minor;
- setup overhead: install time, indexing time, cache size, and cleanup required.

## Controls

- Use disposable branches or worktrees.
- Use identical base SHA and dependency state.
- Reset generated caches between arms unless the pilot is explicitly measuring warm-cache behavior.
- Keep the main agent first: helper tools may find context, but the controller owns decisions and verification.
- Do not let a hosted tool inspect private code unless the user approves that data path.

## Harness Notes

The `usamadar/coding-agent-benchmark` harness is useful as a starting point because it compares correctness and speed across coding-agent tasks, but this workflow also needs tool calls, files read, lines read, tokens, diff size, and review findings. Add those from agent logs or a wrapper script when the harness does not capture them.

## Decision Rule

Recommend a tool as default-on only when the treatment:

- matches or improves correctness;
- reduces at least two exploration-cost metrics, such as tool calls, files read, lines read, tokens, or wall-clock;
- does not introduce unresolved critical or important review findings;
- has an acceptable setup and cleanup burden;
- has a clear permission and data-handling story.

If results are mixed, document the narrower trigger where the tool helped. If results are negative or unmeasured, keep the tool optional and do not repeat vendor benchmark claims as local facts.

## Sources

- Pilot harness candidate: https://github.com/usamadar/coding-agent-benchmark
- Large-codebase routing policy: `large-codebase.md`
