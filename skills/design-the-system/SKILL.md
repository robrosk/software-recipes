---
name: design-the-system
description: Design a system with me in three passes: grill its required behavior into a signed contract, design scalable components against that contract, then admit a design pattern only where it rules out a named failure.
disable-model-invocation: true
license: MIT
metadata:
  display-name: Design The System
  short-description: Behavior contract, then design, then patterns
---

# Design the system

Two things have to hold at once: the system underneath scales, and its behavior is exactly what we planned. This skill gets there in three passes and ends with one design doc.

1. **Grill the behavior** into a contract: what the system always does, never does, and how it fails.
2. **Design together**: components, boundaries, data flow and a scaling path, each checked against the contract.
3. **Patterns on trial**: a design pattern goes in only when it rules out a failure mode the contract names. "No pattern here" is a normal, good answer.

## Interview rules

Every question in this skill follows the same shape: one question per message, your recommended answer with its one reason, and the alternatives you rejected. Answer from the code or docs yourself when they settle it, and say what you found. Push a vague answer once more until it names something checkable: a behavior, a number, a boundary.

## Pass 1: behavior contract

1. **Load the system.** Read the relevant code, `GLOSSARY.md` and `docs/adr/` when they exist. Name the system in one sentence, its actors (users, services, schedulers), and its external dependencies. Done when the user agrees with that sentence and the lists.
2. **Grill the behavior.** Interview through the lenses in [references/behavior-lenses.md](references/behavior-lenses.md): invariants, prohibitions, key scenarios, failure modes and quality targets. Settle what the system must do before how it does it. Done when every lens that applies is resolved or deferred with a reason.
3. **Sign the contract.** Write each item with an id: `INV-n` (always true), `NEVER-n` (must not happen), `SCN-n` (given, when, then), `FAIL-n` (dependency or input fails, system responds), `Q-n` (a quality target with a number). Ask the user to sign off or change items. Done when the user has signed off on the contract.

## Pass 2: design together

4. **Propose components.** For each component give its responsibility, its interface, the state it owns, and the contract ids it guarantees. Draw the data flow between them. Offer the design and one alternative where a real choice exists, with your pick. Done when every contract item has an owning component and every component guarantees at least one item.
5. **Scale each part.** For each component name the load it grows with, what breaks first, and the step that relieves it (stateless replicas, partitioning, a queue, a cache, batching). Size to the `Q-n` targets; "one instance meets the target" is a complete answer. Done when every component has a scaling line tied to a `Q-n` target.
6. **Walk the failures.** Trace each `FAIL-n` and `NEVER-n` item through the design step by step, and mark it covered or a gap. Done when every item is marked, and each gap names the component where it opens.

## Pass 3: patterns on trial

7. **Try each candidate pattern.** For each gap and each error-prone spot, look up the failure in [references/failure-to-pattern.md](references/failure-to-pattern.md). Admit a pattern only when you can name the contract item it protects, the specific error it rules out, and why a plain function plus a test would not rule it out as well. Done when every admitted pattern has those three answers and every rejected candidate has a one-line reason.
8. **Review the doc.** Show the user the design doc below and revise until they approve. Done when the user approves the doc.
9. **Save and hand off.** Save the doc to `docs/design/<system-name>.md`, or where the user asks. Offer two next steps: slice the build by calling the Skill tool with "plan-with-patterns" and giving it the doc, and turn the `INV-n`, `NEVER-n` and `SCN-n` items into property and scenario tests. Done when the doc is saved and the user has picked the next step.

## Output

```
# <System> design

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
