---
name: surgical-diff-review
description: Review a finished code change hunk by hunk, checking that every changed line traces to the ask or the approved plan, and flag scope creep, speculative abstraction, drive-by refactors and missing verification. Use when a change is ready for review, before committing or opening a pull request. Use when the user asks whether a diff is clean, minimal or on scope. Use after building the slices of a plan made with plan-with-patterns.
license: MIT
metadata:
  display-name: Surgical Diff Review
  short-description: Every changed line traces to the ask
---

# Surgical diff review

The verify half of the loop: plan, build, then check that the diff does what was asked and nothing else. A clean diff is one where each hunk points at a line of the plan or the request, and every verify check has a result.

Review first and change nothing. Proposed reverts and splits go in the report for the user to accept.

## Steps

1. **Fix the contract.** Use the approved plan from plan-with-patterns when one exists: its Goal, Slices and Cut sections. Otherwise restate the user's request as one goal line with an observable check. Done when the goal and its check fit on one line and you know what was cut.
2. **Collect the diff.** Diff the change against its base: the merge base for a branch, `HEAD` plus the staging area for local work. Include new and deleted files. Done when every changed file and hunk is on your list.
3. **Trace every hunk.** Label each hunk with the plan line or part of the ask it serves. Use one of three labels: **traced** (does the asked work), **supporting** (a traced hunk needs it: an import, a test, wiring, a migration), or **untraced**. Done when every hunk carries a label and a pointer.
4. **Name the drift.** For each untraced hunk, name its kind from [references/drift-catalog.md](references/drift-catalog.md) and propose one action: revert it, split it into its own change, or keep it with a reason the user can accept. Check that nothing from the plan's Cut section came back. Done when every untraced hunk has a kind and an action.
5. **Check the shape of traced hunks.** Ask of each: could fewer lines or a plain function meet the goal? Each pattern in the diff matches one the plan named, and its force is still present; a pattern the plan did not name is drift of kind speculative abstraction. Names follow the project's glossary and existing style. Done when each traced hunk is either minimal or has a concrete smaller version written next to it.
6. **Check verification.** Run the goal check and each slice's verify check when you can. New behaviour has a test that would fail without it. Done when every check has a result: pass, fail, or not run with the reason.
7. **Give the verdict.** Write the report below. The verdict is **clean** when every hunk is traced or supporting and every check passed, **needs changes** when any action is a revert or split or a check failed, and **unverified** when the diff is on scope but a check did not run. Done when the report is written and the verdict matches these rules.

## Output

```
## Verdict: clean | needs changes | unverified
Goal: <one line> → verify: <check>

## Hunks
| File:lines | Label | Traces to | Note |

## Drift
- <file:lines>: <kind>. Action: revert | split | keep because <reason>

## Verification
- <check>: pass | fail | not run (<reason>)

## Smaller versions
- <file:lines>: <the shorter version, or "none">
```

End by asking the user which proposed actions to apply. Apply only the ones they accept, then run step 6 again.
