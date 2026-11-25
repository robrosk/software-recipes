# Beds

Read this in step 5, and paste every row into each sweeper's brief. Each bed is a question with signals you can point at, so the sweep finds something checkable instead of judging "quality". Sweep every bed and mark each one with findings or "clear" plus one line on what you checked. A bed you skip quietly is a bed nobody gardens.

The "Usual bin" column is a starting guess for triage, not a verdict.

| # | Bed | Question | Signals | Usual bin |
| --- | --- | --- | --- | --- |
| 1 | Design drift | Does the code still follow the design doc? | Code that bypasses a pattern the doc chose; imports across a boundary the doc drew (between layers, processes or components); a component doing another's job; a contract id no component still guarantees. | Question, or weed when the doc is clear and the fix is local |
| 2 | Patterns that stopped earning their place | Does each pattern still rule out the failure it was admitted for? | An interface with one implementation, a factory with one product, a strategy with one strategy, a pattern whose "error it rules out" no longer exists. | Weed when the doc did not choose it; question when it did |
| 3 | Copyable weeds | Is there anything here new code would copy that the design does not want copied? | Two ways to do the same thing; a half-finished migration; a one-off hack in a template, base class, example or the most recently copied module. | Weed, ranked high |
| 4 | Duplication | Is anything written twice? | Hand-rolled helpers a shared utility already covers; copy-pasted blocks that have started to diverge; the same constant, regex or schema defined twice. | Weed |
| 5 | Dead and dormant code | Is anything unused? | Unused exports, files and parameters; unreachable branches; feature flags stuck fully on or off; commented-out code. | Weed |
| 6 | Contract coverage | Does every contract item have a test that would fail if it broke? | `INV`, `NEVER`, `SCN` or `FAIL` items with no test; tests that assert nothing or only snapshot output; skipped or quarantined tests; tests that stay green while the old code path is still called; code that plainly does what an item forbids. | Weed (add the test); bug when the new test fails or the code breaks the item |
| 7 | Boundaries and errors | Is input checked where it enters, and are errors handled the same way? | Input used without validation at a boundary; swallowed exceptions and broad catches; checks for states the types already rule out; sibling modules with different error types. | Weed, or question when the fix changes what callers see |
| 8 | Types and data shapes | Do the types say what the data is? | Casts and `any` hiding a real type; strings standing in for enums; the same group of fields passed around together; primitives standing in for a domain type. | Weed |
| 9 | Change preventers | Does one change stay in one place? | One change that has to touch many files; one file that changes for many reasons; a function more interested in another module's data; long call chains; a class that only forwards. | Question when the fix moves a boundary; weed when it is local |
| 10 | Naming and language | Do names match the glossary and what the thing does? | Names that drift from `GLOSSARY.md`; one concept with two names; a name that no longer says what the thing does. | Weed when the glossary settles it; question otherwise |
| 11 | Docs drift | Do the docs describe the code as it is? | README, ADRs or design doc describing behavior the code no longer has; stale examples and commands; broken links; comments that lie or narrate history. | Weed (fix the doc); bug when the contract says the code is wrong; question when the design itself is in doubt |
| 12 | Agent-facing instructions | Do the instructions agents read match the code? | `AGENTS.md`, `CLAUDE.md` or skill files that contradict the code, repeat each other, or state a rule a lint rule could enforce instead. | Weed; a rule a machine could enforce goes to step 13 |
| 13 | Guardrails | Are the checks still checking? | Lint suppressions, `noqa`, `type: ignore` or `eslint-disable` piling up; rules that keep objecting to correct code; warnings never promoted to errors; CI steps that check nothing. | Weed, or question when a rule should change |
| 14 | Dependencies and toolchain | Is every dependency used and current? | Unused packages; two packages doing one job; deprecated APIs still called; lockfiles or generated files out of date. | Weed when removal changes nothing; question for any upgrade |
| 15 | Config | Is every setting read, and read the same way? | Environment variables and config keys nothing reads; defaults that disagree between files; settings duplicated across environments. | Weed |
| 16 | Performance cliffs | Does anything scale worse than its `Q` target allows? | Queries in a loop; unbounded collections or retries; accidental quadratic work; missing pagination; blocking I/O on a hot path. | Question, because the fix can change timing |
| 17 | Observability | Can each failure path be seen? | `FAIL` items whose path logs nothing; logs without the ids needed to trace a request; metrics nothing reads. | Weed when it only adds a log line; question otherwise |
| 18 | Security hygiene | Is anything exposed that should not be? | Secrets or tokens in the repo; permissive defaults; debug endpoints left on. | Always a question; never a silent PR |
| 19 | Anything else | What in this code would a new contributor or agent copy that the design would not want copied? | Anything the beds above missed that passes this one question. | Weed or question |

Bed 19 is the escape hatch. It widens the search past the list but stays tied to one question, the copy test, so it never becomes "anything I would have written differently".

## Without a design doc

When step 2 found no design doc, beds 1 and 2 have no Architecture or Patterns table to measure against. Sweep them against the ADRs, `AGENTS.md` and the module layout the repo plainly follows, mark both beds **limited**, and keep their findings in the Question bin unless an ADR settles them.
