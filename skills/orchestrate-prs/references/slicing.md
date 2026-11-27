# Slicing

Read this before step 3. Slicing decides whether parallel subagents can work without colliding, so every rule here exists to rule out one collision.

## Seams first

Parallel slices collide most at their edges: two subagents each invent the type they share, or one guesses the other's error shape. Freezing the seams before any work order rules that out.

The seams slice (wave 0) holds only:

- Every type, interface, protocol or abstract class that crosses a component boundary.
- Error types and event or message schemas that cross a boundary.
- Stubs for each interface that raise or return a "not implemented" error, so the code builds and imports before the real slices land.
- Shared test fixtures and fakes for those interfaces, so each slice tests against the same doubles.
- The dependency-injection registrations' shape (names and lifetimes: singleton, scoped or transient) when the design names them, never the real wiring.

It holds no behavior. A seams PR that does anything but define shapes is two slices.

Write each interface once, in one file the seams slice owns. Every other work order pastes the interface verbatim and imports it from that file. A second definition of the same shape anywhere is duplication and fails the lint.

## One slice per component

Start from the design's Architecture table, one row per slice. Then adjust:

- **Split** a component whose slice would pass about 400 changed lines, not counting tests and generated files, along a line the component already has: a sub-module, a layer, a separate command. Each part gets its own contract items.
- **Fold** a component under about 50 lines into the slice it talks to most, and list both component names in that slice's goal.
- **Vertical, not horizontal.** A slice delivers one component working end to end behind its seam, with its tests. A slice that is "all the models" or "all the tests" is a layer, not a slice, and cannot be checked against a contract item alone.

## Ownership

Every file the run will create or change has exactly one owning slice. A work order lists its owned files as paths or globs, and everything else is read-only or off limits to it.

Shared files are where parallel work collides, so they get an owner up front:

| Shared file | Owner |
| --- | --- |
| Interfaces, shared types, schemas, fixtures | seams slice |
| Composition root, DI container, registry, plugin list, router table | wiring slice |
| Package manifest, lockfile, build config | seams slice for dependencies known up front, wiring slice for the rest |
| Top-level docs, changelog | wiring slice |

A slice that needs a new dependency in a manifest it does not own lists it under "Needs from others" in its report; the wiring slice adds it. Two slices never edit the same lockfile.

### The ownership check (step 4)

1. List every owned path or glob across all slices. No path matches two slices.
2. Every file named in the design, and every file a slice must touch for its tests, has an owner.
3. Every contract item maps to exactly one slice. A cross-cutting item (for example `NEVER-1`, no duplicate charge) maps to the slice that enforces it; the others list it under "Contract lines to respect".
4. Every slice except seams and wiring covers at least one contract item. A slice that guarantees nothing is folded or cut.
5. Every existing service whose constructor parameters a slice adds or changes is registered in a block the wiring slice owns, or in lines the order grants that slice up front. Check the composition root (`Program.cs`, DI module, or registry) for registrations built by a manual factory lambda rather than automatic constructor resolution, since those break when the constructor changes.

Done when all five hold.

## Dependencies and waves

A slice depends on another only when its own tests need the other's real behavior. Depending on the other's interface is not a dependency: the seams slice already provides it.

Sort with a topological sort:

- Wave 0: seams.
- Wave 1: every slice that depends only on seams.
- Wave n: every slice whose dependencies are all in earlier waves.
- Last wave: wiring, which depends on every slice it registers.

A cycle means two slices need each other's real behavior, which almost always means a seam is missing. Move the shared shape into seams and sort again. If no seam breaks the cycle, merge the two slices into one.

When the harness caps concurrency below a wave's size, split the wave into sub-waves of equal size; they share a base and do not depend on each other.

## Stacking mode

Choose in step 5 and show it at sign-off.

**Wait (default).** Every PR targets the base branch. A wave is dispatched only after the user has merged the wave before it. Each PR is reviewed against real merged code, nothing needs restacking, and a fix in wave 1 never invalidates wave 2. Choose wait unless the user wants to keep subagents busy while reviews are pending.

**Stacked.** A slice whose dependencies are not merged yet starts anyway:

- With exactly one unmerged parent, it branches from the parent's PR branch and its PR targets that branch. The description opens with "Stacked on #<pr>: merge that first."
- With two or more unmerged parents, it waits. A branch built from several unmerged PRs cannot target any one of them cleanly.
- When a parent PR changes after review, rebase or merge the parent into each child branch and run the gate on the child again.
- After the user merges a parent, retarget the child PR to the base branch.

Stacked mode trades restacking work for speed. Choose it when the user asks, or when they ran stacked PRs on this repo before and said so.

**Single-branch.** When the user wants all waves on one feature branch instead of separate PRs per slice, run each slice in its own worktree branch, gate it in step 12, merge the gated branch into the shared feature branch, and remove the worktree before starting the next wave. Step 13 hands the user the feature branch instead of slice PRs, step 14 runs the check on the feature branch, and after the last wave you open one PR from the feature branch against the base, which the user reviews and merges. Choose it when the user asks for one feature branch, or wants to review the system as a whole rather than slice by slice.

## Branch names

`orchestrate/<system>/<wave>-<slice>`, for example `orchestrate/billing/1-invoice-store`. Use the project's own branch convention instead when `AGENTS.md` or `CONTRIBUTING.md` names one.
