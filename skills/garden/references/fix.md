# Fixing a find

Read the section for this find's bin in step 10. Both kinds share one rule: the fix uses what the design already has. Reuse the modules, seams and patterns the design doc and the code already hold; when a fix seems to need something new, stop and make it a question.

## Weed

- **One kind of change.** A deletion, a move, a dedupe, a doc fix, a type tightening or a missing test, never several mixed. Mixed diffs hide which change broke a behavior.
- **The deletion test.** Name what code this change lets you remove, and give a reason when the change adds more than it removes. A new test is exempt.
- **Behavior unchanged.** Every test that passed before still passes. The acceptance condition is that the guarantee still holds, never that a warning went away.
- **A new contract test must pass on the current code.** It pins behavior that already holds. When it fails, garden has found a bug: keep the test, switch this find to the Bug bin, and fix it with the steps below on the same branch.

## Bug

- **Test first.** Write a test that fails for the reason the contract item names, run it on the untouched branch, and keep its failure output for the PR. A test that passes before the change does not prove the bug.
- **The cause, not the symptom.** Find where in the code the wrong behavior comes from and why, then make the smallest change that removes that cause. A guard that hides the wrong outcome at one call site, when the cause is shared, is a symptom fix.
- **Fit the design.** Put the fix where the design says that behavior lives, in that module's own style, through the seams that already exist. Extending an existing pattern to cover a case it missed is a fit; adding a new pattern or a new layer is not.
- **Nothing beyond the item.** The diff changes behavior only as far as the contract item requires. Other behavior, including what callers see, stays as it was.
- **Prove it.** The new test failed before the change and passes after, and the project's check passes.
