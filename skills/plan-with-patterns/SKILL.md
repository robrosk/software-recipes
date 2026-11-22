---
name: plan-with-patterns
description: Plan a code change before writing it, naming the modules, seams and design patterns it uses and the simplest version that meets the goal. Use when the user asks to plan, design or architect a feature, refactor, or new repo, or when a change touches more than one module.
license: MIT
metadata:
  display-name: Plan With Patterns
  short-description: Pattern-first plan before code
---

# Plan with patterns

Produce a plan the user can approve in one read, before any code is written. The plan is the contract: every later diff traces back to a line of it.

When exploring, read `GLOSSARY.md` and `docs/adr/` if they exist, so the plan uses the project's own words and respects decisions already made.

## Steps

1. **Restate the goal as a check.** Write the goal as something observable: a test that goes green, a command whose output changes, a screen that shows a value. Done when the goal is a pass/fail check, not a wish.
2. **Surface assumptions.** List each assumption in one line. Where two readings of the ask exist, name both and say which you will take. Done when nothing you are about to rely on is unstated.
3. **Map the modules.** Name each module the change touches or adds, its one-sentence responsibility, and its public interface. Prefer deep modules: a lot of behaviour behind a small interface. Done when every file you expect to edit belongs to a named module.
4. **Name the patterns.** For each module, name the design pattern it uses (or "none: plain function") and the one force that earns it. Read [references/pattern-catalog.md](references/pattern-catalog.md) when choosing. A pattern with no force behind it is cut. Done when every pattern has a reason the user can argue with.
5. **Cut to the simplest version.** Remove any module, option or abstraction the goal does not need today. Done when deleting any remaining line of the plan would fail the goal check.
6. **Slice the work.** Order the work as vertical slices, each one ending on its own verify step (`→ verify: <check>`). Done when every slice is small enough to review in one sitting.

## Output

```
## Goal
<one line> → verify: <check>

## Assumptions
- ...

## Modules
| Module | Responsibility | Interface | Pattern (force) |

## Slices
1. <slice> → verify: <check>

## Cut
- <what was left out and why>
```

Stop after the plan. Ask the user to approve or redirect it, then build slice by slice.
