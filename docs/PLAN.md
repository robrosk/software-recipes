# software-recipes: plan

## 1. Recommended structure

```
software-recipes/
├── recipes.toml                  SSOT: plugin metadata, owner, targets on/off
├── skills/                       shipped skills only, one flat level
│   └── plan-with-patterns/
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

The sample skill `plan-with-patterns` combines these: Karpathy's verifiable goal and simplicity cut, Pocock's deep modules and vertical slices, plus Rob's rule that design patterns are named during planning.

## 5. Skills

Shipped:

- `plan-with-patterns` (model-invoked): pattern-first plan before code.
- `surgical-diff-review` (model-invoked): check every changed line traces to the ask or plan.
- `grill-the-plan` (user-invoked): interview one question at a time, then hand off to `plan-with-patterns`.
- `reflect` (user-invoked): route session lessons into skill edits, lint rules or notes.

Candidates:

- `tdd-slice` (model-invoked): one red-green slice at a pre-agreed seam.
- `experiment-log` (model-invoked): config, seed, commit and results for every run.
- System design skill: scalable architecture plus the system-level behaviour it must guarantee. Scope still being discussed.
- `research-notes` (model-invoked): cited findings from primary sources into the repo.

## 6. Open risks (verify by hand)

1. Codex and Copilot installs are **not yet tested** here; the Codex and Copilot CLIs were not available in this environment. Claude Code install was tested: 1 skill loads, no duplicates.
2. `claude plugin validate . --strict` fails only on a missing icon. Add a square PNG at `.claude-plugin/icon.png` (512 to 2048 px) to pass strict mode.
3. The Agent Plugins `extensions` key shape (`"com.openai"`) is from docs, not an install. Test before flipping `agent_plugins = true`.
