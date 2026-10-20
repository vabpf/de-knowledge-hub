# Data Engineering Knowledge Hub

Understand how data systems work, why they fail, and how to choose an approach.
Each article connects a core idea to a practical example, its costs, and primary references.

## Start with the fundamentals

Follow this path if distributed processing is new to you:

1. [Distributed Computing](foundations/distributed-computing.md): split work and reason about partial failure.
2. [Data Partitioning](distributed-systems/partitioning.md): decide which records belong together.
3. [Data Shuffling](distributed-systems/data-shuffling.md): move records to the computation that needs them.
4. [Apache Spark](processing/apache-spark.md): connect those ideas to a processing engine.
5. [Spark Execution Model](processing/spark-execution-model.md): understand jobs, stages, and tasks.

## Solve a problem

| What you need to do | Where to start |
| --- | --- |
| Diagnose a few tasks holding up a job | [Data Skew](distributed-systems/data-skew.md) |
| Avoid reloading the entire dataset | [Incremental Data Loading](processing/incremental-data-loading.md) |
| Choose how to schedule and reprocess a pipeline | [Airflow vs. Dagster](orchestration/airflow-vs-dagster.md) |

## Explore by domain

- **Foundations:** [Distributed Computing](foundations/distributed-computing.md).
- **Distributed systems:** [Partitioning](distributed-systems/partitioning.md), [Shuffling](distributed-systems/data-shuffling.md), [Skew](distributed-systems/data-skew.md).
- **Processing:** [Spark](processing/apache-spark.md), [Execution Model](processing/spark-execution-model.md), [Incremental Loading](processing/incremental-data-loading.md).
- **Orchestration:** [Airflow vs. Dagster](orchestration/airflow-vs-dagster.md).

## Find and use an article

Use search to look for a concept, symptom, or technology. On smaller screens, open the
menu for domain navigation. Each article includes a short answer, an explanation,
an example, trade-offs, misconceptions, and links for further reading.

Check the applicable versions and reference dates before applying engine-specific
advice. Small local simulations illustrate a mechanism; they are not production
implementations or performance benchmarks.
