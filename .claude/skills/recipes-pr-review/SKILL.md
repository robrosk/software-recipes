---
name: recipes-pr-review
description: Review a pull request in the software-recipes repo against its authoring rules and its own skills, and give a verdict of merge, fix first or needs Rob's call with draft comments. Use when a PR in software-recipes is ready for review. Use when asked whether a skill edit in this repo is safe to merge.
license: MIT
metadata:
  display-name: Recipes PR Review
  short-description: Review a software-recipes PR
---

# Recipes PR review

A PR here changes instructions that other agents follow word for word. The usual failure is not a typo: it is a new mode, step or rule that is wired into one place and contradicts another, or an instruction with no one to carry it out. Review for that.

Review first and change nothing on the PR. Rob reviews and merges every PR himself, so the output is a verdict and draft comments, never an approval, a merge or a push to the PR's branch.

## Steps

1. **Load the contract.** Read `AGENTS.md` (layout and authoring rules), `recipes.toml`, `docs/PLAN.md` and `docs/adr/`, then the PR description. This repo's PR descriptions list each change with a "Why" and a "Where this differs from the spec" section: that list is the plan. Done when you can name every change the PR claims and why.
2. **Check the build.** In a clean checkout of the PR head, run `make check`. It already catches em dashes, broken links, symlinks in `skills/`, bad frontmatter, malformed evals and stale generated files, so do not re-check those by hand. Done when `make check` has a result: pass, or the failing lines.
3. **Trace every hunk.** Call the Skill tool with "surgical-diff-review", with the PR description's change list as the approved plan. A file the description does not mention is drift unless it is a generated file the build wrote. Done when the review returns a verdict and every hunk has a label.
4. **Sweep the references.** For each new or renamed mode, step, option, report field or step number, search the whole skill folder, and every skill that calls it, for the places that name the old set, then read each one. Follow [references/sweep.md](references/sweep.md). Done when every place that mentions the changed thing is either updated in this PR or still true, with file:line for each one that is not.
5. **Check each new instruction can run.** For every added sentence that tells an agent to do something, answer three questions: who does it, in which step, and how they know it is done. Read [references/instruction-shape.md](references/instruction-shape.md) for the checks. Done when every new instruction has an actor, a step and a completion criterion, or a finding says which is missing.
6. **Check Rob's standing rules.** No skill text may tell an agent to approve, merge or force-push for Rob, to merge into a base branch without his review, or to skip a sign-off he set. Unfinished skills live in `drafts/`, not `skills/`. Done when each rule holds or has a finding.
7. **Give the verdict.** Write the report below. **Merge** when `make check` passes and steps 3 to 6 found nothing above a nit. **Fix first** when any finding would make an agent following the skill stall, contradict itself or act without a check. **Needs Rob's call** when the change is sound but alters a design decision in `docs/PLAN.md` or an ADR. Done when every finding has file:line, why it matters, and a draft comment written in Rob's voice.

## Output

```
## <PR number> <title>: merge | fix first | needs Rob's call
Head: <sha>   make check: pass | fail (<line>)

## Findings
1. <file:line>: <what breaks, for which agent, in which step>. Fix: <one line>

## Draft comments
- <file:line>: <comment, first person as Rob, plain, no em dashes>
```
