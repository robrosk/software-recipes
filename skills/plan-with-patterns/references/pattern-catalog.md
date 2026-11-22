# Pattern catalog

Reach for a pattern only when its force is present. Each entry: the force that earns it, and the smell that says it is unearned.

| Pattern | Force that earns it | Unearned when |
| --- | --- | --- |
| Single source of truth | The same fact would otherwise live in two files and drift | Only one consumer reads it |
| Adapter | One core model must be rendered into several external formats | There is only one format |
| Strategy | Several interchangeable algorithms are chosen at runtime or by config | The choice never changes |
| Registry | New variants are added often and callers should not change | Two variants, fixed forever |
| Pipeline | Work is a fixed sequence of pure stages (load, validate, render, emit) | Stages share mutable state |
| Repository | Domain code must not know where data is stored | Storage is one in-memory dict |
| Factory | Construction is complex or depends on config | A constructor call is clear |
| Observer / event bus | Producers must not know their consumers | One caller, one callee |
| Value object | A small immutable record is compared by value | It carries behaviour and identity |
| Functional core, imperative shell | Logic should be testable without I/O | The whole module is I/O |
| Dependency injection | A collaborator must be swapped in tests | It is never swapped |

## Composition notes

- Adapter plus registry is the usual shape for "one model, many targets".
- A pipeline of pure stages is the easiest thing to test: feed the stage, assert the output.
- Prefer a plain function over any pattern when the function fits on one screen.
