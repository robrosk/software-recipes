# Instruction shape

Read this from the step "Check each new instruction can run" in [SKILL.md](../SKILL.md). An instruction an agent cannot place is skipped or improvised.

## Three questions for every new instruction

1. **Who does it?** The orchestrator, a subagent, a hunter, the user. Check it against what the skill already says that actor may do. A rule that asks hunters to scope triggers, in a skill where hunters change no code, has no actor.
2. **When?** Name the step. A paragraph in a reference file that no step points at is never read at the right time.
3. **How is it done?** `AGENTS.md` asks every step to end on a completion criterion the agent can check. A new paragraph that stands beside others with "Done when" lines needs one too.

## Finds need a destination

A check that can find something must say what happens to the find: fix it where, re-run which step, and where it lands in the report. For example, a new step that reviews across several fix PRs must say which PR a follow-up fix goes on, and the report needs a section that lists it.

## Match the shape of the neighbors

Items in a numbered list of checks are conditions that hold ("file sets are disjoint"), so a new item written as a procedure ("inspect the composition root, then assign") reads wrong against "Done when all five hold". Rewrite it as a condition, with the procedure after it if needed.

## Platform words

A rule named after one stack (`Program.cs`) should name the general thing first (the composition root) so it still fires on Python, TypeScript or Go projects.
