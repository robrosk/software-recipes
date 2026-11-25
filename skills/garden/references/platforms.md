# Platforms

Read the section for your harness in step 4. The point of several sweepers is that different models miss different things: a find that one model's training hides from it, another model can see. So spread the sweepers across as many different models as the harness offers, and across different labs where it offers more than one. Facts here come from each vendor's docs as of November 2026; when your harness behaves differently, trust what it does and tell the user this file is stale.

## Rules for every harness

- **Name models so they do not go stale.** Use the alias the harness accepts (`opus`, not a dated id) or "the strongest model each lab offers", read from the live list. Never pin a version number in a brief or an agent file.
- **No two sweepers on the same model.** A second sweeper on the same model mostly finds the same things. When the harness offers fewer models than you want sweepers, stop at one sweeper per model.
- **Sweepers are read-only.** They change no file, run no formatter, open no branch and spawn no subagents. Check the working copy is unchanged after they return.
- **Record each sweeper's exact model** in the report and the ledger, so a find only one model raised can be judged like any other.

## Claude Code

- **Models:** one sweeper per model alias the `Agent` tool's `model` parameter accepts. In November 2026 that is `fable`, `opus`, `sonnet` and `haiku`, strongest first. All are Anthropic models and share much of their training, so the lens each sweeper gets (sweeper-brief.md) matters more here than on Copilot.
- **Spawn:** send one `Agent` call per sweeper in one message so they run in parallel, each with its `model` set. Use a read-only agent: the built-in Explore agent, or a custom agent in `.claude/agents/<name>.md` with only Read, Grep and Glob and a `model:` alias in its frontmatter.
- **Nesting:** subagents can spawn their own. The brief forbids it.

## Codex

- **Models:** every subagent shares the session's model provider. A custom agent in `.codex/agents/<name>.toml` (`name`, `description`, `developer_instructions`, optional `model`) can pin a different model from that provider, so give each sweeper its own agent file with a different model the provider offers. Variety on Codex is narrower than on Copilot; say so in the report.
- **Spawn:** multi-agent is on by default. Ask Codex to spawn one subagent per sweeper with its brief and wait for all of them. If `agents.max_concurrent_threads_per_session` in `config.toml` is below the sweeper count, run them in waves.
- **Read-only:** instructions alone do not make a read-only sandbox. Say it in the brief and check the working copy is unchanged after they return.

## GitHub Copilot CLI

- **Models:** read the live list with `/model` before step 4; availability depends on the user's plan and their organization's policy. Pick one sweeper per lab on the list, the strongest model each lab offers. When the list has fewer than four labs, add a second model from the labs with the most models, preferring a different family over a smaller size of the same one.
- **Spawn:** `/fleet` runs subagents in parallel. Fleet subagents default to a low-cost model, so always name the model for each sweeper: in the `/fleet` prompt ("Use <model> for sweeper 3"), or with one custom agent per sweeper in `.github/agents/sweeper-<n>.agent.md`, each with its own `model:` in the frontmatter and the brief as its body.

Labs on GitHub's supported-models page in November 2026, for orientation only:

| Lab | Examples |
| --- | --- |
| Anthropic | Claude Fable, Opus, Sonnet, Haiku |
| OpenAI | GPT-6 and GPT-5.x families, GPT-5.3-Codex |
| Google | Gemini |
| xAI | Grok |
| Microsoft | MAI-Code |
| Moonshot | Kimi |
