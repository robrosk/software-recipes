# Question lenses

Read this in step 2 to find decisions the subject has not raised yet. Each lens is a family of questions. Use the ones that fit the subject; a small change may need three lenses, a new system all of them.

## Goal and check
- What observable result tells us this worked? What command, test or number changes?
- Who uses it first, and what do they do with it on day one?
- What is the smallest version that still proves the idea?

## Scope and cut
- What is explicitly out of scope for now?
- Which part would we drop first if time halved?

## Modules and interfaces
- Which modules change or appear, and what is each one's single responsibility?
- What is the public interface of each, and what stays hidden behind it?
- Where are the seams: the places we swap an implementation, inject a fake, or test in isolation?

## Patterns
- Does any part seem to need a design pattern? Do not settle it here: defer it to design-the-system, which admits a pattern only against a named failure, and route the hand-off there.

## Data and state
- What data flows through, in what shape, and who owns each piece?
- Where does state live, and what is immutable?
- What is the single source of truth for each fact?

## Behaviour and invariants
- What must always be true while the system runs?
- What happens on the unhappy paths: bad input, timeouts, partial failure, retries?
- Which behaviours are guaranteed, and which are best effort?

## Scale and cost
- What load, size or rate does this need to handle now, and in a year?
- What is the cost per run, request or experiment?

## Verification
- Which tests prove each behaviour, and at which seam?
- How do we know a regression happened?

## Research and ML work
- What is the metric, the baseline, and the result that would change our mind?
- How are seeds, configs and data versions recorded so a run can be reproduced?
- Where could data leak between train and evaluation?

## Readability and naming
- What do we call each new concept, and does the project already have a word for it?
- Could a new reader find the entry point and follow the flow in one pass?

## Reversibility
- Which decisions are cheap to change later, and which lock us in?
- What would we write in an ADR so the next person knows why?
