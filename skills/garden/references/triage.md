# Triage

Read this before step 5. Triage is where garden stays useful instead of noisy: most of a sweep's findings should end up confirmed as weeds or recorded as Leave, and "no change" is a normal, good answer.

## Confirm first

A finding is a smell, a surface sign that usually points at a deeper problem and sometimes points at nothing. Before binning one, read the code it cites and the yardstick line it names. Drop it when either is missing, or when the code turns out to follow the yardstick after all; record the dropped ones in the Leave bin.

## The four bins

| Bin | Rule | Goes to |
| --- | --- | --- |
| **Weed** | Fixing it changes structure and not behavior, needs no design decision, and fits one PR within the cost limit below. | Step 6 ranking, then a PR |
| **Question** | Fixing it needs a decision: it moves a boundary, changes a seam or public interface, removes a pattern the design doc chose, needs a new pattern, upgrades a dependency, touches security, or might change timing. | The user, in step 7 and the report |
| **Leave** | The code is correct, or the change would cost more than the drift. One line saying why. | The ledger, so the next run skips it |
| **Bug** | The code breaks a contract item, or a new contract test fails on current code. Fixing it changes behavior. | The user, in step 7 and the report |

When docs and code disagree about behavior: when the contract says what should happen, the code is wrong and it is a bug; when the contract is silent and a README, ADR or comment is stale, fixing the doc is a weed; when you cannot tell which is right, it is a question.

When a rule keeps objecting to correct code, that is not a pile of weeds. It is one question: should the rule's scope change?

## Ranking weeds

Sort by spread, then risk, then cost: the weeds most likely to be copied go first, and among those, the ones nearest a contract item.

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
- Over medium: split it into weeds that each fit, or move it to the Question bin, because it needs a plan.

## Repeats

A weed is a repeat when it shows up in two or more places in this run, or the ledger already lists the same drift from an earlier run. A repeat is still pulled as a weed, and step 12 also proposes the check that keeps it from coming back. The second sighting is the signal: one sighting is an accident, two is a habit the repo is teaching.

## The budget

Pull at most five weeds per run unless the user picks another number. Small batches keep every PR easy to review and leave room to learn from how the first ones land. The rest go to the backlog in the ledger, still ranked, so the next run starts from them.
