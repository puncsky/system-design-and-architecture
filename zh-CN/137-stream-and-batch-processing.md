---
slug: 137-stream-and-batch-processing
id: 137-stream-and-batch-processing
layout: post
title: "流处理与批处理框架"
date: 2019-02-16 22:13
comments: true
tags: [系统设计]
description: "流处理和批处理框架可以以低延迟处理高吞吐量。为什么 Flink 正在获得越来越多的关注？如何在 Storm、Storm-trident、Spark 和 Flink 之间做出架构选择？"
references:
  - https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43864.pdf
  - https://cs.stanford.edu/~matei/papers/2018/sigmod_structured_streaming.pdf
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
  - https://stackoverflow.com/questions/28502787/google-dataflow-vs-apache-storm
---

## 为什么需要这样的框架？

* 以低延迟处理高吞吐量。
* 分布式系统中的容错能力。
* 通用抽象以满足多变的业务需求。
* 适用于有界数据集（批处理）和无界数据集（流处理）。

## 批处理/流处理的简史

1. Hadoop 和 MapReduce。Google 使批处理在分布式系统中变得简单，如 MR `result = pairs.map((pair) => (morePairs)).reduce(somePairs => lessPairs)`。
2. Apache Storm 和 DAG 拓扑。MR 无法有效表达迭代算法。因此，Nathan Marz 将流处理抽象为喷口和螺栓的图。
3. Spark 内存计算。Reynold Xin 表示，Spark 使用 **10 倍更少的机器** 以 **3 倍更快** 的速度对相同数据进行排序。
4. 基于 Millwheel 和 FlumeJava 的 Google Dataflow。Google 支持批处理和流处理计算，使用窗口 API。

### 等等……但为什么 Flink 正在获得越来越多的关注？

1. 它快速采用了 ==Google Dataflow==/Beam 编程模型。
2. 它对 Chandy-Lamport 检查点的高效实现。

## 如何？

### 架构选择

为了用商品机器满足上述需求，流处理框架在这些架构中使用分布式系统……

* 主从（集中式）：apache storm 与 zookeeper，apache samza 与 YARN。
* P2P（去中心化）：apache s4。

### 特性

1. DAG 拓扑用于迭代处理。例如，Spark 中的 GraphX，Apache Storm 中的拓扑，Flink 中的数据流 API。
2. 交付保证。如何保证从节点到节点的数据交付？至少一次 / 至多一次 / 精确一次。
3. 容错能力。使用 [冷/热备用、检查点或主动-主动](https://tianpan.co/notes/85-improving-availability-with-failover)。
4. 无界数据集的窗口 API。例如，Apache Flink 中的流窗口。Spark 窗口函数。Apache Beam 中的窗口处理。

## 比较

| 框架                       | Storm         | Storm-trident | Spark        | Flink        |
| --------------------------- | ------------- | ------------- | ------------ | ------------ |
| 模型                       | 原生          | 微批处理      | 微批处理     | 原生         |
| 保证                       | 至少一次     | 精确一次     | 精确一次     | 精确一次     |
| 容错能力                   | 记录确认      | 记录确认      | 检查点       | 检查点       |
| 容错开销                   | 高            | 中等          | 中等         | 低           |
| 延迟                       | 非常低        | 高            | 高           | 低           |
| 吞吐量                     | 低            | 中等          | 高           | 高           |