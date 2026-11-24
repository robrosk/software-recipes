---
name: design-the-system
description: "Design a system together, with you leading: pin down its behavior, scale and robustness into a signed contract, draft the design yourself while I probe and stress-test it, then admit a design pattern only where it rules out a named failure."
disable-model-invocation: true
license: MIT
metadata:
  display-name: Design The System
  short-description: Behavior contract, your design, patterns on trial
---

# Design the system

Two things have to hold at once: the system underneath scales as far as it needs to, and its behavior is exactly what we planned. This skill gets there as an interview of 11 parts in three passes, and only at the end writes one design doc.

1. **Contract** (parts 1 to 5): what the system always does, never does, how it fails, and how big and how robust it has to be.
2. **The user's design** (parts 6 to 8): the user drafts components, boundaries and data flow; the agent probes, stress-tests and suggests against the contract.
3. **Patterns on trial** (parts 9 to 11): a design pattern goes in only when it rules out a failure the contract names. "No pattern here" is a normal, good answer.

## Turn protocol

This is an interview, not a report. Every part depends on the user's answers to the parts before it, so the agent cannot do a later part ahead of time without inventing those answers. Each turn follows the same loop:

1. **Work silently.** Read code, docs or the user's last answer as the current part needs. Write nothing for later parts.
2. **Show where you are.** Start the message with one progress line: `Part 3 of 11: size the system (question 2 of 9)`.
3. **Ask one question.** Ask only the current part's next question. Name no later part's questions.
4. **Stop.** End your turn here and wait for the user's reply. If your harness has a tool for asking the user, ask through it; otherwise end the message on the question. Do not answer the question yourself, do not draft later parts, and do not write the design doc.

Move to the next part only when the user's own reply says this part is done: they answered its last question, confirmed it, or said to skip or defer it. Silence, your own recommendation, or a guess about what they would say never closes a part. When the user says "your call", give your recommendation, record it as theirs only after they accept it, and stop again.

The design doc is written once, in part 10, from the answers already given. Its template lives in [references/design-doc.md](references/design-doc.md); do not open it before part 10.

## Interview rules

The user leads; the agent sharpens. Every question follows the same shape:

- One question per message, then stop, as the turn protocol says.
- The user answers first. Ask the question open, and give your recommended answer with its one reason only after they answer, or when they ask for it.
- When the code or docs settle a question, say what you found and ask the user to confirm. That is still the turn's one question.
- Push a vague answer once more until it names something checkable: a behavior, a number, a boundary.
- When the user brings a decision record from grill-the-plan, its decisions are already settled. State each one where it falls and ask the user to confirm or change it; interview only on what the record leaves open or deferred.

## Pass 1: contract

1. **Load the system.** Read the relevant code, `GLOSSARY.md` and `docs/adr/` when they exist, and the grill-the-plan decision record when the user brings one. When the code or docs show what the system is, state the one-sentence description, its actors (users, services, schedulers) and its external dependencies as you found them, and ask the user to confirm or correct them. Otherwise ask for the sentence first, then the actors, then the dependencies, one per turn. Done when the user has agreed to the sentence and both lists.
2. **Collect the user's questions.** Ask the user which questions they think this design has to answer, and stop. After they reply, show the interview order: their questions at the top, then the lenses from [references/behavior-lenses.md](references/behavior-lenses.md) that their list leaves out, and ask whether the order is right. Done when the user has given their list and agreed to the order.
3. **Size the system.** Ask the sizing questions in [references/robustness-ladder.md](references/robustness-ladder.md), one per turn, in the order listed there: users now and in a year, peak against average load, read and write mix, data volume and growth, latency, downtime tolerance, data-loss tolerance, consistency, and the response when a dependency fails. Count them in the progress line. After the last answer, propose a rung on the robustness ladder with its reason and ask the user to agree, so a small internal tool is designed like one and a global service like one. Done when every sizing question has a number or a deferral with a reason from the user, and the user has agreed to a rung.
4. **Grill the behavior.** Work through the agreed interview order one question per turn: invariants, prohibitions, key scenarios and failure modes. Settle what the system must do before how it does it. Done when every question on the list is resolved or deferred with a reason.
5. **Sign the contract.** Write each settled answer as an item with an id: `INV-n` (always true), `NEVER-n` (must not happen), `SCN-n` (given, when, then), `FAIL-n` (dependency or input fails, system responds), `Q-n` (a scale or robustness target with a number). Show only the contract and ask the user to sign off or change items. Done when the user has signed off on the contract.

## Pass 2: the user's design

6. **The user drafts.** Ask the user to sketch the components, their boundaries and the data flow, in any form: a list, boxes and arrows, prose. Then stop: offer no design of your own, even a partial one, until their draft is on the page. Done when the user's draft is on the page.
7. **Map the draft to the contract.** For each component, write its responsibility, interface, owned state and the contract ids it guarantees, using the user's names. List every contract item with no owner and every component that guarantees nothing, then ask how to close the first one; take the rest one per turn. Done when every item has an owner and every component guarantees at least one item, by the user's choices.
8. **Stress-test it.** Probe the draft one question per turn: trace each `FAIL-n` and `NEVER-n` item through it, and ask how each component handles its `Q-n` load and what breaks first. When the user is stuck or asks, offer a suggestion with its reason and one alternative. Done when every `FAIL-n` and `NEVER-n` item is marked covered or a gap, and every component has a scaling line tied to a `Q-n` target, sized to the agreed rung.

## Pass 3: patterns on trial

9. **Try each candidate pattern.** For each gap and each error-prone spot, look up the failure in [references/failure-to-pattern.md](references/failure-to-pattern.md). Take one candidate per turn: ask the user which pattern, if any, they would reach for, then put it on trial. Admit it only when it names the contract item it protects, the specific error it rules out, and why a plain function plus a test would not rule it out as well. Done when every admitted pattern has those three answers and every rejected candidate has a one-line reason.
10. **Review the doc.** Now open [references/design-doc.md](references/design-doc.md) and fill it from the answers given in parts 1 to 9, adding nothing the user did not settle. Show it and ask the user to approve or change it; revise until they approve. Done when the user approves the doc.
11. **Save and hand off.** Save the doc to `docs/design/<system-name>.md`, or where the user asks. Offer the next steps: slice the build by calling the Skill tool with "plan-the-change" and giving it the doc, which it slices without changing the Patterns table; for a system too large for one change, run `/orchestrate-prs` with the saved doc to build it as waves of subagent PRs (it requires this doc and will not start without it); and turn the `INV-n`, `NEVER-n` and `SCN-n` items into property and scenario tests. Ask which one they want. Done when the doc is saved and the user has picked the next step.
