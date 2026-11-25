# Fix pull request

Read this in step 12. Each find gets its own pull request, and its description has to stand alone: a reviewer who never saw the sweep should see what drifted or broke, believe the cause, and agree the fix is the right one because it fits the design the repo already has.

When the repo has a pull request template, use its headings and put these sections under the closest ones.

## Rules

- **One find.** The description and the diff cover this find only. Mention another find only in one line, when this PR also covers it.
- **The docs before the code.** Quote the yardstick line first, then say what the code does instead.
- **The cause, not just the symptom.** Say why the code drifted or broke: a half-finished migration, a pattern copied from another file, a doc that was never updated, a case the code never handled.
- **Why this fix.** Say which part of the existing design the fix uses or extends, and why that is more natural than the alternatives you weighed.
- **Plain words.** Say what the code does, not which bed, lens or sweeper found it.

## Weed template

```
Title: <verb> <what>, in plain words (e.g. "Remove the unused retry helper")

## What drifted
<The yardstick line, quoted with its source: the design doc's Patterns
table, contract item INV-3, an ADR, a glossary term or an AGENTS.md rule.
Then what the code does instead, with file:line.>

## Cause
<Why the code drifted from it.>

## Why it matters
<How far it would spread: where it already appears, or which file new
code would copy it from. Which contract item it puts at stake, if any.>

## The fix
<What changes, in a few sentences. One kind of change.>

## Why this fix fits the design
<Which module, seam or pattern the fix uses or extends, and why that is
the natural place for it.>

Alternatives considered:
- <option>: <why rejected>

## What this lets us delete
<The code this removes, with a line count, or why it adds more than it
removes. A new test is exempt.>

## Behavior unchanged
- `<check command>` passes on the base branch and on this branch.
- <Each test that covers the touched code, by name.>
- <For a new contract test: it passes on the current code, so it pins
  behavior that already holds.>

## Repeat
<Only for a repeat weed: the other places this drift shows up, and the
check proposed to catch it, which is in the garden report.>
```

## Bug template

```
Title: Fix <the wrong outcome, in plain words>

## The bug
<The contract item, quoted with its id and source. Then what the code
does instead, with file:line, and what a user or caller would see.>

## Cause
<Where in the code the behavior comes from and why it produces the wrong
outcome. Point at the file and function.>

## The fix
<What changes, in a few sentences.>

## Why this fix fits the design
<Why it removes the cause rather than hiding the symptom. Which module,
seam or pattern it uses or extends, and why that is where the design
says this behavior lives. Why it cannot break the other contract items
it touches.>

Alternatives considered:
- <option>: <why rejected>

## Verification
- New test `<name>` fails on the base branch and passes here.
  <The failure output on the base branch, a few lines.>
- `<check command>` passes.
```

## Branch and stacking

The branch is `garden/<n>-<slug>` off the base branch. When the fix has to touch the same lines as an earlier garden PR, branch from that PR and add one line at the top: "Stacked on #<pr>: merge that first."
