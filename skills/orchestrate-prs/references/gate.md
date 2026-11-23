# Gate

Read this in step 12 for each PR, and in step 14 after each wave merges.

## The PR gate (step 12)

Run these in order and stop at the first failure; later checks are wasted on a PR that fails an earlier one.

1. **Ownership.** `git diff --name-only <target>...<branch>` lists only files the work order owns. Any other file fails the gate, whatever the change is.
2. **Report matches.** The subagent's report says done, lists every test from the order as passing, and names no stop. A report that says done but lists a stop is treated as stopped.
3. **Tests exist and fail without the change.** Each test in the order's table is in the diff. For at least the tests covering `NEVER` and `INV` items, check out the target branch with only the test files applied and confirm they fail.
4. **Check passes.** Run the project's check command on the branch, in a clean working copy. Do not trust the subagent's own run.
5. **Surgical review.** Call the Skill tool with "surgical-diff-review". Give it the work order as the approved plan: the order's Goal and done line as the goal and its check, the "Tests that define done" table as the slices, and the "Never" section, "Off limits" files and any pattern not in "Design rules" as the cut. A pattern or abstraction the order did not name is drift.
6. **Contract spot check.** For each contract line the order implements, read the code path that makes it true and confirm the test exercises that path, not a mock of it.

A PR passes when all six hold. Record the verdict and the fix rounds.

## Fix rounds

When a PR fails, decide first whether the code or the work order is wrong:

- **The order was wrong or silent** (the subagent made a reasonable guess the order allowed): fix the order, lint it, and re-dispatch a fresh subagent on the same branch with the fixed order and the gate findings. Log it under "Work order fixes" in the report.
- **The code is wrong** (the order was clear and the subagent missed it): send the same subagent, or a fresh one with the order, the gate findings and the branch, back to fix only the findings.

At most two fix rounds per PR. After the second failed round, stop, flag the PR to the user with the findings, and leave it open. Never fix a subagent's PR by hand in a way the order would not have allowed; that hides the gap from the next run.

## After a wave merges (step 14)

1. Fetch and check out the base branch as merged.
2. Run the project's check, then every test written for a contract item in this and earlier waves. A test that passed in its PR and fails here is an integration bug; it becomes a new slice in the next wave, with its own work order.
3. Diff each seam as it now exists in the code against the seam pasted in the remaining work orders. Any difference, even a renamed parameter, means each order that pastes it is updated and linted again (checks 3, 4 and 16).
4. Read every "Needs from others" and "Surprises" line in this wave's reports. Route each to the order it affects: a manifest entry to wiring, a seam change to seams and its callers, a repo fact to the conventions of every remaining order.
5. When the next wave is wiring, write its order now, against the merged entry points.

Done when the check and every contract test pass on the merged base, and every remaining order has been updated and passes the lint.
