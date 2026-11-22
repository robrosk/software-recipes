# Robustness ladder

Read this in step 3. The rung sets how much machinery the design earns. Pick the lowest rung whose targets cover the answers from the sizing questions; climb only when a number demands it.

| Rung | Typical shape | Users and load | Downtime tolerated | Data loss tolerated | What the design usually needs |
| --- | --- | --- | --- | --- | --- |
| 1. Personal or prototype | A script, a notebook, one process | One to a few people, bursty | Hours | Rerun it | One process, local files or SQLite, logs |
| 2. Internal tool | A small service for a team | Tens to hundreds, office hours | Minutes to an hour | Last backup, daily | One instance, managed database, backups, health check |
| 3. Product | A public app or API | Thousands to hundreds of thousands, daily peaks | Minutes per month | Seconds to minutes | Stateless replicas behind a load balancer, managed database with replicas, queues for slow work, monitoring and alerts |
| 4. Critical or large | Money, safety, or millions of users | Millions, sustained peaks | Seconds per month | None for committed writes | Multiple zones or regions, partitioned data, idempotent writes, circuit breakers, load shedding, tested failover |

## Sizing questions in order

1. How many people or clients use it now, and in a year?
2. What is the peak load against the average, and when does the peak hit?
3. What share of requests read, and what share write?
4. How much data now, and how fast does it grow?
5. What latency is acceptable, at what percentile?
6. How long can it be down before someone is hurt or loses money?
7. How much committed data can be lost in a failure?
8. Must every reader see the latest write, or is a short delay fine?
9. When each dependency fails, should the system stop, degrade, or queue?

## Reading the answers

- Each answer becomes a `Q-n` item with a number.
- When answers point at different rungs, the highest one sets the rung for that part only. A rung 2 tool with one rung 4 write path designs that path for rung 4 and the rest for rung 2.
- "We don't know yet" is fine: record the deferral and design for the next rung up only where changing later would be expensive, such as the data model and the write path.
