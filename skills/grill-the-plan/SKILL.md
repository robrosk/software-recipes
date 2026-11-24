---
name: grill-the-plan
description: Interview me about a plan or design one question at a time, each with your recommended answer, until we share one understanding, then hand the decisions to design-the-system for a new or cross-module system, or to plan-the-change for a small change.
disable-model-invocation: true
license: MIT
metadata:
  display-name: Grill The Plan
  short-description: Interview me until the design is clear
---

# Grill the plan

Pressure-test a plan, design or idea by interviewing the user until the two of you hold the same picture of it. The interview walks the design as a tree of decisions, settles the ones others depend on first, and ends with a decision record. A big design takes that record to design-the-system; a small change takes it straight to plan-the-change for slicing.

Be relentless about the decision and easy on the person: every question comes with your recommended answer, so the user can reply "yes" and move on.

## Steps

1. **Load the subject.** Identify what is being grilled: a plan file, a design doc, a pull request, or an idea in the chat. Read the relevant code first, plus `GLOSSARY.md` and `docs/adr/` when they exist. Done when you can state the subject in one sentence and you know which questions the code and the docs already answer.
2. **Build the decision tree.** List every open decision as a node. Put each decision after the decisions it depends on, so the goal and its check come before modules, and modules come before data shapes. Design patterns are not decided here: when one comes up, record it as deferred to design-the-system. Use [references/question-lenses.md](references/question-lenses.md) to find decisions the subject has not raised. Done when every open decision is on the tree with its parents, and you have shown the user the top level in a few lines.
3. **Ask one question.** Take the next unresolved node whose parents are settled. Ask it in one message: the decision, your recommended answer with its one reason, and the alternatives you rejected. Answer it yourself from the code when the code settles it, and tell the user what you found. Then end your turn and wait for the user's reply: do not ask the next question or answer this one yourself. Done when exactly one question is open and you have stopped.
4. **Push until it is concrete.** Accept an answer once it names something checkable: an observable behaviour, a module boundary, a number. Follow a vague answer with one sharper question on the same node. When an answer opens a new decision, add it to the tree. Done when the node is resolved, or the user has deferred it with a reason.
5. **Keep the ledger.** After each resolved node, add one line to a running decision ledger: the decision, the choice, the reason. Show the ledger when the user asks or every five decisions. Done when the ledger holds every resolved and deferred node.
6. **Stop at shared understanding.** End the interview when every node is resolved or deferred, or when the user says stop. Done when no node is open, or the user has ended it.
7. **Hand off by size.** Write the summary below, then route it. A new system, a change that touches several modules, or one with open scale, robustness or pattern questions goes to design-the-system: offer `/design-the-system` and say it will start from this decision record, confirming the settled decisions instead of asking them again. A small single change goes to plan-the-change: Call the Skill tool with "plan-the-change" and give it the summary as the ask. Done when the user has the summary and has chosen the next step.

## Output

```
## Subject
<one sentence>

## Decisions
| Decision | Choice | Reason |

## Deferred
- <decision>: <why, and what would settle it>

## Assumptions
- <what we are relying on without having checked>

## Terms
- <word>: <meaning we agreed>   (glossary candidates)

## ADR candidates
- <decision worth recording, and the forces behind it>
```

## Tone

Ask the way a sharp colleague would at a whiteboard: direct, curious, specific. One question per message, short, with the recommended answer first so the conversation keeps moving.
