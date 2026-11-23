# Ledger

Read this in step 2, to load what earlier runs decided, and in step 13, to record this one. The ledger at `docs/garden/ledger.md` is garden's memory between runs. It is what lets the next run skip correct code it already judged, spot a weed that came back, start from the backlog, and say whether the garden is getting better.

It is committed, so every session and every harness sees the same history. Each run adds a section at the top and leaves earlier sections as they were.

## Grades

Grade each area the run covered against the yardstick. Compare with the last run's grade, so the trend is visible.

- **A**: no weeds, questions or bugs.
- **B**: only weeds with spread 0 or 1.
- **C**: a weed with spread 2 or 3, or a contract item with no test.
- **D**: a bug, an `INV` or `NEVER` item with no test, or drift across a boundary the design doc drew.

The areas are Design (beds 1 to 3, 9), Code (beds 4, 5, 7, 8, 10, 15), Tests (bed 6), Docs (beds 11 and 12), Guardrails (beds 13 and 14), and Runtime (beds 16 to 18). Bed 19 counts toward whichever area its finding falls in.

## Format

```
## <YYYY-MM-DD>: <scope>

Yardstick: <design doc path | docs and rules only>   Base: <commit>

| Area | Grade | Last run |

### Pulled
- <weed>: <bed>, <file>, PR <link> <(repeat)>

### Questions
- <question>: <the decision it needs>

### Bugs
- <bug>: <contract item>

### Leave
- <file or symbol>: <why it is correct>

### Backlog
- <rank>. <weed>: <bed>, <file>, spread <n>, risk <n>, cost <small | medium>
```

A Leave entry holds only while its code is unchanged. When the next run finds the file or symbol changed since that run's base commit, it sweeps it again.
