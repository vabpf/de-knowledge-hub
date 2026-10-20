---
id: processing/spark-execution-model
title: Spark Execution Model
description: Spark coordinates jobs as stages containing tasks. Understanding that
  structure helps connect a slow query to the work actually running.
type: mechanism
status: published
difficulty: intermediate
tags:
- spark
- data-processing
- performance
prerequisites:
- processing/apache-spark
- distributed-systems/data-shuffling
related:
- distributed-systems/data-skew
- processing/incremental-data-loading
implementations: []
verified_at: '2026-10-19'
sources:
- spark-cluster
- spark-rdd
- spark-sql
applies_to: Apache Spark 3.5.7; RDD and DataFrame execution concepts
---

# Spark Execution Model

## TL;DR

Spark coordinates jobs as stages containing tasks. Understanding that structure helps connect a slow query to the work actually running.

## Why It Exists

A query’s logical operations do not directly reveal its network transfers, task parallelism, or bottleneck. The execution model supplies a vocabulary for inspecting plans and runtime evidence.

## How It Works

The driver schedules work on executors. For the RDD model, transformations record dependencies, and actions request results. Shuffle dependencies introduce stage boundaries. A task handles a partition for a particular stage; partitions, tasks, executor processes, and host machines are different units.

DataFrame queries add SQL planning and optimization. Read the physical plan, then inspect the actual execution. Avoid predicting an exact number of jobs from the source code alone: API details, query planning, and adaptive execution can change the work.

## Practical Example

Conceptual walkthrough, not a runtime trace:

1. Read two input partitions of `(customer_id, amount)` rows.
2. Filter invalid amounts independently within each input partition.
3. Group by customer, redistributing contributions when the required grouping is absent.
4. Combine customer totals in destination partitions and write the output.

In the [Spark overview example](apache-spark.md#practical-example), inspect the output of `explain()` for an exchange and aggregation. Confirm task counts and shuffle metrics in your own run rather than asserting that every `groupBy` produces the same plan.

## Trade-offs

Large tasks can amortize scheduling overhead but limit parallelism or exceed working memory. Many tiny tasks can waste time scheduling. Caching can help repeated work but consumes storage and should be justified by reuse. Optimize a measured bottleneck instead of treating partition count as a universal tuning knob.

## Common Misconceptions

A stage is not a machine. Adding executors does not split a single hot-key aggregation arbitrarily. A transformation call is not necessarily an immediate distributed computation. A successful retry says little about whether arbitrary external writes were duplicated.

## Related Concepts

Use [Data Skew](../distributed-systems/data-skew.md) to distinguish uneven work from insufficient cluster capacity. [Incremental Data Loading](incremental-data-loading.md) reduces the amount of data scheduled in the first place.

## References

- [Spark Cluster Mode Overview](https://spark.apache.org/docs/3.5.7/cluster-overview.html), 3.5.7; verified October 19, 2026.
- [Spark RDD Programming Guide](https://spark.apache.org/docs/3.5.7/rdd-programming-guide.html), 3.5.7; verified October 19, 2026.
- [Spark SQL Getting Started](https://spark.apache.org/docs/3.5.7/sql-getting-started.html), 3.5.7; verified October 19, 2026.
