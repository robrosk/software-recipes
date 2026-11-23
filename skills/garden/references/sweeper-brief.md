# Sweeper brief

Read this in step 4 when the scope is too large to sweep in one pass. Fan out to 2 to 4 sweepers; more than that and merging their findings costs more than it saves. For a small scope, sweep alone.

## Splitting the work

- Give each sweeper a disjoint set of beds, not a disjoint set of files. Drift that spans files (duplication, change preventers, naming) only shows up to a sweeper that sees the whole scope.
- Bed 19 goes to every sweeper; you dedupe its findings when you merge.
- Sweepers are read-only: they change no file, run no formatter, open no branch and spawn no subagents. On Claude Code, use a read-only agent (the built-in Explore agent, or one with only Read, Grep and Glob). On Codex and Copilot, say it in the brief and check the working copy is unchanged after they return.

## The brief

Paste this, filled in, as each sweeper's whole prompt. Sweepers may not load `AGENTS.md`, so paste every rule they need.

```
You are sweeping a codebase for drift. You find; you never fix.

Scope: <paths or commit range>
Your beds: <numbers and rows pasted from beds.md, plus bed 19>

Yardstick (pasted verbatim):
<contract items, Architecture table, Patterns table, glossary terms and
repo rules the beds above need>

Skip these, already judged correct in an earlier run:
<Leave entries from the ledger that fall in your beds and scope>

Rules:
- Change no file. Run no command that writes.
- Every finding cites file:line, the yardstick line or rule it drifts
  from, and the evidence. A finding with nothing to point at is taste:
  drop it.
- Report each of your beds, including the ones that are clear.

Report, one block per bed:
Bed <n>: <clear: what you checked | findings below>
- <file:line>: <what drifts> | drifts from: <yardstick line> | evidence: <what you saw>
```

## Merging

Merge findings that name the same place and the same drift into one entry, and keep every place a repeated finding showed up, because step 6 counts places to mark repeats. Done when every sweeper has returned and every bed has its line.
