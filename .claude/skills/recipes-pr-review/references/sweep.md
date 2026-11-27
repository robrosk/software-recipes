# Reference sweep

Read this in step 4. A skill's steps, done lines, report template and reference files all describe the same run, so a change to one has to show up in the others.

## What to search for

For each changed thing, search `skills/<name>/` and any skill that calls it (`grep -rn "Call the Skill tool with \"<name>\"" skills`):

| Changed thing | Search for |
| --- | --- |
| A new mode or option | The list of the old ones (for example `wait` and `stacked`), and every step whose done line assumes one of them |
| A new or moved step | `step <n>` in every reference file, and the "Run steps a to b" ranges in SKILL.md |
| A new artifact (a PR, a branch, a file) | Every step that creates, gates, hands over or merges that kind of artifact |
| A new check in a numbered list | The "Done when all <n> hold" line, and the summary of the list in SKILL.md |
| A new mode that a step hands to another skill (`/garden`, `/break-it`) | That skill's own step where it finds its base, branch or target, since it does not see the caller's mode unless the step passes it |
| A new report field or section | The Output template, and the done line that says what the report must contain |

## How to judge a hit

Read the step, not just the line. Ask: if an agent picks the new mode or option, can it meet this step's done line? If not, that step needs a line for the new case.

Example from #11: single-branch mode was added to step 5 and the report's `Mode:` line, but step 13 still ended "when every PR in the wave is merged" and step 14 still checked the base branch. In single-branch there is no per-slice PR and the code sits on the feature branch, so the run could never finish step 13.


The same PR's second round fixed steps 13 to 15 but left step 14's garden pass on main: `/garden` finds its base on its own, so the feature branch has to be passed to it.
