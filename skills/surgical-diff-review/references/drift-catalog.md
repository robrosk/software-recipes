# Drift catalog

Each kind of drift: the signal that gives it away, and the usual action. Read this in step 4 when naming an untraced hunk.

| Kind | Signal | Usual action |
| --- | --- | --- |
| Scope creep | A feature, option or flag the ask never mentioned | Revert, or split into its own change if the user wants it |
| Speculative abstraction | An interface, base class, factory, config knob or generic parameter with one caller and no second one planned | Inline it into the one caller |
| Drive-by refactor | Renames, moves or restructuring in code the change did not need to touch | Split into a separate refactor change |
| Formatting churn | Whitespace, import order or quote style changes in untouched lines | Revert, or run the formatter in its own commit |
| Dead code | Functions, branches or parameters nothing calls | Delete |
| Defensive noise | Checks for states the types or callers already rule out, broad try/except that hides errors | Remove, or narrow to the one real failure |
| Unasked dependency | A new package, service or tool | Revert, or ask the user before keeping |
| Cut item returned | Something the plan's Cut section left out | Revert |
| Comment narration | Comments that restate the next line or describe the change history | Delete; keep comments that explain why |
| Test weakening | A test skipped, loosened, or its assertion changed to match new output | Revert and fix the code instead |

## Supporting, not drift

These are supporting hunks when a traced hunk needs them: imports, a test for the new behaviour, wiring a new module into a registry, a migration for a new column, a docs line for a changed public interface, regenerated files the build produces.

## Judging "keep because"

Keep an untraced hunk only when the reason is about this change: it fixes a bug the change would otherwise expose, or the traced code cannot work without it. "It was nearby" and "it is cleaner" are reasons for a separate change.
