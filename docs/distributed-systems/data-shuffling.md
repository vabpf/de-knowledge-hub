---
id: distributed-systems/data-shuffling
title: Data Shuffling
description: Redistributing records between parallel processing stages.
type: mechanism
status: published
difficulty: intermediate
tags:
- distributed-systems
- data-processing
- performance
prerequisites:
- distributed-systems/partitioning
related:
- distributed-systems/partitioning
implementations: []
verified_at: '2026-10-19'
sources:
- spark-rdd
---

# Data Shuffling

## TL;DR

A shuffle redistributes records so the next stage has the data it needs together. It can add network, serialization, and disk costs.

## Why It Exists

An aggregation by customer needs all contributions for each customer to meet. The previous stage may have divided input by file rather than customer.

## How It Works

Producers select destination partitions, write intermediate records, and consumers fetch their assigned data. Local combining can reduce transferred volume. Exact buffering, sorting, and persistence depend on the engine and version.

## Practical Example

Two illustrative input partitions contain `[(10, 5), (11, 3)]` and `[(10, 7), (12, 2)]`. Routing by `customer_id % 2` sends both customer 10 records to destination 0. Summing there yields `{10: 12, 12: 2}`; destination 1 yields `{11: 3}`. This is a conceptual example, not runnable distributed code.

## Trade-offs

Redistribution enables global grouping but consumes bandwidth and intermediate storage. A skewed destination can become a bottleneck. Partial aggregation can reduce volume when the aggregation permits it.

## Common Misconceptions

Not every transformation needs a shuffle. In Spark, mapping each record independently can avoid one; grouping may require one depending on existing partitioning. Shuffle does not imply that every record travels to another machine.

## Related Concepts

Read [Data Partitioning](partitioning.md) first to understand destination assignment.

## References

- [Apache Spark 3.5.7 RDD Programming Guide: Shuffle Operations](https://spark.apache.org/docs/3.5.7/rdd-programming-guide.html#shuffle-operations), consulted October 19, 2026. Engine details should be rechecked when adopting a different Spark version.
