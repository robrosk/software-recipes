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

- **[plan-with-patterns](./skills/plan-with-patterns/SKILL.md)**: Plan a change before coding it, naming its modules, seams and design patterns, cut to the simplest version.

**User-invoked** (only you can fire these, by typing `/name`)

- none yet

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

Patterns borrowed from [Matt Pocock's skills](https://github.com/mattpocock/skills), [Lauren Tan's skills](https://github.com/poteto), and [Andrej Karpathy's notes on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876).

## License

MIT
