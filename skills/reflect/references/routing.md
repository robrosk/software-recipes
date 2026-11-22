# Routing lessons

Read this in step 3 to place a lesson in an exact file and section.

## In this repo (software-recipes)

| Lesson is about | Target |
| --- | --- |
| A step that was missing, out of order, or unclear | `skills/<name>/SKILL.md`, that step |
| A step that ended too early or too late | `skills/<name>/SKILL.md`, that step's "Done when" |
| A skill that fired when it should not, or stayed quiet when it should fire | `skills/<name>/SKILL.md` description, plus a prompt in `evals/triggers.json` |
| Reference that only some runs need | `skills/<name>/references/<topic>.md`, linked from the step that needs it |
| A rule about skill files that a script can check | a new function in `tools/recipes/rules.py`, added to `RULES`, with a test in `tests/` |
| A recurring workflow with no skill yet | `drafts/<name>/SKILL.md` |
| A repo-wide authoring rule a machine cannot check | `AGENTS.md`, Writing a skill |
| A term the user and agent defined | `GLOSSARY.md` |
| A design decision with forces behind it | `docs/adr/NNNN-<title>.md` |

## In another project

Skill lessons still belong in software-recipes, since that is where the skills live: write the edit against this repo and tell the user it lands there. Project lessons go in that project's own `AGENTS.md`, `CLAUDE.md`, glossary or ADRs.

## Telling a rule from a note

Prefer a rule when the mistake has a mechanical signature: a pattern in text, a missing file, a field out of range. Prefer a note when catching it takes judgement. A rule that would fire on correct work more than rarely is a note.

## Keeping skills lean

When a lesson would push a `SKILL.md` past what every run needs, put the detail in `references/` and add one pointer in the step. When two lessons say the same thing, merge them into one edit.
