---
name: mint-skill
description: Create a new Claude Code skill or subagent from a repeated workflow, with trigger-description tuning and a quality checklist. Use when a workflow has been performed manually two or more times, when /retro proposes a skill candidate, or when the user asks to make something reusable.
disable-model-invocation: true
---

# Mint Skill

Crystallize a repeated workflow into a skill or subagent that actually triggers when it should.

## Step 1: Choose the right primitive

| Signal | Primitive |
| --- | --- |
| Reusable prompt/workflow that should run in the main conversation | Skill (`.claude/skills/<name>/SKILL.md`) |
| Work with verbose output, restricted tools, or a fresh-context requirement | Subagent (`.claude/agents/<name>.md`) |
| A rule that must be enforced every time, not remembered | Hook (settings.json) or `stop-gate.json` check |
| External system integration | MCP server — do not wrap it in a skill |

Before building: check whether an existing skill in this repo, the user's collection, or a well-known community catalog already covers it. Duplicating a battle-tested skill is slop.

## Step 2: Draft

- Skill body under ~150 lines; anything longer goes in reference files exactly one level deep, each with a Contents section if over 100 lines.
- Do not explain what a capable model already knows; write the delta.
- One default path plus an escape hatch — not an option menu.
- Multi-step flows get a literal `- [ ]` checklist.
- Side-effecting skills (deploy, publish, commit) get `disable-model-invocation: true`.
- Subagents get the minimum tool set that does the job (reviewers and verifiers get no Edit/Write).

## Step 3: Tune the trigger description

The `description` is the single biggest lever on whether the skill fires. It must be third person, state what the skill does AND when to use it, and contain the concrete words a user would actually say.

Test it: write 3-5 realistic prompts that SHOULD trigger it and 2-3 that should NOT. Walk through each against the description; if a should-trigger prompt shares no vocabulary with the description, rewrite the description — not the prompt.

## Step 4: Validate before shipping

- [ ] Frontmatter parses; name matches directory; description passes the trigger test above.
- [ ] A fresh session (or fresh subagent) can follow the skill without conversation context.
- [ ] The skill was tried on one real task end to end.
- [ ] User approved the final file location and content.
