---
name: garden
description: "Tend a codebase back toward its docs: several different models sweep every kind of drift against the design doc and contract, then each confirmed weed or contract bug gets its own pull request right away, explaining what drifted, why, and why the fix fits the existing design, and any weed that comes back becomes a lint rule."
disable-model-invocation: true
license: MIT
metadata:
  display-name: Garden
  short-description: Multi-model sweep, one fix PR per find
---

# Garden

Agents copy whatever patterns they find in a codebase, good or bad, so drift that sits still spreads. Garden pulls the code back toward its docs in small, safe steps: the codebase should say what the design doc, the contract and the repo's rules say. Several models sweep for drift independently, the main agent confirms every find, and each confirmed find gets its own pull request right away. The user merges every PR.

The run has five passes:

1. **Yardstick**: the design doc, the contract and the repo's own rules, plus a green baseline.
2. **Sweep**: several sweepers, each on a different model, sweep every bed in the checklist on their own.
3. **Triage**: merge and confirm the finds, bin each as weed, bug, question or leave, and rank them.
4. **Fix**: one find per pull request, in rank order, each explaining the drift, its cause and why the fix fits the design.
5. **Learn**: a weed that comes back becomes a deterministic check, and the ledger records the run.

The yardstick decides everything. A find names the line of the design, contract or rule it drifts from; a find with nothing to point at is taste, and garden drops it.

Run garden from a session on the strongest model you have. The sweepers supply the variety; the main agent confirms every find and writes every fix.

## What garden never does

Garden brings code in line with what the docs already say. It never decides what the docs should say. It never adds a new abstraction or design pattern, changes a public interface or a seam, edits a contract item, renames against `GLOSSARY.md`, upgrades a dependency in a way that changes behavior, reformats what the formatter owns, touches security without asking, or merges a pull request. Each of those becomes a question for the user instead.

A weed PR changes structure and never behavior. A bug PR changes behavior only where a contract item already says what the code must do, and nothing beyond that item.

## Pass 1: yardstick

1. **Set the scope.** Garden the whole repo unless the user names paths or a commit range. After an orchestrate-prs wave, the scope is that wave's merged range plus the files that import what it changed. Done when the scope is written as a path list or a commit range.
2. **Load the yardstick.** Read the design doc from design-the-system (`docs/design/*.md`) when one exists: its contract (`INV`, `NEVER`, `SCN`, `FAIL`, `Q` items), Architecture table and Patterns table with each pattern's "error it rules out". Read a plan from plan-the-change when the user points at one. Then read `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md`, `docs/adr/`, the lint and test config, and the ledger at `docs/garden/ledger.md` from earlier runs. When there is no design doc, garden against the docs and rules that exist, mark beds 1 and 2 in [references/beds.md](references/beds.md) as limited, and offer `/design-the-system` for next time. Done when every yardstick source is read or recorded as missing.
3. **Get a green baseline.** Find the base branch and the one command that checks the project (tests plus lint), and run it on the base. Done when the check passes on the base, or the user has accepted a named failing baseline. Garden fixes nothing on an unexplained red baseline, because it could not tell its own breakage from what was already broken.

## Pass 2: sweep

4. **Pick the sweepers.** Read the section for your harness in [references/platforms.md](references/platforms.md) and pick one sweeper per model it lists, each with its own lens from [references/sweeper-brief.md](references/sweeper-brief.md). On GitHub Copilot the models come from as many different labs as the user's plan offers; on Claude Code they are the different Claude models; on Codex they are the models the session's provider offers. Name models by alias or as "the strongest each lab offers", never by a pinned version. Done when every sweeper has a model, a lens, and no two sweepers share a model.
5. **Release the sweepers.** Launch every sweeper in parallel with the brief in [references/sweeper-brief.md](references/sweeper-brief.md). Each one sweeps every bed in [references/beds.md](references/beds.md) across the whole scope, on its own, and changes no file. Skip anything the ledger marks Leave unless the code around it changed. Done when every sweeper has returned a report with every bed, 1 to 19, marked with finds or "clear", or its timeout and last action are recorded.

## Pass 3: triage

Read [references/triage.md](references/triage.md) before step 6; it holds the merge rules, the bin rules and the ranking rubric.

