---
name: reflect
description: End a session by turning each lesson into a proposed edit to the skill it improves, a lint rule or script, or a note, applied only once you accept it.
disable-model-invocation: true
license: MIT
metadata:
  display-name: Reflect
  short-description: Turn session lessons into skill edits
---

# Reflect

Close the learning loop. Each lesson from this session becomes a small, reviewable edit in the place that will change future behaviour, so the skills get sharper from how the user actually works.

Route each lesson to the first home that fits, in this order:

1. **The skill it improves.** A step, a completion criterion, or a reference file in the skill that was running when the lesson happened.
2. **A lint rule or script.** A check in `tools/recipes/rules.py`, a test, or a script, when a machine can catch the mistake every time.
3. **A note.** A line in `AGENTS.md`, `GLOSSARY.md`, or a new ADR in `docs/adr/`, when the lesson is project context rather than a procedure.

Propose every edit and apply only the ones the user accepts.

## Steps

1. **Collect lessons.** Scan the session for user corrections, retries and failed attempts, surprises, and approaches the user confirmed worked. Write each as one line with its evidence: a quoted correction or the event that showed it. Done when every lesson has evidence, or you have told the user the session held none and stopped.
2. **Keep the ones that recur.** Keep a lesson when it would change what an agent does next time on a similar task. Rewrite each kept lesson as "Next time, <behaviour>." Done when every kept lesson is a "Next time" line and each dropped one has a one-word reason (one-off, already covered, unclear).
3. **Route each lesson.** Pick the first home from the list above that fits. Read [references/routing.md](references/routing.md) to find the exact file and section. A lesson about a workflow no skill covers yet becomes a skill draft in `drafts/<name>/`. Done when every lesson names one target file and the reason that home beats the one above it.
4. **Draft the smallest edit.** Write each edit as a diff against the current file. Follow `AGENTS.md`: positive phrasing, steps that end on a completion criterion, no em dashes, `SKILL.md` kept to steps every run needs. Done when every routed lesson has a diff that applies cleanly.
5. **Propose.** Show the user the table below and ask them to accept, change or reject each row. Done when every row has the user's decision.
6. **Apply and verify.** Apply the accepted edits only. Run `make check` in this repo, or the project's own check elsewhere. Then Call the Skill tool with "surgical-diff-review" on the applied edits, with the accepted rows as the ask. Done when the check passes, the review verdict is clean, and you have listed what changed.

## Output

```
## Lessons
| # | Next time | Evidence | Home | Target |

## Proposed edits
### 1. <target file>
<diff>

## Dropped
- <lesson>: <reason>
```
