---
name: orchestrate-prs
description: Turn a signed-off system design into one pull request per component, each built by a subagent from a meticulous standalone work order, dispatched in dependency waves and gated by review before you merge.
disable-model-invocation: true
license: MIT
metadata:
  display-name: Orchestrate PRs
  short-description: Design to waves of subagent PRs
---

# Orchestrate PRs

Build a large system as many small pull requests, each one written by a subagent that knows nothing but its work order. The main agent is the orchestrator: it slices the design, writes and lints every work order, dispatches the subagents in waves, and gates every PR. The user signs off the plan once and merges every PR.

The run has four passes:

1. **Ground**: a signed design and a green base branch.
2. **Slice**: freeze the seams, cut one slice per component with disjoint file ownership, and sort the slices into waves.
3. **Work orders**: one standalone brief per slice, linted until a cold reader has no questions, then one sign-off.
4. **Waves**: dispatch, gate, hand to the user, integrate, and update the remaining work orders. Repeat until the last wave merges.

A subagent's output can only be as good as its work order. When a subagent goes wrong, fix the work order first and the code second.

## Pass 1: ground

1. **Load the design.** Find the saved design doc from design-the-system (`docs/design/*.md`), or the one the user names. This doc is required: it must hold both the system-level behavior contract, signed (`INV`, `NEVER`, `SCN`, `FAIL` and `Q` items with ids), and the architecture (an Architecture table and a Patterns table). When there is no saved doc, the design lives only in the chat, or the doc is missing the contract or the architecture, stop before planning anything: tell the user to run `/design-the-system` first, which saves the doc, and resume orchestrate-prs with it. Done when the doc is loaded and every component in its Architecture table guarantees at least one contract item.
2. **Read the ground truth.** Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `GLOSSARY.md`, `docs/adr/`, the lint and test config, and the pull request template when they exist. Find the base branch and the one command that checks the project (tests plus lint), then run it on the base. Done when you know the base branch, the check command, the naming and style rules, and the check passes on the base, or the user has accepted a named failing baseline.

## Pass 2: slice

Read [references/slicing.md](references/slicing.md) before step 3; it holds the rules for seams, ownership, sizes and waves.

3. **Freeze the seams.** For every arrow in the design's data flow, write the exact interface in the project's language: types, function signatures, error types, events, schemas, and the dependency-injection lifetime of each service when the design names one. Put every shared type and interface in one **seams slice**, wave 0, that holds only those definitions, stubs that fail loudly, and shared test fixtures. Done when every cross-component call or message has one written interface, and each interface is defined in exactly one place.
4. **Cut the slices.** One slice per component from the Architecture table; split a component only when its slice would pass the size limit, and fold a tiny one into its nearest neighbor. Give each slice a disjoint set of owned files. Shared files (the composition root, registries, config, package manifests, lockfiles) belong to one **wiring slice**, last, or to the seams slice. Map each contract item to the one slice that implements and tests it. Done when the ownership check in slicing.md passes: file sets are disjoint, every contract item has exactly one slice, and every slice except seams and wiring covers at least one item.
5. **Sort into waves.** Draw the dependency graph: a slice depends on another when its tests need the other's real behavior, not just its seam. Sort the graph into waves; slices in one wave run in parallel. A cycle means a seam is missing, so move that interface into the seams slice and sort again. Choose the stacking mode with the rules in slicing.md: **wait** (default: a wave starts after the user merges the one before it), **stacked** (a slice with one unmerged parent branches from that parent's PR) or **single-branch** (each gated slice merges into one shared feature branch instead of opening its own PR). Done when every slice has a wave, the graph has no cycle, and the mode is chosen.

## Pass 3: work orders

6. **Write one work order per slice.** Fill the template in [references/work-order.md](references/work-order.md) for every slice, seams and wiring included. A work order is the subagent's whole world: paste interfaces, contract lines and conventions into it verbatim, never by reference. It names the design patterns from the design's Patterns table that apply to this slice and forbids adding others. Save each one to `.orchestrate/<system>/<wave>-<slice>.md`, and add `.orchestrate/` to `.git/info/exclude` so it is never committed. Done when every slice has a saved work order with every template section filled.
7. **Lint every work order.** Run the checks in [references/work-order-lint.md](references/work-order-lint.md): standalone, interfaces verbatim and matching the seams, executable done criteria, disjoint ownership, full contract coverage, no symbol defined twice across orders, and stop conditions present. Then run the cold read it describes: one fresh read-only subagent per work order lists the questions it would need answered before starting. Fix each order and lint it again. Done when every order passes every check and every cold read returns no blocking question.
8. **Get one sign-off.** Show the user the slice plan in one message: the table below, the stacking mode, and where the work orders are saved. Revise until the user signs off. When the user said up front to skip this stop, post the plan and go on. Done when the user has signed off, or said up front to skip it.

