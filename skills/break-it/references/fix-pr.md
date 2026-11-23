# Fix pull request

Read this in step 13. Each fix gets its own pull request, and its description has to stand alone: a reviewer who never saw the hunt should understand the bug, believe the cause, and agree the fix is the right one, from the description and the diff.

When the repo has a pull request template, use its headings and put these sections under the closest ones.

## Rules

- **One bug.** The description and the diff cover this bug only. Mention another bug only in one line, when this fix also resolves it (step 10 found it covered).
- **The problem before the solution.** Explain what goes wrong in user terms before any code.
- **Correct, not just passing.** Say why the change fixes the cause, and why it is better than the alternatives you weighed.
- **Plain words.** No hunter or persona names; say what a user does.

## Template

```
Title: Fix <the wrong outcome, in user terms>

## The bug
<What the user does, what happens, and what should happen instead. Cite
the contract line it breaks: NEVER-2 "an invoice is never created twice".>

## Steps to reproduce
1. <from a fresh start, exact inputs>
2. ...
Expected: <...>
Actual: <...>

## Cause
<Where in the code the behavior comes from and why it produces the wrong
outcome. Point at the file and function.>

## The fix
<What changes, in a few sentences.>

## Why this is the correct fix
<Why it addresses the cause rather than the symptom, and why it cannot
break the other contract items it touches.>

Alternatives considered:
- <option>: <why rejected>
- <option>: <why rejected>

## Verification
- New test `<name>` fails on the base branch and passes here.
- The repro steps above no longer reproduce.
- <project check command>: passes.
```

## Branch and stacking

The branch is `break-it/<n>-<slug>` off the base branch. When the fix has to touch the same lines as an earlier fix PR, branch from that PR and add one line at the top: "Stacked on #<pr>: merge that first."
