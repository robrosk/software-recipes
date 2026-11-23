---
name: garden
description: "Tend a codebase back toward its design: sweep every kind of drift against the design doc and contract, rank the weeds by how far they would spread, then pull each one in its own small behavior-preserving pull request and turn any weed that comes back into a lint rule."
disable-model-invocation: true
license: MIT
metadata:
  display-name: Garden
  short-description: Sweep for drift, one weed per PR
---

# Garden

Agents copy whatever patterns they find in a codebase, good or bad, so drift that sits still spreads. Garden pulls the code back toward its design in small, safe steps. It finds drift, decides what is worth touching, and pulls each weed in its own behavior-preserving pull request. The user signs off the weed list once and merges every PR.

The run has five passes:

1. **Yardstick**: the design doc, the contract and the repo's own rules, plus a green baseline.
2. **Sweep**: every bed in the checklist, each marked with findings or "clear".
3. **Triage**: confirm each finding, bin it as weed, question, leave or bug, rank the weeds, and get one sign-off.
4. **Prune**: one weed per pull request, tests green before and after.
5. **Learn**: a weed that comes back becomes a deterministic check, and the ledger records the run.

The yardstick decides everything. A finding names the line of the design, contract or rule it drifts from; a finding with nothing to point at is taste, and garden drops it.

## What garden never does

Garden changes structure, never behavior. It never changes what the system does, adds a new abstraction or design pattern, changes a public interface or a seam, renames against `GLOSSARY.md`, upgrades a dependency in a way that changes behavior, reformats what the formatter owns, fixes a bug, or merges a pull request. Each of those becomes a question or a bug for the user instead.

## Pass 1: yardstick

1. **Set the scope.** Garden the whole repo unless the user names paths or a commit range. After an orchestrate-prs wave, the scope is that wave's merged range plus the files that import what it changed. Done when the scope is written as a path list or a commit range.
2. **Load the yardstick.** Read the design doc from design-the-system (`docs/design/*.md`) when one exists: its contract (`INV`, `NEVER`, `SCN`, `FAIL`, `Q` items), Architecture table and Patterns table with each pattern's "error it rules out". Read a plan from plan-with-patterns when the user points at one. Then read `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md`, `docs/adr/`, the lint and test config, and the ledger at `docs/garden/ledger.md` from earlier runs. When there is no design doc, garden against the docs and rules that exist, mark beds 1 and 2 in [references/beds.md](references/beds.md) as limited, and offer `/design-the-system` for next time. Done when every yardstick source is read or recorded as missing.
3. **Get a green baseline.** Find the base branch and the one command that checks the project (tests plus lint), and run it on the base. Done when the check passes on the base, or the user has accepted a named failing baseline. Garden prunes nothing on an unexplained red baseline, because it could not tell its own breakage from what was already broken.

## Pass 2: sweep

4. **Sweep every bed.** Work through each bed in [references/beds.md](references/beds.md) across the scope, asking its question and looking for its signals. Skip anything the ledger marks Leave unless the code around it changed. For a large scope, split the beds across 2 to 4 read-only sweepers with the brief in [references/sweeper-brief.md](references/sweeper-brief.md), then merge their findings yourself. Every finding cites `file:line`, the yardstick line, contract id or rule it drifts from, and the evidence. Done when every bed, 1 to 19, has findings or the word "clear" with one line on what was checked.

## Pass 3: triage

Read [references/triage.md](references/triage.md) before step 5; it holds the bin rules, the ranking rubric and the budget.

5. **Confirm and bin.** Treat every finding as a smell until you have read the code and the yardstick line it names. Then put it in one bin: **Weed** (a behavior-preserving repair that fits one small PR), **Question** (needs a design decision, so it goes to the user), **Leave** (correct code, no change, one line saying why) or **Bug** (the code breaks the contract, so fixing it changes behavior). A pattern that rules out no named failure is a weed to remove only when the design doc did not choose it; when the doc chose it, it is a question. A repair that seems to need a new pattern is a question for design-the-system, never a weed. Done when every finding is in exactly one bin with its reason.
6. **Rank the weeds.** Score each weed by spread, then risk, then cost, with the rubric in triage.md. Mark a weed as a **repeat** when it shows up in two or more places in this run, or the ledger already holds it from an earlier run. Done when the weeds are in rank order and every repeat is marked.
7. **Get one sign-off.** Show the user, in one message, the ranked weed table below, the questions, and the bugs. Ask which weeds to pull; the default is the top five (the budget in triage.md). Questions and bugs do not block pruning. When the user said up front to skip this stop, post the table and pull the default. Done when the user has signed off the pull list, or said up front to skip it.

```
| # | Weed | Bed | Where | Drifts from | Spread | Risk | Cost | Repeat |
```

## Pass 4: prune

Pull one weed at a time, in rank order.

8. **Branch and prove the baseline.** Branch `garden/<n>-<slug>` from the base branch, not from another weed, so each PR merges on its own. When this weed touches the same lines as an open weed PR, branch from that PR and say so in the description. Run the check on the new branch before changing anything. Done when the check passes on the untouched branch.
9. **Pull the weed.** Make one kind of change only: a deletion, a move, a dedupe, a doc fix, a type tightening or a missing test, never several mixed. Run the deletion test: name what code this change lets you remove, and give a reason when the change adds more than it removes (a new test is exempt). A new test for a contract item must pass on the current code; when it fails, garden has found a bug, so stop this weed, move it to the Bug bin with the failing test as its evidence, and go to the next weed. Done when the change is one kind, the check passes, and every test that passed before still passes.
10. **Review the diff.** Call the Skill tool with "surgical-diff-review", with this one weed as the ask and the drifted yardstick line as the goal. Apply the actions it proposes that keep the diff to this weed. Done when the verdict is clean and every changed line serves this weed.
11. **Open the PR.** Commit, push the branch, and open a pull request against the base with the description from [references/weed-pr.md](references/weed-pr.md). Never merge it; the user reviews and merges every garden PR. Done when the PR is open and every section of its description is filled.

## Pass 5: learn

12. **Turn repeats into checks.** For each repeat weed, write the deterministic check that would have caught it: a lint rule, a validator rule or a test, with the file it belongs in and the places it would flag today. Fall back to a line in `AGENTS.md` only when no machine can catch it, and say why. Offer the user `/reflect` to turn these into accepted edits; garden proposes checks and never adds one to the repo unasked. Done when every repeat has a proposed check or a reason no machine can catch it.
13. **Update the ledger.** Write this run into `docs/garden/ledger.md` with the format in [references/ledger.md](references/ledger.md): the date and scope, a grade per area, every weed with its PR, every question, every Leave with its reason, and the backlog of weeds not pulled. Commit it on its own branch `garden/ledger-<date>` and open it as a docs-only pull request. Done when the ledger PR is open and every finding from step 5 appears in it exactly once.
14. **Report.** Write the report below. Done when every finding from step 5 appears in exactly one section.

## Output

```
# Garden report: <repo or scope>

Yardstick: <design doc | docs and rules only>   Scope: <paths | range>   Baseline: <green | accepted red: reason>

## Grades
| Area | Grade | Last run | Why |

## Pulled
| # | Weed | Bed | Drifts from | PR |

## Questions for you
- <question>: <the decision it needs, and the option you would pick with one reason>

## Bugs found
- <bug>: <contract item it breaks, the evidence, and the failing test when there is one>

## Make it a check
- <repeat weed>: <proposed rule or test, where it lives, what it flags today>

## Backlog
- <weed not pulled this run>: <rank, and why it waited>

## Left alone
- <finding>: <why the code is correct>
```
