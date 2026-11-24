---
name: break-it
description: "Hunt for bugs in a running app: pin down how the system must behave, send ten subagents, each driving its own browser, to use it and break it, triage what they find, then fix each confirmed bug in its own pull request."
disable-model-invocation: true
license: MIT
metadata:
  display-name: Break It
  short-description: Ten hunters, triage, one PR per bug
---

# Break it

Find the bugs real users would hit, then fix them one at a time. The run has four passes and the main agent owns every decision between them.

1. **Contract**: what the system must always do, never do, and how it fails. Taken from the docs when they say it, grilled out of the user when they do not.
2. **Hunt**: ten subagents drive the running app like real users and report bugs. They find; they never fix.
3. **Triage**: the main agent dedupes, reproduces and ranks every report against the contract.
4. **Fix**: the main agent fixes confirmed bugs in rank order, one bug per pull request.

The contract is the yardstick for all four. A hunter's report names the contract line it breaks, triage ranks by it, and each fix PR explains the bug in its terms.

## Pass 1: contract

1. **Read what the project already says.** Read the design doc from design-the-system (`docs/design/*.md`) when one exists, then `README.md`, `GLOSSARY.md`, `docs/adr/`, specs and the key tests. Extract every statement of system behavior into four kinds: `INV-n` (always true), `NEVER-n` (must not happen), `SCN-n` (given, when, then) and `FAIL-n` (a dependency or input fails, the system responds). Keep the source of each item. Done when each kind is marked **stated** (with items and sources) or **missing**, using the test in [references/contract-grill.md](references/contract-grill.md).
2. **Grill the gaps.** When every kind is stated, skip to step 3: the docs already tell. Otherwise grill the user on the missing kinds only, with the questions and interview rules in [references/contract-grill.md](references/contract-grill.md): one question per message, the user answers first, your recommendation after. If the user would rather design the whole system first, tell them to run `/design-the-system` and resume break-it with its doc. Done when every kind has at least one item, each written with its id.
3. **Set the hunting ground.** Settle how the app starts, where hunters reach it (URL, command, device), which test accounts and seed data each hunter gets, what is off limits (production, real email or SMS, real payments, third-party APIs with side effects), and the time budget per hunter. Start the app and run one smoke check through the same interface the hunters will use. Done when the app is up, the smoke check passes, the target is not production, and the user has signed off the contract and the ground together in one message.

## Pass 2: hunt

4. **Fit the run to this harness.** Read the section for the harness you are running in from [references/platforms.md](references/platforms.md). Confirm three things: you can spawn ten subagents, each one can drive the app (a browser tool, or a terminal for a CLI app), and each gets its own browser and test account so hunters cannot corrupt each other's state. Check the last one with the isolation probe in that file. When one is missing, tell the user which and offer the fallback that section names. Done when all three are confirmed or the user has accepted a fallback.
5. **Brief ten hunters.** Build each brief from the template in [references/hunter-brief.md](references/hunter-brief.md): the contract, the hunting ground, the rules and the report format. On Claude Code and Codex, give each hunter one persona from [references/personas.md](references/personas.md), all ten distinct. On GitHub Copilot, give every hunter the same unscripted brief and pin each to a different model, spread across as many labs as the roster in [references/platforms.md](references/platforms.md) offers; the models are the diversity. Done when ten briefs exist and no two share a persona (or, on Copilot, a model).
6. **Release the hunters.** Launch all ten in parallel and wait for every one. Hunters change no code and do not restart the app; if the app goes down, record which hunter and what it was doing, restart it yourself and let the rest continue. Done when each hunter has returned a report, or its timeout and last action are recorded.

## Pass 3: triage

7. **Merge the reports.** Group reports by root symptom: the same wrong outcome from the same action is one bug, even when hunters reached it by different paths. Keep every distinct repro path under the one entry and note which hunters found it. When unsure whether two reports are one bug, use the merge rules in [references/triage.md](references/triage.md). Done when every report maps to exactly one entry and no two entries describe the same wrong outcome.
8. **Reproduce each bug yourself.** Follow each entry's steps from a fresh state on the hunting ground. Mark it **confirmed**, **flaky** (with the hit rate), **not reproduced** (with what you saw), or **not a bug** (the contract allows it; quote the line). Done when every entry has a status and its evidence.
9. **Rank and get the fix list.** Rank confirmed and flaky bugs with the rubric in [references/triage.md](references/triage.md). Show the user the ranked table and ask which to fix; "all confirmed" is the default answer. Done when the user has signed off the fix list.

## Pass 4: fix

Work on one bug at a time, in rank order. Keep a local integration branch, `break-it/integration`, that starts at the base branch and gains each finished fix; never push it. It exists so each later bug is re-checked against every earlier fix.

10. **Re-check before fixing.** Rebuild the app from `break-it/integration` and re-run this bug's repro. When it no longer reproduces, record which earlier fix covered it, add one line to that fix's PR saying so, and move to the next bug. Done when the bug is confirmed still present or recorded as covered.
11. **Fix it alone.** Branch `break-it/<n>-<slug>` from the base branch, not from another fix, so each PR merges on its own. When this fix must touch the same lines as an open fix PR, branch from that PR instead and say so in the description. Write a test that fails for this bug's reason first, then the smallest change that makes it pass, aimed at the cause rather than the symptom. Done when the new test failed before the change and passes after, the project's own check passes, and the repro no longer reproduces.
12. **Review the diff.** Call the Skill tool with "surgical-diff-review", with this one bug as the ask. Apply the actions it proposes that keep the diff to this bug. Done when the verdict is clean and every changed line serves this bug.
13. **Open the PR.** Commit, push the branch, and open a pull request against the base with the description from [references/fix-pr.md](references/fix-pr.md): the bug, how to reproduce it, its cause, the fix, and why this fix is the correct one with the alternatives you rejected. The description covers this bug and nothing else. Then merge the fix into `break-it/integration` locally. Done when the PR is open, its description has every section filled, and the integration branch holds the fix.

Never merge a fix PR. The user reviews and merges every one.

14. **Report.** Write the report below. Done when every entry from step 7 appears in exactly one section.

## Output

```
# Break-it report: <system>

Contract: <n items> (<stated in docs | grilled | both>)
Hunters: <10 personas | 10 models across <k> labs>, <minutes> each

## Fixed
| # | Bug | Contract | Severity | PR |

## Covered by an earlier fix
- #<n> <bug>: covered by PR <link>

## Not fixed
- #<n> <bug>: <user left it off the list | flaky, <rate> | not reproduced: <what you saw> | not a bug: <contract line>>

## Held up
- <what hunters tried that behaved as the contract says, one line per area>
```
