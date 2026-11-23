# Work order lint

Read this in step 7, and again in steps 11 and 14 for any order you change. A failure here costs one edit; the same gap found by a subagent costs a wasted run and a bad PR.

## Per-order checks

Run each check on each order. Every failure names the order, the section and the fix.

| # | Check | Fails when |
| --- | --- | --- |
| 1 | Every section filled | A template section is missing or blank. "none" passes. |
| 2 | Standalone | The order says "the design", "above", "as discussed", "the other slice", "see doc", or uses a name that is neither defined in the order nor present in the repo at the base. |
| 3 | Interfaces verbatim | An interface in the order differs, by one character, from the seams file it cites. |
| 4 | Interfaces complete | The goal or a test uses a type or function the order does not paste or the repo does not already have. |
| 5 | Done is executable | A done criterion or a test row is not a runnable test name or command. |
| 6 | Tests cover the contract | A contract line under "you implement" has no test row, or a test row covers no line. |
| 7 | Files listed | A file the steps or tests must touch is missing from "You own". |
| 8 | Patterns bounded | The order names a pattern that is not in the design's Patterns table, or does not forbid adding others. |
| 9 | Stops present | "Stop and ask" or "Never" is missing any line from the template. |
| 10 | Size | The estimated change is over about 400 lines, not counting tests. Split the slice. |
| 11 | Branch and target | Branch, base and PR target are missing, or a stacked order does not name its parent PR. |

## Cross-order checks

Run once across all orders.

| # | Check | Fails when |
| --- | --- | --- |
| 12 | Disjoint ownership | One path or glob matches files owned by two orders. |
| 13 | Off limits complete | An order's "Off limits" leaves out a path another order owns. |
| 14 | Contract coverage | A contract item is implemented by zero orders, or by two. |
| 15 | No duplicate symbols | Two orders each ask for a new function, type or helper with the same job. Move it to seams or to one order, and have the other import it. |
| 16 | Interface agreement | The implementing order and every calling order paste the same version of an interface. |
| 17 | Waves consistent | An order calls real behavior from a slice in the same or a later wave. |

## The cold read

Lint catches what is missing from the template. The cold read catches what is missing from the reader's head.

For each order, launch one fresh subagent with read-only tools and no other context. In parallel is fine. Give it the order and this prompt:

````
Below is a work order for a coding task in this repository. Do not write
or change anything. Read the order, then read any repository files it
names.

List every question you would need answered before you could finish the
task without guessing. For each one, say which section of the order
raised it and what you would have guessed.

Then list any instruction you could follow in two different ways that
would lead to different code.

If you have no questions and no double readings, reply exactly: READY.

<work order>
````

A question the repo or the order already answers is not blocking; note it and move on. Every other question means the order changes: answer it in the order itself, then lint that order again. Do not answer the cold reader, since the real subagent will not have your answer either.

Done when every order passes checks 1 to 17 and its latest cold read is READY or lists only non-blocking questions.
