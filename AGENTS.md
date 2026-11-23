# Working in software-recipes

This repo ships agent skills as one plugin for Claude Code, Codex and GitHub Copilot.

## Layout rules

- `skills/<name>/SKILL.md` holds only **shipped** skills, one flat level deep. Codex and Copilot discover every `SKILL.md` under `skills/`, so anything unfinished lives in `drafts/<name>/` instead.
- No symlinks inside `skills/`: Codex drops them when it copies a plugin into its cache.
- `recipes.toml` and each `SKILL.md` are the single source of truth. These files are **generated** by `make build` and are never hand-edited: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/*/agents/openai.yaml`, and the root `plugin.json` when that target is on.
- Run `make check` before committing. It fails on lint errors and on stale generated files.

## Writing a skill

- Frontmatter is plain one-line scalars plus an optional `metadata:` map (`display-name`, `short-description`). No block scalars, no lists.
- Every value must be valid YAML. Wrap a value in double quotes when it contains `: ` or ` #`, ends with `:`, or starts with a YAML indicator such as `-`, `[`, `&` or `*`. `make check` rejects the unquoted form.
- **Model-invoked** (default): the description is model-facing and ends with `Use when ...` triggers, one per distinct case.
- **User-invoked**: add `disable-model-invocation: true` and write the description as a one-line human summary. The build adds the matching Codex policy.
- Keep `SKILL.md` to the steps every run needs. Push reference that only some runs need into `references/` behind a link that says when to read it.
- End every step on a completion criterion the agent can check.
- Model-invoked skills carry `evals/triggers.json` with prompts that should and should not fire the skill.
- To call another skill, write `Call the Skill tool with "<name>"`; never link across skill folders.
- No em dashes in any prose.
