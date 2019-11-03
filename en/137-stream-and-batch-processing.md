---
layout: post
title: "Stream and Batch Processing Frameworks"
date: 2019-02-16 22:13
comments: true
categories: system design
language: en
references:
  - https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43864.pdf
  - https://cs.stanford.edu/~matei/papers/2018/sigmod_structured_streaming.pdf
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
  - https://stackoverflow.com/questions/28502787/google-dataflow-vs-apache-storm
---

## Why such frameworks?

* process high-throughput in low latency.
* fault-tolerance in distributed systems.
* generic abstraction to serve volatile business requirements.
* for bounded data set (batch processing) and for unbounded data set (stream processing).


## Brief history of batch/stream processing

1. Hadoop and MapReduce. Google made batch processing as simple as MR `result = pairs.map((pair) => (morePairs)).reduce(somePairs => lessPairs)` in a distributed system.
2. Apache Storm and DAG Topology. MR doesn’t efficiently express iterative algorithms. Thus Nathan Marz abstracted stream processing into a graph of spouts and bolts.
3. Spark in-memory Computing. Reynold Xin said Spark sorted the same data **3X faster** using **10X fewer machines** compared to Hadoop.
4. Google Dataflow based on Millwheel and FlumeJava. Google supports both batch and streaming computing with the windowing API.


### Wait... But why is Flink gaining popularity?

1. its fast adoption of ==Google Dataflow==/Beam programming model.
2. its highly efficient implementation of Chandy-Lamport checkpointing.



## How? 

### Architectural Choices

To serve requirements above with commodity machines, the steaming framework use distributed systems in these architectures...

* master-slave (centralized): apache storm with zookeeper, apache samza with YARN.
* P2P (decentralized): apache s4.


### Features

1. DAG Topology for Iterative Processing. e.g. GraphX in Spark, topologies in Apache Storm, DataStream API in Flink.
2. Delivery Guarantees. How guaranteed to deliver data from nodes to nodes? at-least once / at-most once / exactly once.
3. Fault-tolerance. Using [cold/warm/hot standby, checkpointing, or active-active](/notes/85-improving-availability-with-failover).
4. Windowing API for unbounded data set. e.g. Stream Windows in Apache Flink. Spark Window Functions. Windowing in Apache Beam.


## Comparison

| Framework                   | Storm         | Storm-trident | Spark        | Flink        |
| --------------------------- | ------------- | ------------- | ------------ | ------------ |
| Model                       | native        | micro-batch   | micro-batch  | native       |
| Guarentees                  | at-least-once | exactly-once  | exactly-once | exactly-once |
| Fault-tolerance             | Record-Ack    | record-ack    | checkpoint   | checkpoint   |
| Overhead of fault-tolerance | high          | medium        | medium       | low          |
| latency                     | very-low      | high          | high         | low          |
| throughput                  | low           | medium        | high         | high         |
