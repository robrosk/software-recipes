# Hunter personas

Read this in step 5 on Claude Code and Codex. Give each hunter exactly one persona; the ten together cover different surfaces, so two hunters rarely walk the same path. On GitHub Copilot, skip this file: hunters get no persona and the model roster supplies the diversity.

Each persona is a way of using the app, not a character to role-play. Paste its row's three fields into the brief.

| # | Persona | Mindset | Push on |
| --- | --- | --- | --- |
| 1 | Newcomer | First visit, reads labels literally, takes the obvious path, makes the natural mistake | Onboarding, empty states, defaults, wording of errors, what happens after a wrong first click |
| 2 | Power user | Knows the app, moves fast, wants shortcuts | Keyboard shortcuts, bulk actions, deep links, back and forward, rapid repeated actions, large lists |
| 3 | Input breaker | Every field is a test case | Empty, whitespace, very long, unicode, emoji, right-to-left text, leading zeros, negative and huge numbers, dates across time zones and daylight saving, pasted rich text |
| 4 | Boundary tester | Wants what is not theirs, inside the sandbox | Changing ids in URLs, editing hidden or disabled fields, skipping steps of a flow, replaying a request, harmless injection markers such as `<b>x</b>` and `' OR '1'='1` in text fields, using only the hunter's own test accounts |
| 5 | Bad connection | On a train, the network drops and recovers | Slow and offline modes, double submit, refresh or close mid-write, retry after a timeout, what survives a reload |
| 6 | Two places at once | Same account in two tabs or two sessions | Editing the same record twice, deleting in one tab while editing in the other, stale views, last write wins or lost update |
| 7 | Keyboard and screen reader | Never touches the mouse, listens to the page | Tab order, focus traps, visible focus, labels and roles in the accessibility tree, 200 percent zoom, reduced motion |
| 8 | Small screen | On a phone | Narrow viewport, hidden or overlapping controls, long words wrapping, modals that will not close, orientation change |
| 9 | Long haul | Uses it for months | Many records, pagination edges, search with no results and with thousands, session expiry mid-task, undo and history, returning after time passes |
| 10 | Contract auditor | Reads the contract line by line | Walks every `SCN` item literally, then tries to trigger each `NEVER` and `FAIL` item from the outside, and reports any item it could not test |

## Non-browser apps

For a CLI, TUI or API, keep the same ten mindsets and swap the surfaces:

- **Small screen** becomes a narrow terminal, no color support, and output piped to a file.
- **Keyboard and screen reader** becomes `--help` and error text quality, exit codes, and output a script can parse.
- **Bad connection** becomes killing the process mid-write (Ctrl+C), a full disk or a read-only directory, and a dependency that times out.
- **Two places at once** becomes two processes on the same files, lock or database.

The other six carry over as written.
