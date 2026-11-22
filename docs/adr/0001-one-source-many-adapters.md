# 0001: One skill source, one adapter per harness, generated files committed

Date: 2026-11-22. Status: accepted.

## Context

The repo targets Claude Code, Codex and Copilot. All three read Agent Skills (`skills/<name>/SKILL.md`), but each wants its own extras: Claude reads `.claude-plugin/`, Codex reads per-skill `agents/openai.yaml` for picker labels and invocation policy, and Codex and Copilot both now prefer a root `plugin.json` (Agent Plugins 1.0). Hand-maintaining these means the same fact (name, version, skill list, invocation) lives in several files and drifts.

## Decision

- **Single source of truth**: `recipes.toml` for plugin metadata, each `SKILL.md` for skill metadata.
- **Adapter per harness**, collected in a **registry**. Adapters are pure: config and skills in, `{path: content}` out.
- **Pipeline** with a **functional core, imperative shell**: load, validate, render are pure; only `write` and `find_drift` touch disk.
- Generated files are **committed**, because every harness installs straight from git and runs no build step. CI runs `make check`, which fails on drift (golden-file check).
- Lean on `.claude-plugin/` as the one manifest all three read today. Keep the Agent Plugins adapter behind a flag until installs on Codex and Copilot confirm it.

## Consequences

- Adding a harness is one new adapter file plus one registry line.
- Adding a skill is one folder; the manifests follow on `make build`.
- `skills/` must stay flat and shipped-only, since Codex and Copilot discover recursively. Drafts live in `drafts/`.
