# Platforms

Read the section for your harness in step 9. Facts here come from each vendor's docs as of November 2026; when your harness behaves differently, trust what it does and tell the user this file is stale.

## What every harness needs

Three things, checked in step 9:

1. **Parallel subagents.** If the harness caps concurrency below a wave's size, split the wave into sub-waves (slicing.md).
2. **One working copy per subagent.** Two subagents in one checkout overwrite each other's files and commit each other's changes. Disjoint ownership lowers the damage but does not stop a shared `git add` or a shared lockfile.
3. **Who commits, pushes and opens the PR.** Either the subagent does all three from its own copy, or it stops after committing and you push and open the PR. Pick one per run and write it into every work order's Steps section.

**The fallback, any harness.** When subagents cannot get their own copies, create them yourself before dispatch, one per slice:

```bash
git worktree add ../<repo>-wt/<slice> -b <branch> <base>
```

Tell each subagent to work only inside its path. When subagents cannot push, have each one commit and report; then push and open each PR yourself. After the wave, remove each worktree with `git worktree remove <path>` once its branch is pushed.

**Work orders carry every rule.** Not every harness loads `AGENTS.md` into subagents, so the Conventions section of each work order pastes what the subagent needs. Never rely on a subagent reading the repo's instruction files.

## Claude Code

- **Spawn:** the `Agent` tool. Send one call per slice in one message so the wave runs in parallel. The cap is 20 concurrent subagents (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
- **Isolation:** pass `isolation: "worktree"` on each call, or set `isolation: worktree` in a custom agent's frontmatter in `.claude/agents/<name>.md`. With agent teams on, the frontmatter alone is not enough: pass it on the call. Worktrees land in `.claude/worktrees/`.
- **Base branch:** subagent worktrees start from the remote default branch (`worktree.baseRef: "fresh"`); the only other value, `"head"`, uses your current HEAD. Neither can name a branch. When a slice must start elsewhere (a stacked parent's branch, or a base that is not the default), make its worktree yourself with the fallback above.
- **Commit, push, PR:** worktree subagents have Bash, Edit and Write and can commit. Pushing and opening a PR depend on the session's git remote and tools; when the probe push in step 9 fails, use the fallback.
- **Permissions:** a subagent inherits the parent's permission mode, and a background subagent asks its permission prompts in your session. Settle the mode before dispatch so ten prompts do not queue up.
- **Tools:** restrict with `tools` and `disallowedTools` in the agent's frontmatter; `disallowedTools` wins. For the cold read in step 7, use a read-only agent (the built-in Explore agent, or one with only Read, Grep and Glob).
- **Nesting:** subagents can spawn their own, up to three levels. The work order forbids it; `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` enforces it.
- **Results:** background subagents report back by completion notification, with only their summary in your context. That summary is the work order's Report back block.
- **Instruction files:** non-fork subagents load `CLAUDE.md` and `AGENTS.md` from the main conversation, not from their worktree's branch.
- **Cleanup:** a worktree with unpushed commits or uncommitted changes stays behind. Remove each one after its PR is open.
- **Related:** the built-in `/batch` splits a change into units, one background worktree subagent each. It has no seams, contract, lint or gate, so orchestrate-prs does not use it.

## Codex

- **Spawn:** subagents are on by default (`agents.enabled`). Ask Codex to spawn one subagent per slice with its work order, and wait for all of them; Codex returns once every result is in. `/subagents` switches between their threads.
- **Concurrency:** `agents.max_concurrent_threads_per_session` in `config.toml`, not counting the main thread. When it is below the wave's size, run sub-waves.
- **Isolation:** the docs do not say that in-session subagents get their own worktrees, and warn that agents editing code at once can conflict. Treat them as sharing one checkout and use the fallback, or run one process per slice in its own managed worktree:

  ```bash
  codex exec --worktree "<work order>"
  ```

- **Commit, push, PR:** subagents inherit the parent's sandbox and approval policy, and a custom agent file cannot loosen them. Under `workspace-write`, `.git` is read-only and network is off by default, so a subagent most likely cannot commit or push. Plan for the subagent to edit and test, and for you to commit, push and open each PR. In a non-interactive run, an action that needs approval fails and the error comes back to you.
- **Tools:** a custom agent in `.codex/agents/<name>.toml` (`name`, `description`, `developer_instructions`, optional `model`) can turn off features, for example `features.shell_tool = false` for the cold read. Instructions alone do not make a read-only sandbox.
- **Instruction files:** `AGENTS.md` is read per run from the repo root down; whether subagents load it is not documented, so paste conventions into each order.
- **Cloud tasks:** `codex cloud exec --env <id>` (experimental) runs a task in its own cloud workspace, and `codex apply` brings its diff into the local tree. Use it as the fallback when local isolation is not possible; you open the PR from the applied diff.

## GitHub Copilot

Copilot has two ways to run slices. Use the CLI for speed and the cloud agent for isolation.

### Copilot CLI (`/fleet`)

- **Spawn:** `/fleet` runs subagents in parallel, each in its own context; `/tasks` shows, stops or removes them. Fleet subagents default to a low-cost model, so name the model per slice in the prompt or in a custom agent's `model:` field.
- **Isolation:** none documented. Treat fleet subagents as sharing one checkout and use the fallback, telling each subagent its worktree path.
- **Permissions:** `--allow-tool='shell(git:*)'` and `--deny-tool='shell(git push)'` let subagents commit but not push; deny always wins. Whether these flags reach fleet subagents is not documented, so check with the probe in step 9.
- **Tools:** a custom agent in `.github/agents/<name>.agent.md` takes `tools:` (aliases such as `read`, `edit`, `search`, `execute`; `[]` turns all off) and `strict-tools-list: true` to drop the defaults. The prompt body can run to 30,000 characters, which fits a work order.
- **Instruction files:** CLI subagents do not read the repo's custom instructions unless the agent file sets `include-custom-instructions: true`.

### Copilot cloud agent

- **Dispatch:** one task per slice, one PR per task. Assign an issue whose body is the work order to Copilot, use `/delegate` from the CLI, or call the API (`agent_assignment` with `base_branch` on REST, `agentAssignment.baseRef` on GraphQL, or the agent tasks API in preview with `prompt`, `base_ref` and `create_pull_request`).
- **Isolation:** each task runs in its own GitHub Actions sandbox, capped at 59 minutes per task. Split any slice that cannot finish in that time.
- **Stacking:** set the base branch per task to the parent PR's branch for a stacked slice, or to the base branch in wait mode.
- **Push and PR:** it pushes only to its own `copilot/` branch and opens the PR itself. It cannot approve or merge, workflows on its PRs wait for approval from someone with write access, and the person who asked cannot approve the PR. Tell the user in step 13 that CI on these PRs needs their approval to run, and run the gate's check locally on the branch meanwhile.
- **Instruction files:** it reads `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `AGENTS.md` and `CLAUDE.md`. Paste conventions into the work order anyway, so it matches the other harnesses.
- **Results:** there is no completion message to you. Poll the task status or the PR list until every task in the wave is completed or failed, then read each PR's description and commits as its report.

## The probe (step 9)

Before the first wave, dispatch one throwaway subagent the same way the slices will run. Have it create a file in its working copy, commit it on a probe branch, and report its working directory, branch and whether a push succeeds. Then confirm the file is not in your own checkout, delete the probe branch locally, and remove its worktree. Do not push the probe branch unless the user agrees. Done when you know whether subagents get their own copy and whether they can commit and push.
