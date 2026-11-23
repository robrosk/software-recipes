# Contract grill

Read this in step 1 to judge whether the docs state the system's behavior, and in step 2 when they do not. The ids match design-the-system's contract, so a doc from that skill drops straight in and anything grilled here can later feed it.

## When a kind counts as stated

A kind is **stated** when the docs give it in checkable terms a hunter can test against from the outside:

| Kind | Stated when the docs give | Missing when they only give |
| --- | --- | --- |
| `SCN-n` | Each key flow with its starting state, the user's action and the visible result | Feature lists, screenshots, "users can manage X" |
| `INV-n` | Facts that hold at every moment: counts, balances, ownership, ordering, uniqueness | Data models with no rule about what values are legal |
| `NEVER-n` | Outcomes that would be a bug or an incident, and what must never cross a boundary | Security or privacy promises with no concrete case |
| `FAIL-n` | For each dependency and bad input, what the user sees and what state is kept | "Handles errors gracefully" |

Tests count as docs when their names and assertions read as behavior. Code alone does not: what the code does is what the hunters are checking, so it cannot also be the yardstick.

## Interview rules

The same rules as design-the-system, so the user meets one style across the repo:

- One question per message.
- The user answers first. Ask the question open, and give your recommended answer with its one reason only after they answer, or when they ask.
- When the docs or code suggest an answer, say what you found and ask the user to confirm it.
- Push a vague answer once more until it names something a hunter could observe: a screen, a value, a message, a state that survives a reload.

## Questions, by missing kind

Ask only the kinds marked missing, in this order, since later kinds lean on the flows.

**Key scenarios (SCN)**
1. What are the three to five flows that, if broken, would make the app useless? For each: from what state, the user does what, and sees what?
2. What does a brand-new user do first, and what should they end up with?

**Invariants (INV)**
1. What must always be true on every screen or in every response: totals that add up, items that belong to one owner, an order that holds?
2. Which value has exactly one source of truth, so two views must never disagree on it?

**Prohibitions (NEVER)**
1. Which outcome would be an incident: lost work, a double charge or double send, one user seeing another's data, an action taking effect twice?
2. Which state changes are illegal: a step skipped, a closed item edited, a deleted item coming back?

**Failure responses (FAIL)**
1. When each dependency is slow or down, what should the user see, and what of their work must survive?
2. On bad input, a double submit, a refresh mid-action or an expired session, what should happen?

## Writing the items

Write each item on one line with its id and, for grilled items, `(grilled)` in place of a doc source. Stop when each kind has the items the user cares about; three good `SCN` items beat ten vague ones. Show the full list in step 3 with the hunting ground for one sign-off.
