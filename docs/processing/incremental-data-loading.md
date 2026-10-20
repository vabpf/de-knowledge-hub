---
id: processing/incremental-data-loading
title: Incremental Data Loading
description: Incremental loading applies changes since a recorded boundary instead
  of rebuilding everything. Correctness depends on how changes are captured, replayed,
  and committed.
type: pattern
status: published
difficulty: intermediate
tags:
- data-processing
- reliability
prerequisites:
- foundations/distributed-computing
related:
- orchestration/airflow-vs-dagster
- processing/apache-spark
implementations: []
verified_at: '2026-10-19'
sources:
- postgres-insert
- postgres-decoding
- postgres-isolation
applies_to: General pattern; PostgreSQL 16 features used as examples
---

# Incremental Data Loading

## TL;DR

Incremental loading applies changes since a recorded boundary instead of rebuilding everything. Correctness depends on how changes are captured, replayed, and committed.

## Why It Exists

A full reload may be too slow or expensive for the freshness target. Incremental work narrows the input, but introduces state: a cursor, watermark, or log position must agree with what the destination has durably applied.

## How It Works

Choose a change source: an update column, an append-only sequence, or change data capture (CDC). A timestamp watermark needs explicit assumptions about late commits, ties, clock behavior, updates, and deletions. A generic wall-clock maximum does not establish complete coverage.

Capture a bounded input set, apply it idempotently, and advance state only after the output is durable. When output and checkpoint share a transactional database, a transaction can make their update atomic. Across separate systems, design recovery for the gap rather than claiming a single atomic commit.

PostgreSQL 16 `ON CONFLICT` can implement a row upsert using a unique key. Logical decoding is a different mechanism that derives changes from WAL; a durable consumer must still handle replay and replication-slot retention. These are examples of building blocks, not a complete CDC service.

## Practical Example

This toy model assumes a strictly ordered, complete change log with integer offsets. It demonstrates replay safety, not concurrent capture or durable transactions.

```python
changes = [(1, 10, 5), (2, 11, 3), (3, 10, 12)]
def apply(target, checkpoint, batch):
    updated = dict(target)
    for offset, customer_id, amount in batch:
        if offset > checkpoint:
            updated[customer_id] = amount
    return updated, max([checkpoint] + [offset for offset, _, _ in batch])
first, cursor = apply({}, 0, changes)
replayed, same_cursor = apply(first, cursor, changes)
assert first == replayed == {10: 12, 11: 3}
assert cursor == same_cursor == 3
```

In production, persist the target and checkpoint together where possible. Test a crash before and after each durable write. Define deletes, schema changes, and late events explicitly.

## Trade-offs

CDC captures more kinds of changes than an insert-only timestamp query but needs operational state and retention management. Overlapping extraction windows can recover bounded lateness when writes are idempotent; they do not cover unbounded lateness. Keep periodic reconciliation against a trusted snapshot.

## Common Misconceptions

“Exactly once” is not established by an upsert alone. Advancing a cursor before writing output can lose records. An update timestamp may miss deletes. Retrying an append sink can duplicate results even if extraction is deterministic.

## Related Concepts

[Airflow vs. Dagster](../orchestration/airflow-vs-dagster.md) considers scheduling and backfills. [Distributed Computing](../foundations/distributed-computing.md) supplies the partial-failure model.

## References

- [PostgreSQL INSERT and ON CONFLICT](https://www.postgresql.org/docs/16/sql-insert.html), 16; verified October 19, 2026.
- [PostgreSQL Logical Decoding Concepts](https://www.postgresql.org/docs/16/logicaldecoding-explanation.html), 16; verified October 19, 2026.
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/16/transaction-iso.html), 16; verified October 19, 2026.
