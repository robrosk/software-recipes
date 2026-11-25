# Sweeper brief

Read this in steps 4 and 5. Every sweeper sweeps every bed across the whole scope, on its own. Overlap is the point: each model sees the same garden and misses different things, so the merged list covers more than any one of them would.

## Lenses

Give each sweeper one lens, all distinct. A lens is only where the sweeper starts and which way it walks; every sweeper still covers all 19 beds. Hand them out in this order, the first to the strongest model:

| # | Lens | Start from | Walk toward |
| --- | --- | --- | --- |
| 1 | Contract first | Each `INV`, `NEVER`, `SCN` and `FAIL` item | The code and test that should guarantee it |
| 2 | Code first | Each module in the scope | The yardstick line it should follow |
| 3 | Copy first | The files new code imitates: templates, base classes, examples, the most imported and the most recently copied modules | Every place their patterns were copied to |
| 4 | Docs first | README, ADRs, the design doc, `AGENTS.md`, `CLAUDE.md` and skill files | The code each claim describes |
| 5 | History first | The most recent commits in the scope, newest first | What each one left half done or out of step with the docs |

With more sweepers than lenses, start again from lens 1. With fewer, use the first ones.

## The brief

Paste this, filled in, as each sweeper's whole prompt. Sweepers may not load `AGENTS.md`, so paste every rule they need.

```
You are sweeping a codebase for drift from its docs. You find; you never fix.

Scope: <paths or commit range>
Your lens: <name, where to start and which way to walk, pasted from the
table>
Beds: <all 19 rows pasted from beds.md>

Yardstick (pasted verbatim):
<contract items, Architecture table, Patterns table, glossary terms and
repo rules>

Skip these, already judged correct in an earlier run:
<Leave entries from the ledger that fall in the scope>

Rules:
- Change no file. Run no command that writes. Spawn no subagents.
- Every find cites file:line, the yardstick line or rule it drifts from,
  and the evidence. A find with nothing to point at is taste: drop it.
- Code that does what a contract item forbids, or fails to do what it
  promises, is a find too: cite the item.
- Report every bed, including the ones that are clear.

Report, one block per bed:
Bed <n>: <clear: what you checked | finds below>
- <file:line>: <what drifts> | drifts from: <yardstick line> | evidence: <what you saw>
```

## Merging

Step 6 merges the reports. Two finds are one entry when they name the same place and the same drift, even when the sweepers worded them differently; keep every place a repeated find showed up, because step 8 counts places to mark repeats, and list every sweeper that raised it in the Found by column. Done when every sweeper has returned and every bed has its line from each one.
