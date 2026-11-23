# Weed pull request

Read this in step 11. Each weed gets its own pull request, and its description has to stand alone: a reviewer who never saw the sweep should see what drifted, believe nothing else changed, and agree this is the right repair.

When the repo has a pull request template, use its headings and put these sections under the closest ones.

## Rules

- **One weed, one kind of change.** No mixing a move with a rename, a dedupe with a test rewrite, or any change with formatting. Mixed diffs hide which change broke a behavior.
- **The drift before the repair.** Name the yardstick line first, then what the code does instead.
- **Behavior unchanged, and shown.** The acceptance condition is that the guarantee still holds, never that a warning went away.
- **Plain words.** Say what the code does, not which bed or sweeper found it.

## Template

```
Title: <verb> <what>, in plain words (e.g. "Remove the unused retry helper")

## What drifted
<The yardstick line, quoted with its source: the design doc's Patterns
table, contract item INV-3, an ADR, a glossary term or an AGENTS.md rule.
Then what the code does instead, with file:line.>

## Why it matters
<How far it would spread: where it already appears, or which file new
code would copy it from. Which contract item it puts at stake, if any.>

## The repair
<What changes, in a few sentences. One kind of change.>

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

## Branch and stacking

The branch is `garden/<n>-<slug>` off the base branch. When the weed has to touch the same lines as an earlier weed PR, branch from that PR and add one line at the top: "Stacked on #<pr>: merge that first."
