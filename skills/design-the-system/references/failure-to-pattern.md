# Failure to pattern

Read this in step 9. Start from the failure, never from the pattern. Each row gives the error a pattern rules out and the plainer fix to try first. Admit the pattern only when the plainer fix leaves the error possible.

| Failure the contract names | Pattern that rules it out | Try first |
| --- | --- | --- |
| Duplicate request or message applies twice | Idempotency key, or an outbox with dedupe | A unique constraint in the database |
| Same fact drifts between two places | Single source of truth, derived views | Delete the copy |
| Illegal state transition | State machine with explicit transitions | An enum plus one validating function |
| Invalid data reaches the core | Validate at the boundary into a value object | A parse function at the entry point |
| Partial multi-step write leaves bad state | Transaction, or saga with compensations | Reorder steps so the last one commits |
| Slow or failing dependency drags everything down | Timeout plus circuit breaker, bulkhead | A timeout and a clear error |
| Load spikes overwhelm a component | Queue with backpressure, rate limiter | A bounded worker pool |
| Lost writes on crash | Write-ahead log, outbox | Write before acknowledging |
| Concurrent updates overwrite each other | Optimistic concurrency with versions | A row lock for the one hot path |
| Core logic tangled with I/O, untestable | Functional core, imperative shell; ports and adapters | Pass data in, return data out |
| Variant logic copied across callers | Strategy, registry | One function with a parameter |
| Swapping a dependency in tests is impossible | Dependency injection at the seam | Pass the collaborator as an argument |
| Events reach consumers in the wrong order | Partitioned log keyed by entity, sequence numbers | Process one entity at a time |
| Unsafe action from a learned component | Safety envelope or shield around the policy | A hard bounds check before acting |
| Run cannot be reproduced | Experiment record: config, seed, commit, data version | Log those four values at start |
| One model rendered into several external formats drifts per format | Adapter per format behind one interface | One render function per format |
| Domain logic breaks when the storage changes | Repository at the storage seam | Keep every query in one module |
| Adding a consumer means editing the producer | Observer or event bus | One list of callbacks in the producer |
| Config-dependent construction is copied across call sites | Factory | One constructor function |
| Stages share mutable state, so no stage can be tested alone | Pipeline of pure stages | Functions that take and return data |

## Signs a pattern is being forced

- It names no `FAIL-n`, `NEVER-n` or `INV-n` item.
- The error it prevents cannot happen in this design.
- It has one implementation and no second one planned.
- The plain fix in the right column covers the same error.

Any one of these sends the pattern to "Considered and left out".
