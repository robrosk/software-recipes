# Platforms

Read "Isolated trigger endpoints" in step 3, the section for your harness in step 4, and the Copilot roster in step 5. Facts here were checked against each vendor's docs in November 2026; when your harness behaves differently, trust what it does and tell the user this file is stale.

## What every harness needs

Three things, checked in step 4:

1. **Ten parallel subagents.** If the harness caps concurrency below ten, run the hunters in waves and say so.
2. **A way to drive the app.** For a web app that is a browser tool. Playwright MCP (`npx -y @playwright/mcp@latest`) is the one browser driver all three harnesses can run. For a CLI or TUI, the terminal is enough.
3. **One browser per hunter.** Hunters that share a browser close each other's tabs and report each other's state as bugs.

**The isolation probe.** Before briefing, spawn two short probe subagents that each open the app in the browser tool and list their open tabs. If either sees the other's tab, the browser is shared. Then use the fallback: each hunter drives its own headless browser from the terminal by writing and running small Playwright scripts with its own user data directory (`/tmp/break-it/<hunter>/profile`), and reads screenshots and page text after each step. Done when the probe shows separate tabs, or the fallback is in place.

**Isolated trigger endpoints in local harnesses.** When hunters drive a local test server with shared background triggers (such as cron ticks, queue drains, or chaos toggles), scope each trigger and chaos header to the calling hunter's namespace or prefix so parallel hunters never mutate another hunter's seeded state. You do this in step 3, before any hunter starts, using only test harness config, since hunters never change code. When the app cannot scope a trigger per namespace, run the hunts that depend on it one at a time instead of changing app code. Done when every shared trigger is scoped per hunter, or the hunts that use it are queued to run one at a time.

**What "computer use" means here.** The desktop computer-use tools on these harnesses hold one screen for one session, so ten hunters cannot each have a desktop. Browser automation per hunter is how break-it gives ten agents their own way to use the app. Tell the user this once in step 4.

## Claude Code

- **Spawn:** the `Agent` tool (older versions call it `Task`). Send all ten calls in one message so they run in parallel. The default cap is 20 concurrent subagents (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
- **Nesting:** subagents can spawn their own. Tell hunters not to, in the brief.
- **Model:** every hunter can use the parent's model. A per-call `model` can pick `opus`, `sonnet` or `haiku`; all are Anthropic models, so diversity on Claude Code comes from personas.
- **Browser:** subagents inherit the session's MCP tools. Add Playwright MCP with `claude mcp add playwright -- npx -y @playwright/mcp@latest` when it is missing. Claude in Chrome (`--chrome`) drives the user's one visible, signed-in Chrome and pauses at logins, so do not use it for hunters. Desktop computer use is macOS only and one session at a time, so it is not for hunters either.
- **Fallback:** if the probe shows a shared browser, use the terminal fallback above.

## Codex

- **Spawn:** multi-agent is on by default in the CLI (`features.multi_agent`). Ask Codex to spawn ten subagents with the ten briefs and wait for all of them.
- **Concurrency:** `agents.max_concurrent_threads_per_session` in `config.toml`. If it is below ten, run waves.
- **Model:** a custom agent file in `.codex/agents/<name>.toml` (`name`, `description`, `developer_instructions`, optional `model`) can pin a model, but all subagents share the session's model provider. Diversity on Codex comes from personas.
- **Browser:** the Codex CLI has no built-in browser; the in-app browser and computer use are desktop-app features. Add Playwright MCP under `[mcp_servers.playwright]` in `config.toml`. Subagents inherit the parent's MCP servers and cannot set their own, so they most likely share one browser: run the probe, and expect to use the terminal fallback.

## GitHub Copilot CLI

- **Spawn:** `/fleet` runs subagents in parallel through the `task` tool, and `/tasks` shows their progress. The concurrency cap is not documented; if fewer than ten run at once, the rest queue.
- **Model per hunter:** name the model for each piece of work in the `/fleet` prompt ("Use <model> for hunter 3"), or create ten custom agents in `.github/agents/hunter-<n>.agent.md`, each with its own `model:` in the frontmatter and the brief as its body. Fleet subagents default to a low-cost model, so always name the model.
- **Browser:** the GitHub MCP server is built in; Playwright is not. Add it with `/mcp add`, or in `.github/mcp.json`. Run the probe.

### Copilot model roster

Read the live list with `/model` before step 5: availability depends on the user's plan and their organization's policy, and the docs publish display names, not stable ids. Pick ten models this way:

1. One model from each lab on the list, the strongest each lab offers.
2. Fill the remaining seats with a second model from the labs with the most models, alternating labs, preferring a different model family over a smaller size of the same one.
3. Never repeat an exact model.

Labs on GitHub's supported-models page in November 2026, for orientation only:

| Lab | Examples |
| --- | --- |
| Anthropic | Claude Opus, Sonnet, Haiku, Fable |
| OpenAI | GPT-6 and GPT-5.x families, GPT-5.3-Codex |
| Google | Gemini |
| xAI | Grok |
| Microsoft | MAI-Code |
| Moonshot | Kimi |

Six labs means some labs supply two hunters. Record each hunter's exact model in the report, so a bug only one model found can be judged in triage like any other.
