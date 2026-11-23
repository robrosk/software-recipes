---
name: plan-the-change
description: Plan one code change before writing it, as a pass/fail goal, the modules and interfaces it touches, the simplest version and vertical slices with verify steps. Reuses the design patterns a design-the-system doc chose and never picks its own. Use when the user asks to plan a feature, fix or refactor before any code is written. Use when slicing a design doc from design-the-system into buildable steps. Use when a change spans more than one file and the order of the work is not obvious.
license: MIT
metadata:
  display-name: Plan The Change
  short-description: Goal, modules and slices for one change
---

# Plan the change

Produce a plan the user can approve in one read, before any code is written. The plan is the contract: every later diff traces back to a line of it.

This skill slices work; it never chooses design patterns. Only design-the-system does, so a plan can never bring back a pattern the design rejected. When a design doc from design-the-system exists (`docs/design/*.md`, or the one the user names), read it first: its contract and Patterns table are fixed inputs, and it stays the source of truth. When the plan departs from its Architecture, the same PR updates the doc. For a new system, or a change that redraws component boundaries, offer `/design-the-system` instead of planning it here.

When exploring, read `GLOSSARY.md` and `docs/adr/` if they exist, so the plan uses the project's own words and respects decisions already made.

## Steps

1. **Restate the goal as a check.** Write the goal as something observable: a test that goes green, a command whose output changes, a screen that shows a value. Done when the goal is a pass/fail check, not a wish.
2. **Surface assumptions.** List each assumption in one line. Where two readings of the ask exist, name both and say which you will take. Done when nothing you are about to rely on is unstated.
3. **Map the modules.** Name each module the change touches or adds, its one-sentence responsibility, and its public interface. With a design doc, use its component names and interfaces. Prefer deep modules: a lot of behaviour behind a small interface. Done when every file you expect to edit belongs to a named module.
4. **Copy the patterns.** With a design doc, copy its Patterns table into the plan as given. Without one, write "None chosen: no design doc" and follow the patterns the touched code already uses. Never add, drop or swap a pattern. Done when the Patterns section is the doc's table unchanged, or the no-doc line.
5. **Cut to the simplest version.** Remove any module, option or abstraction the goal does not need today. Done when deleting any remaining line of the plan would fail the goal check.
6. **Slice the work.** Order the work as vertical slices, each one ending on its own verify step (`→ verify: <check>`). When a slice seems to need a pattern the Patterns section does not list, stop: tell the user which slice needs it and why, and send them to `/design-the-system` to put it on trial. Done when every slice is small enough to review in one sitting and none needs an unlisted pattern.
7. **Record departures from the design doc.** With a design doc, list each way the plan departs from its Architecture: a module added or dropped, an interface changed, a responsibility moved between components. For each, name the doc edit and put it in the slice that makes the change, so the code and the doc land in the same PR: update the Architecture table and data flow, and add a line to the doc's Change log saying what changed and why. A departure that adds or drops a pattern, or changes or cannot meet a contract item, is not a doc edit: stop and send the user to `/design-the-system`. Done when every departure has its doc edit in a slice, or the plan says "No departures".

## Output

```
## Goal
<one line> → verify: <check>

## Assumptions
- ...

## Modules
| Module | Responsibility | Interface |

## Patterns (copied from <design doc path>, unchanged)
| Pattern | Where | Error it rules out | Protects | Why not plain code |
or: None chosen: no design doc

## Slices
1. <slice> → verify: <check>

## Cut
- <what was left out and why>

## Design doc updates
- <departure> → <doc edit>, in slice <n>
or: No departures
```

Stop after the plan. Ask the user to approve or redirect it, then build slice by slice.
