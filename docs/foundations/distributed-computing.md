---
id: foundations/distributed-computing
title: Distributed Computing
description: Distributed computing coordinates work across processes that communicate
  over a network. It expands the work a system can handle while making coordination
  and partial failure part of the design.
type: concept
status: published
difficulty: beginner
tags:
- distributed-systems
prerequisites: []
related:
- distributed-systems/partitioning
- processing/apache-spark
implementations: []
verified_at: '2026-10-19'
sources:
- mapreduce-paper
---

# Distributed Computing

## TL;DR

Distributed computing coordinates work across processes that communicate over a network. It expands the work a system can handle while making coordination and partial failure part of the design.

## Why It Exists

A dataset may exceed one machine’s storage, or a computation may need more throughput than one worker can provide. Distributing independent pieces can help. First measure a single-machine implementation: orchestration and data movement have costs, and a small job can finish sooner on one machine.

## How It Works

Divide the input into units, assign units to workers, and combine outputs. The MapReduce paper gives a concrete map-and-reduce design, including retrying failed work and bringing equal keys together. This is one model, not a requirement for every distributed system.

A useful design exercise is to enumerate failure points: a worker can finish a write before its acknowledgement is lost; a coordinator can retry work whose outcome is unknown. Keep external writes idempotent or use a commit protocol with explicit recovery. Distribution alone does not establish exactly-once side effects.

## Practical Example

This local simulation shows decomposition and combination; it does not emulate networking or failures. Each chunk can be counted independently because addition is associative.

```python
from collections import Counter
chunks = [["red", "blue"], ["red", "green", "red"]]
partials = [Counter(chunk) for chunk in chunks]
result = Counter()
for partial in partials:
    result.update(partial)
assert result == {"red": 3, "blue": 1, "green": 1}
```

If the second chunk is retried, replace its previous partial result rather than adding it twice. In a real system, chunk identity and commit state must survive process restarts.

## Trade-offs

Parallel execution introduces coordination, serialization, and network overhead. Slow workers delay dependent work. Replication can improve resilience but consumes capacity. Benchmark throughput and recovery under representative data distributions rather than assuming a linear speedup.

## Common Misconceptions

A distributed system is not automatically faster or fault tolerant. Multiple processes on one host can model concurrency but do not demonstrate resilience to host failure. Retrying a computation does not make every external side effect safe to repeat.

## Related Concepts

Read [Data Partitioning](../distributed-systems/partitioning.md) for work assignment, then [Apache Spark](../processing/apache-spark.md) for a concrete processing engine.

## References

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI 2004; verified October 19, 2026.
