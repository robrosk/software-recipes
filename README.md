# software-recipes

Rob's agent skills for planning, building and verifying software. One repo, installable as a plugin on Claude Code, OpenAI Codex and GitHub Copilot.

## Install


**Claude Code**

```bash
claude plugin marketplace add robrosk/software-recipes
claude plugin install software-recipes@software-recipes
```

**Codex**

```bash
codex plugin marketplace add robrosk/software-recipes
codex plugin add software-recipes@software-recipes
```

**GitHub Copilot CLI**

```bash
copilot plugin marketplace add robrosk/software-recipes
copilot plugin install software-recipes@software-recipes
```

All three read the same `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`.

## Skills

**Model-invoked** (the agent reaches for these when the task fits)

- **[plan-the-change](./skills/plan-the-change/SKILL.md)**: Plan one change before coding it: goal as a check, modules, the simplest version and vertical slices. Reuses the design doc's patterns and never picks its own.
- **[surgical-diff-review](./skills/surgical-diff-review/SKILL.md)**: Check every changed line traces to the ask or plan; flag drift and missing verification.

**User-invoked** (only you can fire these, by typing `/name`)

- **[grill-the-plan](./skills/grill-the-plan/SKILL.md)**: Interview you one question at a time until the design is clear, then hand off to design-the-system for a big design or plan-the-change for a small change.
- **[design-the-system](./skills/design-the-system/SKILL.md)**: Pin down behavior, scale and robustness into a contract, draft the design yourself while the agent stress-tests it, and admit a pattern only where it rules out a named failure. The only skill that chooses design patterns.
- **[orchestrate-prs](./skills/orchestrate-prs/SKILL.md)**: Turn a signed-off design into one PR per component, each built by a subagent from a linted standalone work order, in dependency waves, gated by review before you merge.
- **[break-it](./skills/break-it/SKILL.md)**: Pin down how the system must behave, send ten computer-use hunters at the running app, triage what they find, and fix each confirmed bug in its own PR.
- **[garden](./skills/garden/SKILL.md)**: Sweep the codebase for drift from its design, rank the weeds by how far they would spread, and pull each one in its own small behavior-preserving PR; a weed that comes back becomes a lint rule.
- **[reflect](./skills/reflect/SKILL.md)**: Turn session lessons into proposed edits to skills, lint rules or notes.

The loop: `grill-the-plan` → `design-the-system` (a new system or cross-module change) or straight to `plan-the-change` (a small change) → build → `surgical-diff-review` → `break-it` → `garden` → `reflect`. Only `design-the-system` chooses design patterns; every later skill reuses its Patterns table. When `plan-the-change` departs from the design doc, the same PR updates the doc; a change to the signed contract needs your go-ahead and a concrete reason first.

For a large system, `orchestrate-prs` replaces the middle: `design-the-system` (required: it saves the design doc with the architecture and system-level behavior contract) → `orchestrate-prs` (waves of subagent PRs, each gated by `surgical-diff-review`, with a `garden` pass offered after each wave) → `break-it` → `reflect`.

## How the repo works

```
recipes.toml + skills/*/SKILL.md      single source of truth
        │
        ▼
tools/recipes  (load → validate → render)
        │
        ├── ClaudeAdapter          → .claude-plugin/plugin.json, marketplace.json
        ├── CodexSkillMetadata     → skills/*/agents/openai.yaml
        └── AgentPluginsAdapter    → plugin.json (off until verified)
```

```bash
make validate   # lint every SKILL.md
make build      # regenerate every platform file
make check      # tests + lint + fail on stale generated files (CI runs this)
```

Python 3.11+ standard library only. See [AGENTS.md](./AGENTS.md) for the authoring rules and [docs/PLAN.md](./docs/PLAN.md) for the design.

## Credits

Patterns borrowed from [Matt Pocock's skills](https://github.com/mattpocock/skills), [Lauren Tan's skills](https://github.com/poteto), and [Andrej Karpathy's notes on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876). `garden` also draws on write-ups of Lauren Tan's talks on gardening agent-written code, [OpenAI's harness engineering post](https://openai.com/index/harness-engineering/) and [Builder.io's guide to de-slopping a codebase](https://www.builder.io/blog/de-slop-ai-generated-codebase).

## License

MIT
