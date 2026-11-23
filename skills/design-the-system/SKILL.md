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

Two things have to hold at once: the system underneath scales as far as it needs to, and its behavior is exactly what we planned. This skill gets there in three passes and ends with one design doc.

1. **Contract**: what the system always does, never does, how it fails, and how big and how robust it has to be.
2. **The user's design**: the user drafts components, boundaries and data flow; the agent probes, stress-tests and suggests against the contract.
3. **Patterns on trial**: a design pattern goes in only when it rules out a failure the contract names. "No pattern here" is a normal, good answer.

## Interview rules

The user leads; the agent sharpens. Every question follows the same shape:

- One question per message.
- The user answers first. Ask the question open, and give your recommended answer with its one reason only after they answer, or when they ask for it.
- When the code or docs settle a question, say what you found and ask the user to confirm.
- Push a vague answer once more until it names something checkable: a behavior, a number, a boundary.
- When the user brings a decision record from grill-the-plan, its decisions are already settled. State each one where it falls and ask the user to confirm or change it; interview only on what the record leaves open or deferred.

## Pass 1: contract

1. **Load the system.** Read the relevant code, `GLOSSARY.md` and `docs/adr/` when they exist, and the grill-the-plan decision record when the user brings one. Ask the user to describe the system in a sentence, its actors (users, services, schedulers) and its external dependencies, then fill gaps from what you read. Done when the user agrees with the sentence and the lists.
2. **Collect the user's questions.** Ask the user which questions they think this design has to answer. Put theirs at the top of the interview, then add the lenses from [references/behavior-lenses.md](references/behavior-lenses.md) that their list leaves out. Done when the user has given their list and seen the full interview order.
3. **Size the system.** Grill scale and robustness: users now and in a year, peak against average load, read and write mix, data volume and growth, latency targets, availability and downtime tolerance, durability and data-loss tolerance, consistency needs, and the response when a dependency fails. Then place the system on the robustness ladder in [references/robustness-ladder.md](references/robustness-ladder.md), so a small internal tool is designed like one and a global service like one. Done when every sizing question has a number or a deferral with a reason, and the user has agreed to a rung.
4. **Grill the behavior.** Work through the user's questions and the remaining lenses: invariants, prohibitions, key scenarios and failure modes. Settle what the system must do before how it does it. Done when every question on the list is resolved or deferred with a reason.
5. **Sign the contract.** Write each item with an id: `INV-n` (always true), `NEVER-n` (must not happen), `SCN-n` (given, when, then), `FAIL-n` (dependency or input fails, system responds), `Q-n` (a scale or robustness target with a number). Ask the user to sign off or change items. Done when the user has signed off on the contract.

## Pass 2: the user's design

6. **The user drafts.** Ask the user to sketch the components, their boundaries and the data flow, in any form: a list, boxes and arrows, prose. Wait for their draft before offering any design of your own. Done when the user's draft is on the page.
7. **Map the draft to the contract.** For each component, write its responsibility, interface, owned state and the contract ids it guarantees, using the user's names. List every contract item with no owner and every component that guarantees nothing, and ask the user how to close each one. Done when every item has an owner and every component guarantees at least one item, by the user's choices.
8. **Stress-test it.** Probe the draft one question at a time: trace each `FAIL-n` and `NEVER-n` item through it, and ask how each component handles its `Q-n` load and what breaks first. When the user is stuck or asks, offer a suggestion with its reason and one alternative. Done when every `FAIL-n` and `NEVER-n` item is marked covered or a gap, and every component has a scaling line tied to a `Q-n` target, sized to the agreed rung.

## Pass 3: patterns on trial

9. **Try each candidate pattern.** For each gap and each error-prone spot, look up the failure in [references/failure-to-pattern.md](references/failure-to-pattern.md). Ask the user which pattern, if any, they would reach for, then put it on trial: admit it only when it names the contract item it protects, the specific error it rules out, and why a plain function plus a test would not rule it out as well. Done when every admitted pattern has those three answers and every rejected candidate has a one-line reason.
10. **Review the doc.** Show the user the design doc below and revise until they approve. Done when the user approves the doc.
11. **Save and hand off.** Save the doc to `docs/design/<system-name>.md`, or where the user asks. Offer the next steps: slice the build by calling the Skill tool with "plan-the-change" and giving it the doc, which it slices without changing the Patterns table; for a system too large for one change, run `/orchestrate-prs` with the doc to build it as waves of subagent PRs; and turn the `INV-n`, `NEVER-n` and `SCN-n` items into property and scenario tests. Done when the doc is saved and the user has picked the next step.

## Output

```
# <System> design

## Scale and robustness
| Dimension | Now | In a year | Source |
Rung: <name> because <reason>

## Behavior contract
- INV-1: <always true>
- NEVER-1: <must not happen>
- SCN-1: Given <state>, when <event>, then <result>
- FAIL-1: When <dependency or input fails>, the system <responds>
- Q-1: <metric> <target>

## Architecture
| Component | Responsibility | Interface | Owns state | Guarantees |

<data flow, a short diagram or numbered steps>

## Scaling
| Component | Grows with | Breaks first | Relief | Target |

## Failure walk
| Item | Path through the design | Covered or gap |

## Patterns
| Pattern | Where | Error it rules out | Protects | Why not plain code |

## Considered and left out
- <pattern or option>: <reason>

## Deferred
- <question>: <what would settle it>
```
