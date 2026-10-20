---
id: distributed-systems/partitioning
title: Data Partitioning
description: Dividing data into subsets for parallel processing.
type: concept
status: published
difficulty: beginner
tags:
- distributed-systems
- data-processing
prerequisites:
- foundations/distributed-computing
related:
- distributed-systems/data-shuffling
implementations:
- processing/apache-spark
verified_at: '2026-10-19'
sources:
- spark-rdd
---

# Data Partitioning

## TL;DR

Partitioning divides data into subsets that can be processed independently. The distribution of records affects parallelism and load balance.

## Why It Exists

Large computations need to divide work across tasks. Partition boundaries let an engine assign portions of a dataset to different workers.

## How It Works

A rule assigns each record to a partition. Hash partitioning groups equal keys; range partitioning assigns intervals. The rule and partition count determine placement. Uneven key frequencies can produce uneven work even with a uniform hash function. Execution partitions and directory partitions in a storage layout serve different purposes.

## Practical Example

This illustrative hash rule partitions integer customer IDs into two groups; it is not a claim about a particular engine's hash function.

```python
rows = [(10, 5), (11, 3), (10, 7), (12, 2)]
partitions = {0: [], 1: []}
for customer_id, amount in rows:
    partitions[customer_id % 2].append((customer_id, amount))
assert partitions == {0: [(10, 5), (10, 7), (12, 2)], 1: [(11, 3)]}
```

## Trade-offs

More partitions can expose parallel work but add scheduling overhead. A hot key can dominate one partition. Choosing a different key can improve balance but may require redistribution for a later computation.

## Common Misconceptions

A partition is not permanently tied to one machine. Increasing the partition count does not necessarily spread the work of one hot key.

## Related Concepts

Start with [Distributed Computing](../foundations/distributed-computing.md). See [Apache Spark](../processing/apache-spark.md) for an implementation.

[Data Shuffling](data-shuffling.md) explains redistribution between processing stages.

## References

- [Apache Spark 3.5.7 RDD Programming Guide](https://spark.apache.org/docs/3.5.7/rdd-programming-guide.html), sections on parallelized collections and shuffle operations; consulted October 19, 2026. Spark is one implementation example; the Python example above is illustrative.
