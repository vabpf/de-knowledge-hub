---
id: distributed-systems/data-skew
title: Data Skew
description: Data skew is uneven work across partitions or tasks. Diagnose which records
  or keys concentrate the work before adding resources or changing partition counts.
type: problem
status: published
difficulty: intermediate
tags:
- distributed-systems
- performance
- spark
prerequisites:
- distributed-systems/partitioning
- distributed-systems/data-shuffling
related:
- processing/spark-execution-model
- processing/incremental-data-loading
implementations: []
verified_at: '2026-10-19'
sources:
- spark-tuning
applies_to: General diagnosis; Spark SQL 3.5.7 adaptive skew-join discussion
---

# Data Skew

## TL;DR

Data skew is uneven work across partitions or tasks. Diagnose which records or keys concentrate the work before adding resources or changing partition counts.

## Why It Exists

A pipeline can spend most of its runtime waiting for a small fraction of tasks. More workers may sit idle if the remaining work is concentrated in one destination. Unequal record counts are one signal; record size and computation cost can also differ.

## How It Works

Compare task duration, input and shuffle bytes, spill, and key frequencies. Check for hot keys, null or default keys, and joins that multiply matching rows. Distinguish these from a slow host or uneven external service latency. These are diagnostic hypotheses, not conclusions from a single long-running task.

For Spark SQL 3.5.7, adaptive execution can optimize certain skewed sort-merge joins when its documented conditions and settings apply. It is not a general solution for every skewed aggregation. Inspect the actual plan before attributing a speedup to this mechanism.

## Practical Example

This local example demonstrates why increasing the number of hash buckets does not divide one hot key. It is not Spark's hash implementation.

```python
from collections import Counter
keys = ["hot"] * 90 + [f"cold-{n}" for n in range(10)]
counts = Counter(keys)
assert counts["hot"] == 90
# A deterministic toy hash, not the function used by Spark.
for partition_count in (2, 8, 32):
    loads = Counter(sum(key.encode()) % partition_count for key in keys)
    assert max(loads.values()) >= 90
```

A possible repair for a decomposable sum is partial aggregation before movement. Salting a hot key requires a second combine step and an explicit correctness argument; do not salt a join or non-associative calculation blindly.

## Trade-offs

Filtering invalid defaults changes semantics unless the data contract permits it. Broadcasting a genuinely small relation can avoid some join redistribution but increases per-worker memory use. Salting adds intermediate work. Always compare output totals and key-level results before and after a repair.

## Common Misconceptions

Balanced input file sizes do not guarantee balanced downstream grouping. More partitions cannot spread one key if equal keys must meet. A slow task alone does not prove skew. Synthetic examples here are not benchmark results.

## Related Concepts

Use [Spark Execution Model](../processing/spark-execution-model.md) to locate the stage involved. [Data Partitioning](partitioning.md) explains key placement, and [Data Shuffling](data-shuffling.md) explains redistribution.

## References

- [Spark SQL Performance Tuning](https://spark.apache.org/docs/3.5.7/sql-performance-tuning.html), 3.5.7; verified October 19, 2026.