```
| Wave | Slice | Owns | Covers | Depends on | Est. lines |
```

## Pass 4: waves

Run steps 9 to 14 once per wave, starting with wave 0.

9. **Fit the run to this harness.** On the first wave only, read the section for your harness in [references/platforms.md](references/platforms.md). Confirm three things: you can run this wave's subagents in parallel, each one gets its own working copy, and you know who commits, pushes and opens the PR (the subagent or you). Check the first two with the probe in that file. When one is missing, tell the user which and offer the fallback that section names. Done when all three are confirmed or the user has accepted a fallback.
10. **Dispatch the wave.** Launch one subagent per slice in this wave, in parallel, each in its own working copy on its own branch, with its work order as its entire prompt. Subagents write tests first, implement, run the check and commit, and push and open the PR when step 9 found they can (in single-branch mode they stop after the commit); they never merge, never force-push, never spawn subagents and never touch files outside their ownership. Done when every subagent has returned a report in the work order's format, or its timeout and last action are recorded.
11. **Answer the stops.** For each subagent that stopped with a question, answer it from the design when the design settles it; otherwise ask the user, one question per message. When an answer changes a seam or a contract item, update the seams slice and every work order that pastes it, lint them again, and re-dispatch the affected slices. Done when no slice in this wave is waiting on an answer.
12. **Gate each PR.** Run the gate in [references/gate.md](references/gate.md) on every PR in the wave, or on every slice branch in single-branch mode: the ownership check on the changed file list, the project check, the work order's named tests, and a review by calling the Skill tool with "surgical-diff-review" with the work order as the approved plan. Send failures back with the findings for at most two fix rounds, then flag it to the user. Done when every PR in the wave (or slice branch, in single-branch mode) is clean or flagged with its reason.
13. **Hand the wave to the user.** Post the wave's PRs in merge order, each with its slice, the contract items it covers and its gate verdict. Never merge a PR; the user reviews and merges every one. In wait mode, hold the next wave until the user has merged this one. In single-branch mode there are no slice PRs: merge each clean slice branch into the shared feature branch yourself, remove its worktree, then post the feature branch with the wave's slices listed the same way, and leave each flagged branch unmerged. Done when every PR in the wave is merged, or the user has said how to proceed without one; in single-branch mode, when every clean branch is in the feature branch with its worktree removed and the user has said how to proceed with each flagged one.
14. **Integrate and update.** Pull the base branch (the shared feature branch in single-branch mode; read "merged base" below as that branch) and run the check, plus every test written for a contract item so far. Offer the user a garden pass on this wave's merged range: they run `/garden` and resume here once its fix PRs are merged or declined (in single-branch mode, tell `/garden` the feature branch is its base, so it sweeps that branch and its fix PRs target it), then you pull the base again. Compare the merged code's real interfaces with the seams; for any difference, and for anything a subagent's report flagged, update the remaining work orders and lint each changed one again. Done when the check passes on the merged base, the user has taken or declined the garden pass, and every remaining work order matches the code as merged.

15. **Report.** After the last wave, walk every contract item to its test and write the report below. In single-branch mode, open one PR from the feature branch against the base with the report in its description; the user reviews and merges it. Offer two next steps: run `/break-it` against the running system, and run `/reflect` to turn this run's lessons (work orders that needed fixes, stops that recurred) into skill edits. Done when every contract item appears in the report with a test and its status.

## Output

```
# Orchestrate-prs report: <system>

Design: <doc path>   Mode: <wait | stacked | single-branch>   Waves: <n>   PRs: <n>

## Pull requests
| Wave | Slice | PR | Covers | Gate | Fix rounds |

## Contract
| Item | Slice | Test | Status |

## Work order fixes
- <slice>: <what the order was missing, and how it was found: lint, cold read, stop, or gate>

## Open
- <flagged PR, deferred question or uncovered item, with what would settle it>
```
