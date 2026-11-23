# software-recipes: plan

## 1. Recommended structure

```
software-recipes/
├── recipes.toml                  SSOT: plugin metadata, owner, targets on/off
├── skills/                       shipped skills only, one flat level
│   └── plan-the-change/
│       ├── SKILL.md              steps every run needs (< 500 lines)
│       ├── references/           disclosed reference, read on demand
│       ├── evals/triggers.json   should / should-not trigger prompts
│       └── agents/openai.yaml    GENERATED (Codex labels + policy)
├── drafts/                       unshipped skills, invisible to every harness
├── tools/recipes/                stdlib-only build tool
│   ├── skill.py                  Skill value object + strict frontmatter parser
│   ├── config.py                 PluginConfig from recipes.toml
│   ├── rules.py                  validation rules, one function each
│   ├── pipeline.py               load → validate → render → write | check
│   └── adapters/                 one file per harness + REGISTRY
├── .claude-plugin/               GENERATED plugin.json + marketplace.json
├── tests/                        unit tests + "repo is up to date" test
├── docs/                         this plan, ADRs
├── AGENTS.md / CLAUDE.md         authoring rules (CLAUDE.md imports AGENTS.md)
└── Makefile, .github/workflows/check.yml
```

## 2. Design patterns, and the force behind each

| Pattern | Where | Force |
| --- | --- | --- |
| Single source of truth | `recipes.toml`, `SKILL.md` | name, version and skill list would otherwise live in 3 to 5 files |
| Adapter | `adapters/*.py` | one model, several manifest formats |
| Registry | `adapters/__init__.py` | new harnesses get added; the pipeline should not change |
| Pipeline, functional core / imperative shell | `pipeline.py` | rendering is pure and unit-testable; only two functions touch disk |
| Rule list (Strategy per rule) | `rules.py` | lint rules grow; each is one small function appended to `RULES` |
| Value object | frozen dataclasses | Skill and config are compared and passed, never mutated |
| Golden-file drift check | `make check`, CI | generated files are committed because installs read git directly |

## 3. Key cross-platform tradeoff

All three tools read the Agent Skills format (`SKILL.md` with `name` + `description`), so skill bodies are fully shared. The fork is the **plugin manifest**:

- **`.claude-plugin/` (chosen default).** Claude Code reads it natively. Codex falls back to `.claude-plugin/plugin.json` when it has no manifest of its own (confirmed in Codex's manifest source). Copilot CLI checks `.claude-plugin/` for both plugin and marketplace. Matt Pocock reports this exact setup installing on all three (his ADR, Oct 2026). Both vendors now label it "legacy-compatible".
- **Root `plugin.json`, Agent Plugins 1.0.** The format Codex and Copilot now recommend. Closed schema, skills only from `skills/<name>/`, vendor extras under `extensions`. Claude Code's docs do not mention it. When present, Codex and Copilot prefer it, so a wrong shape breaks them while Claude keeps working. Built as an adapter, **off** until verified.

Per-skill difference: Claude uses `disable-model-invocation: true`; Codex needs `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. The build generates the Codex side from the Claude field, so a skill is user-invoked everywhere or nowhere.

## 4. Patterns taken from the three sources

**Matt Pocock (mattpocock/skills)**
- Small, composable skills. Split on one axis: **user-invoked** (orchestrators, human-facing description) vs **model-invoked** (reusable discipline, "Use when ..." triggers).
- Skills call each other with "Call the Skill tool with X", never by linking across folders.
- Progressive disclosure: steps in `SKILL.md`, reference in sibling files behind a pointer that says when to read it.
- Every step ends on a completion criterion. Positive phrasing over prohibitions. Leading words (`red`, `tracer bullet`, `seam`) instead of repeated sentences.
- `GLOSSARY.md` + ADRs as shared language; a frontmatter checker in CI; no em dashes.

**Lauren Tan (poteto/how, brainmaxxing, verification-skill-example)**
- `SKILL.md` holds routing logic only; prompts handed to subagents live in `references/`.
- Fan out 2 to 4 parallel explorers for complex questions, one pass for simple ones, then synthesize.
- A learning loop (`reflect`, `meditate`): route each lesson to the skill it improves, or encode it as a lint rule or script before writing a note.
- Scoped, behavior-level reference files an agent can open one at a time, instead of a wiki.

**Andrej Karpathy (LLM coding pitfalls post, via multica-ai/andrej-karpathy-skills)**
- Think before coding: state assumptions, surface tradeoffs, ask when confused.
- Simplicity first: minimum code, no speculative abstraction.
- Surgical changes: every changed line traces to the request.
- Goal-driven execution: turn tasks into verifiable checks and loop until they pass.

The sample skill, now `plan-the-change`, combines Karpathy's verifiable goal and simplicity cut with Pocock's deep modules and vertical slices. Rob's rule that design patterns are named during planning now lives in `design-the-system`, the only skill that chooses them, so a plan can never bring back a pattern the design rejected.

## 5. Skills

Shipped:

- `plan-the-change` (model-invoked): goal, modules and vertical slices for one change, reusing the design doc's Patterns table unchanged.
- `surgical-diff-review` (model-invoked): check every changed line traces to the ask or plan.
- `grill-the-plan` (user-invoked): interview one question at a time, then hand off to `design-the-system` for a new system or cross-module change, or to `plan-the-change` for a small one.
- `design-the-system` (user-invoked): contract covering behavior, scale and robustness, then the user's own design stress-tested against it, then patterns admitted only where they rule out a named failure. The only skill that chooses design patterns.
- `break-it` (user-invoked): behavior contract from the docs or a grill, ten computer-use hunters (distinct personas, or on Copilot distinct models across labs) that only report bugs, triage by the main agent, then one fix PR per bug.
- `orchestrate-prs` (user-invoked): signed design into frozen seams, slices with disjoint file ownership sorted into waves, one linted and cold-read work order per slice, one sign-off, then subagents open one PR each, gated by `surgical-diff-review`, with remaining work orders updated after every merged wave.
- `garden` (user-invoked, and offered by `orchestrate-prs` after each wave): sweep 19 beds of drift against the design doc and contract, bin each finding as weed, question, leave or bug, rank weeds by how far they would spread, pull each in its own behavior-preserving PR, turn repeat weeds into proposed lint rules or tests, and keep a ledger in `docs/garden/ledger.md` across runs.
- `reflect` (user-invoked): route session lessons into skill edits, lint rules or notes.

Candidates:

- `tdd-slice` (model-invoked): one red-green slice at a pre-agreed seam.
- `experiment-log` (model-invoked): config, seed, commit and results for every run.
- `research-notes` (model-invoked): cited findings from primary sources into the repo.

## 6. Open risks (verify by hand)

1. Codex and Copilot installs are **not yet tested** here; the Codex and Copilot CLIs were not available in this environment. Claude Code install was tested: 1 skill loads, no duplicates.
2. `claude plugin validate . --strict` fails only on a missing icon. Add a square PNG at `.claude-plugin/icon.png` (512 to 2048 px) to pass strict mode.
3. The Agent Plugins `extensions` key shape (`"com.openai"`) is from docs, not an install. Test before flipping `agent_plugins = true`.
