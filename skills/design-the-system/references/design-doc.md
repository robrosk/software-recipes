# Design doc template

Read this in part 10, when you write the doc for review, and not before: the doc is assembled from the working file's Decided section, so nothing in it is drafted ahead of the interview.

```
# <System> design

## Scale and robustness
| Dimension | Now | In a year | Source |
Rung: <name> because <reason>

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

## Change log
- <date>, <PR>: <what changed in the design and why>
```
