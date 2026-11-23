# Triage

Read this in step 7 to merge duplicates, and in step 9 to rank confirmed and flaky bugs. Severity comes from the contract first; reach and certainty only order bugs inside a level.

## Severity

| Level | The bug | Examples |
| --- | --- | --- |
| S1 | Breaks a `NEVER` or `INV` item | Lost or corrupted data, one user sees another's data, an action takes effect twice, totals that do not add up |
| S2 | Breaks a key `SCN` flow with no workaround, or a `FAIL` response is wrong | Cannot finish sign-up, a dependency outage loses the user's work, a crash on a common path |
| S3 | Breaks a flow that has a workaround, or degrades it | A refresh fixes it, a second try works, a confusing error with a clear way out |
| S4 | Cosmetic, or outside the contract | Layout glitches, typos, a slow screen with no `Q-n` target |

A bug outside the contract can still rank S1 when it is plainly an incident, such as a security hole. Say in its row that the contract should gain the missing line, and offer that edit to the user after the run.

## Order inside a level

1. **Reach**: on a key flow most users take, before an edge only the input breaker found.
2. **Certainty**: confirmed every time, before flaky.
3. **Blast radius**: a fix that may also cover other entries goes first, since step 10 will then skip them.

## Merging duplicates

- Same wrong outcome after the same kind of action: one bug, many paths.
- Same symptom with different causes you can see from the outside (one on save, one on delete): two bugs.
- When unsure, keep them apart. Step 10 re-checks every bug after each fix, so an over-split pair costs one re-check, while an over-merged pair hides a bug.

## The table to show the user

```
| # | Bug | Contract | Severity | Status | Found by |
| 1 | Saving twice creates two invoices | NEVER-2 | S1 | confirmed | Bad connection, Power user |
```

Then ask which to fix. "All confirmed" is the default.
