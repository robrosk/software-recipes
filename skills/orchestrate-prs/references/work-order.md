# Work order

Read this in step 6. The work order is the subagent's entire prompt. The subagent has not seen the design, the conversation, the other slices or this skill, so anything the work order leaves out, the subagent will guess.

## Rules for writing one

- **Paste, never point.** Interfaces, contract lines, conventions and commands go in verbatim. "See the design doc" or "as discussed" gives the subagent nothing.
- **Exact over descriptive.** File paths, symbol names, test names, commands and branch names, written out in full.
- **Done is a command.** Every done criterion is a test that passes or a command whose output changes. "Works correctly" is not a criterion.
- **Say what not to do.** Off-limits files, patterns not to add and actions not to take are as much a part of the order as the goal.
- **Small and deep.** Ask for a lot of behavior behind the slice's small interface, and nothing outside it.
- **One voice.** Second person, imperative, short sentences.

## Template

Fill every section. Write "none" in a section that truly has nothing, so the lint can tell an empty section from a forgotten one.

````
# Work order: <wave>-<slice>

## Goal
<One sentence: what this slice delivers, in the system's own terms.>
Done when: <the one command or test that proves it>.

## Where this fits
<Three to five sentences: what the system is, what this component is
responsible for, who calls it and what it calls. Name only components
whose interfaces appear below.>

## Contract lines you implement
<Each item, id and full text, that this slice must make true, with the
test that proves it.>
- NEVER-2: "An invoice is never created twice for one order."
  Test: `test_create_invoice_is_idempotent_per_order`

## Contract lines to respect
<Items another slice implements that this code must not break. "none" if none.>

## Interfaces you implement
<Verbatim code from the seams file, with its path. Implement exactly
these signatures. Do not change them.>

```<language>
# path/to/seams/file
<interface code>
```

## Interfaces you call
<Verbatim code, with its path, for every interface this slice consumes.
In tests, use the fakes listed under Fixtures.>

## Files
- You own (create or change only these): <paths or globs>
- You read, never change: <paths>
- Off limits (other slices own them): <paths or globs>

## Fixtures and fakes
<Paths of the shared fakes and fixtures from the seams slice to use in tests.>

## Design rules
- Patterns: <each admitted pattern from the design that applies here,
  with where it goes and the error it rules out>. Add no other design
  pattern, abstraction layer or extension point.
- Dependencies: <how collaborators are passed in: constructor injection,
  function arguments; and the lifetime of each service if named>.
- Errors: <which error types to raise or return, and what to do on each
  FAIL item this slice handles>.
- Reuse: <existing helpers in the repo to use instead of writing new
  ones>. Write no helper that duplicates one already in the repo or in
  the seams file.

## Conventions
<Pasted from AGENTS.md, CONTRIBUTING.md, the linter config and the
glossary: naming, formatting, import style, logging, docstrings,
terms to use.>

## Steps
1. Write the tests listed under "Tests that define done". Run them and
   confirm each one fails for the reason it names.
2. Implement until they pass. Keep the change inside the files you own.
3. Run `<check command>` and fix everything it reports in your files.
4. Commit on branch `<branch>` from `<base>` with message
   `<conventional message>`, then push. Open a pull request against
   `<target branch>` with the description below. <Or, when the
   orchestrator opens PRs: stop after the commit and report.>

## Tests that define done
| Test | Asserts | Covers |
| `test_create_invoice_is_idempotent_per_order` | a second create for one order returns the first invoice | NEVER-2 |

Done when every test above passes, `<check command>` passes, and
`git diff --name-only <base>...HEAD` lists only files you own.

## Stop and ask
Stop, change nothing more, and report the question when any of these happen:
- An interface above cannot express what this slice needs.
- You need to change a file you do not own, or add a dependency to a
  manifest you do not own.
- A contract line conflicts with another, or with an interface.
- A test cannot pass without changing code outside your files.
- Two readings of this order are both reasonable and lead to different code.
Never work around a stop by editing another file, widening an interface
or skipping a test.

## Never
- Merge, force-push, or push to any branch but `<branch>`.
- Spawn subagents.
- Disable, skip or delete a test to get the check green.
- Add a pattern, layer or option this order does not ask for.

## Pull request
Title: <imperative, under 70 characters>
Body:
<the repo's PR template when it has one, otherwise:>
- What this adds: <one paragraph, user-visible terms>
- Contract: <ids covered, each with its test>
- Files: <owned files changed>
- Stacked on: <#pr, or "none">
- Verification: <check command> passes; <tests> pass.
<Then this whole work order inside a collapsed details block, so the
reviewer can check the diff against it.>

## Report back
Return only this:
- Status: done | stopped
- PR: <url, or branch and commit when the orchestrator opens PRs>
- Tests: <each test from the table, pass or fail>
- Check: pass | fail, with the first failing line
- Files changed: <list>
- Stopped on: <the question, the file or line that raised it, and the
  options you see>, or "none"
- Needs from others: <a dependency, a wiring entry, a seam change>, or "none"
- Surprises: <anything in the repo that contradicted this order>, or "none"
````

## Seams and wiring orders

The seams order has no "Interfaces you call" and its tests check that every stub raises "not implemented" and every fake satisfies its interface. Its "Stop and ask" adds: a shape that two contract items need differently.

The wiring order owns the composition root and registries, and its tests are the end-to-end `SCN` scenarios that need every slice. Its "Interfaces you call" lists every slice's public entry point as merged, so write it after the last implementation wave merges, during step 14.
