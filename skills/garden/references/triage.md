# Triage

Read this before step 6. Triage is where garden stays useful instead of noisy: several sweepers raise many finds, most of them should end up merged, confirmed as weeds or bugs, or recorded as Leave, and "no change" is a normal, good answer.

## Merge first

Two finds are one entry when they name the same place and the same drift. Two finds at different places are separate entries even when the drift is the same; they make a repeat. When unsure, read both places: if one fix would remove both, they are one entry.

Record which sweepers raised each entry. That count is evidence for the report, not a vote: a find only one model raised is confirmed or dropped exactly like one every model raised, because catching what the other models miss is why there are several.

## Confirm

A find is a smell, a surface sign that usually points at a deeper problem and sometimes points at nothing. Before binning one, read the code it cites and the yardstick line it names. Drop it when either is missing, or when the code turns out to follow the yardstick after all; record the dropped ones in the Leave bin.

## Which side is wrong

When code and docs disagree, decide for each entry which side to fix before binning it. Garden never rewrites code to match a doc it has not checked is right.

- **The contract says what should happen:** the code is wrong. It is a bug.
- **The contract is silent and a README, ADR, comment or agent file describes code that has since moved on:** the doc is wrong. Fixing the doc is a weed.
- **Two docs disagree, or the code looks like a deliberate change the docs never caught up with:** the design itself is in question. It is a question, never a code change, because only the user decides what the design should be.
- **You cannot tell which side is right:** it is a question.

Write the side you picked, and why, in the entry's reason.

A wrong doc is also a sign that the process upstream let it fall behind. For each entry where the doc was the wrong side, or the design itself is in question, note in one line the step that should have kept it right: design-the-system for the design doc and contract, plan-the-change's Change log for a change that departed from the design, orchestrate-prs's integrate step for seams after a wave, or the PR that changed the code without touching its doc. These go in the report's Upstream section, so `/reflect` can fix the step rather than the same doc again next run.

## The four bins

| Bin | Rule | Goes to |
| --- | --- | --- |
| **Weed** | Fixing it changes structure and not behavior, needs no design decision, and fits one PR within the cost limit below. | A PR this run |
| **Bug** | The code breaks a contract item that says what it must do, and the fix fits the existing design within the cost limit below. Fixing it changes behavior, toward the contract. | A PR this run, test first |
| **Question** | Fixing it needs a decision: it moves a boundary, changes a seam or public interface, edits a contract item, removes a pattern the design doc chose, needs a new pattern, upgrades a dependency, touches security, might change timing, or the docs disagree with each other. | The user, in step 8 and the report |
| **Leave** | The code is correct, or the change would cost more than the drift. One line saying why. | The ledger, so the next run skips it |

A bug whose fix would need a new abstraction, a changed seam or more than the cost limit is a question, with the failing test as its evidence. Garden fixes bugs the design already has room for; a bug the design has no room for needs design-the-system or plan-the-change first.

When a rule keeps objecting to correct code, that is not a pile of weeds. It is one question: should the rule's scope change?

## Ranking

Rank weeds and bugs together. Sort by spread, then risk, then cost: the finds most likely to be copied go first, and among those, the ones nearest a contract item. Ranking sets the order PRs are opened in, which is also the order the user will see them.

**Spread**: how far it would travel.
- 3: already in three or more places, or in a file new code imitates (a template, base class, example, scaffold, or the module most recently copied).
- 2: in two places, or in a module many files import.
- 1: in one place that other code reads.
- 0: in one place nothing imports or copies.

**Risk**: what it puts at stake.
- 3: an `INV` or `NEVER` item.
- 2: an `SCN` or `FAIL` item.
- 1: a design rule, ADR or `AGENTS.md` rule, but no contract item.
- 0: hygiene only.

**Cost**: what the PR touches, lowest first.
- Small: one file and under 50 changed lines.
- Medium: up to five files and under 200 changed lines.
- Over medium: split it into finds that each fit, or move it to the Question bin, because it needs a plan.

## Repeats

A weed is a repeat when it shows up in two or more places in this run, or the ledger already lists the same drift from an earlier run. A repeat is still fixed in one PR that covers every place, when that fits the cost limit, and step 13 also proposes the check that keeps it from coming back. The second sighting is the signal: one sighting is an accident, two is a habit the repo is teaching.

## The cap

Open at most ten fix PRs per run, in rank order, unless the user names another number or says no cap. Every PR stays small and stands alone, so ten is a review session, not a flood. The rest go to the ledger's backlog, still ranked, so the next run starts from them. Duplicates never count against the cap, because step 6 merges every find before the first PR opens.
