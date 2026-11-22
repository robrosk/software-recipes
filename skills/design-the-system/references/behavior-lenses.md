# Behavior lenses

Read this in step 2. Each lens is a family of questions; ask the ones that fit the system, one at a time.

## Invariants (INV)
- What must be true at every moment the system runs? Think of balances, counts, ownership, ordering, uniqueness.
- Which facts have exactly one source of truth?
- What does a reader of the system's state always get to assume?

## Prohibitions (NEVER)
- What outcome would be a serious bug or an incident? Double charges, lost writes, a trade placed twice, a robot moving while stopped.
- What must never cross a boundary: secrets, personal data, unvalidated input?
- Which state transitions are illegal?

## Key scenarios (SCN)
- What are the three to five flows that define the system? Write each as given, when, then.
- What does the first user do on day one?
- Which scenario, if it broke, would make the rest not matter?

## Failure modes (FAIL)
- For each external dependency: what happens when it is slow, down, or returns garbage?
- What happens on a retry, a duplicate message, an out-of-order message, or a restart halfway through?
- What happens under partial failure: one replica, one partition, one step of a multi-step write?
- Which failures should be loud, and which should degrade quietly?

## Concurrency and time
- Can two actors change the same thing at once? Who wins, and is that acceptable?
- Which operations must be idempotent?
- Where do clocks, timeouts and deadlines matter?

## Quality targets (Q)
- Latency, throughput and availability: what numbers, at what percentile, at what load?
- Data size now and in a year.
- Cost per request, run or day.
- Recovery: how much data can be lost, and how fast must it come back?

## Learning and control systems
- What must the policy or model never output, and what catches it if it does?
- Which safety envelope holds regardless of the learned component?
- How is a run reproduced: seeds, configs, data versions, commit?
- How do we detect drift between training and the live environment?
