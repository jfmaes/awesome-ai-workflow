0a. Study `specs/*` with up to 500 parallel subagents to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md.
0c. Study @AGENTS.md for operational context and validation commands.
0d. For reference, the application source code is in `src/*`.
0e. Study the **Rules** section and the **Stack** section matching this project's language from ~/AI_RETRO.md. Ignore other sections.

1. Your task is to implement functionality per the specifications using parallel subagents. Follow @IMPLEMENTATION_PLAN.md and choose the most important item to address. Tasks include required tests — implement tests as part of task scope. Before making changes, search the codebase (don't assume not implemented) using subagents. You may use up to 500 parallel subagents for searches/reads and only 1 subagent for build/tests. Use Opus subagents when complex reasoning is needed (debugging, architectural decisions).

2. After implementing functionality or resolving problems, run all required tests specified in the task definition. All required tests must exist and pass before the task is considered complete. If functionality is missing then it's your job to add it as per the application specifications. Ultrathink.

3. When you discover issues, immediately update @IMPLEMENTATION_PLAN.md with your findings using a subagent. When resolved, update and remove the item.

4. When the tests pass, update @IMPLEMENTATION_PLAN.md, then `git add -A` then `git commit` with a message describing the changes. After the commit, `git push`.

999. Required tests derived from acceptance criteria must exist and pass before committing. Tests are part of implementation scope, not optional.
9999. Important: When authoring documentation, capture the why — tests and implementation importance.
99999. Important: Single sources of truth, no migrations/adapters. If tests unrelated to your work fail, resolve them as part of the increment.
999999. Keep @IMPLEMENTATION_PLAN.md current with learnings using a subagent — future work depends on this to avoid duplicating efforts. Update especially after finishing your turn.
9999999. When you learn something new about how to run the application, update @AGENTS.md using a subagent but keep it brief.
99999999. For any bugs you notice, resolve them or document them in @IMPLEMENTATION_PLAN.md using a subagent even if unrelated to current work.
999999999. Implement functionality completely. Placeholders and stubs waste efforts and time redoing the same work.
9999999999. When @IMPLEMENTATION_PLAN.md becomes large, periodically clean out completed items using a subagent.
99999999999. If you find inconsistencies in specs/*, use an Opus subagent with ultrathink to update the specs.
999999999999. IMPORTANT: Keep @AGENTS.md operational only — status updates and progress notes belong in IMPLEMENTATION_PLAN.md. A bloated AGENTS.md pollutes every future loop's context.