6. **Merge the finds.** Merge finds that name the same place and the same drift into one entry, and record which sweepers raised it. Keep every place a repeated find showed up. No PR opens until this merge is done, so two models never get two PRs for one find. Done when every sweeper's find maps to exactly one entry.
7. **Confirm and bin.** Treat every entry as a smell until you have read the code and the yardstick line it names yourself; a find one sweeper raised counts as much as one every sweeper raised, once you have confirmed it. When code and docs disagree, decide which side is wrong with the rules in triage.md: fix the doc when it is stale, fix the code when the contract says what it must do, and make it a question when the design itself is in question. Then put it in one bin: **Weed** (a behavior-preserving repair), **Bug** (the code breaks a contract item that says what it must do), **Question** (needs a decision only the user can make) or **Leave** (correct code, no change, one line saying why). A pattern that rules out no named failure is a weed to remove only when the design doc did not choose it; when the doc chose it, it is a question. A fix that seems to need a new pattern is a question for design-the-system, never a weed or a bug. Done when every entry is in exactly one bin with its reason.
8. **Rank and post the plan.** Score each weed and bug by spread, then risk, then cost, with the rubric in triage.md, and mark every **repeat**. Post the ranked table below, with the questions, and go straight on to step 9: the top weeds and bugs get a PR this run, up to the cap in triage.md (ten unless the user named another number or said no cap), and the rest go to the backlog. Stop for a sign-off only when the user asked for one up front. Done when the table is posted and every weed and bug has a rank and is marked fix now or backlog.

```
| # | Find | Kind | Bed | Where | Drifts from | Found by | Spread | Risk | Cost | Repeat |
```

## Pass 4: fix

Fix one find at a time, in rank order.

9. **Branch and prove the baseline.** Branch `garden/<n>-<slug>` from the base branch, not from another find, so each PR merges on its own. When this find touches the same lines as an open garden PR, branch from that PR and say so in the description. When an earlier PR in this run already removed this find, record it as covered by that PR and go to the next. Run the check on the new branch before changing anything. Done when the check passes on the untouched branch.
10. **Fix it.** Read the rules for your bin in [references/fix.md](references/fix.md). For a weed, make one kind of behavior-preserving change and run the deletion test. For a bug, write a test that fails for the contract item's reason first, then the smallest change that makes it pass, aimed at the cause, using the modules and patterns the design already has. When a weed's new contract test fails, the weed is a bug: keep the test and fix it as a bug on the same branch. When the fix turns out to need a design decision, stop this find, move it to the Question bin with what you learned, and go to the next. Done when the check passes, every test that passed before still passes, and a bug's new test failed before the change and passes after.
11. **Review the diff.** Call the Skill tool with "surgical-diff-review", with this one find as the ask and the drifted yardstick line as the goal. Apply the actions it proposes that keep the diff to this find. Done when the verdict is clean and every changed line serves this find.
12. **Open the PR.** Commit, push the branch, and open a pull request against the base with the description from [references/fix-pr.md](references/fix-pr.md): what drifted or broke, its cause, the fix, and why the fix fits or naturally extends the existing design. Never merge it; the user reviews and merges every garden PR. Done when the PR is open and every section of its description is filled.

## Pass 5: learn

13. **Turn repeats into checks.** For each repeat weed, write the deterministic check that would have caught it: a lint rule, a validator rule or a test, with the file it belongs in and the places it would flag today. Fall back to a line in `AGENTS.md` only when no machine can catch it, and say why. Offer the user `/reflect` to turn these into accepted edits; garden proposes checks and never adds one to the repo unasked. Done when every repeat has a proposed check or a reason no machine can catch it.
14. **Update the ledger.** Write this run into `docs/garden/ledger.md` with the format in [references/ledger.md](references/ledger.md): the date, scope and sweepers, a grade per area, every weed and bug with its PR, every question, every Leave with its reason, and the backlog. Commit it on its own branch `garden/ledger-<date>` and open it as a docs-only pull request. Done when the ledger PR is open and every entry from step 7 appears in it exactly once.
15. **Report.** Write the report below. List under Upstream every entry where the doc was the wrong side or the design is in question, with the step that should have kept the doc right, and offer `/reflect` for those. Done when every entry from step 7 appears in exactly one of Fixed, Covered by an earlier fix, Questions for you, Backlog or Left alone.

## Output

```
# Garden report: <repo or scope>

Yardstick: <design doc | docs and rules only>   Scope: <paths | range>   Baseline: <green | accepted red: reason>
Sweepers: <model and lens per sweeper>

## Grades
| Area | Grade | Last run | Why |

## Fixed
| # | Find | Kind | Drifts from | Found by | PR |

## Covered by an earlier fix
- <find>: covered by PR <link>

## Questions for you
- <question>: <the decision it needs, and the option you would pick with one reason>

## Upstream: docs that fell behind
- <find>: <the doc that was wrong, and the step that should have kept it right>

## Make it a check
- <repeat weed>: <proposed rule or test, where it lives, what it flags today>

## Backlog
- <find not fixed this run>: <rank, and why it waited>

## Left alone
- <find>: <why the code is correct>
```
