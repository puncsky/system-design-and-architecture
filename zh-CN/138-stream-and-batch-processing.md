---
layout: post
title: "流处理和批处理框架"
date: 2019-02-27 02:20
comments: true
categories: architecture, system design
language: zh-cn
references:
  - https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43864.pdf
  - https://cs.stanford.edu/~matei/papers/2018/sigmod_structured_streaming.pdf
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
  - https://stackoverflow.com/questions/28502787/google-dataflow-vs-apache-storm
---

## 为什么有这种框架？
 
 * 为了在更短的时间内处理更多的数据。
 * 统一处理分布式系统中的容错问题。
 * 将任务简化抽象以应对多变的业务要求。
 * 分别适用于有界数据集（批处理）和无界数据集（流处理）。
 
 
 
 ## 批处理与流处理的发展史简介
 
 1. Hadoop 与 MapReduce。谷歌让批处理在一个分布式系统中像 MapRduce`result = pairs.map((pair) => (morePairs)).reduce(somePairs => lessPairs)`一样简单。
 2. Apache Storm 与有向图拓扑结构。MapReduce 不能很好地表示迭代算法。因此，内森·马兹（Nathan Marz）将流处理抽象成一个由 spouts 和 bolts 组件构成的图结构。
 3. Spark 内存计算。辛湜（Reynold Xin）指出 Spark 在处理相同数据的时候比 Hadoop **少使用十倍机器**的同时**速度却快三倍**
 4. 基于 Millwheel 和 FlumeJava 的谷歌数据流（Google Dataflow）。谷歌使用窗口化API同时支持批处理与流处理。
 
 
 
 ### 等等...那么为什么 Flink 变得如此热门？
 
 1. Flink 快速采纳了 ==Google Dataflow== 以及 Apache Beam 的编程模式。
 2. Flink 对 Chandy-Lamport checkpointing 算法的高效实现。
 
 
 
 ## 这些框架
 
 ### 架构选择
 
 若要用商业机器来满足以上的需求，有这些热门的分布式系统架构……
 
 * master-slave（中心化的）：Apache Storm + zookeeper， Apache Samza + YARN
 * P2P（去中心化的）：Apache s4
 
 ### 功能
 
 1. DAG Topology 用来迭代处理 -例如Spark 中的 GraphX， Apache Storm 中的 topologies， Flink 中的 DataStream API。
 2. 交付保证 (Delivery Guarantees)。如何确保节点与节点之间数据交付的可靠性？至少一次 / 至多一次 / 一次。
 3. 容错性。使用[cold/warm/hot standby, checkpointing 或者 active-active 来实现容错。](/notes/85-improving-availability-with-failover)
 4. 无界数据集的窗口化API。例如 Apache 的流式窗口。Spark 的Window函数。Apache Beam 的窗口化。
 
 
 
 ## 不同架构的区别对照表
 
 | 架构       | Storm    | Storm-trident | Spark  | Flink  |
 | ---------- | -------- | ------------- | ------ | ------ |
 | 模型       | 原生     | 微批量        | 微批量 | 原生   |
 | Guarentees | 至少一次 | 一次          | 一次   | 一次   |
 | 容错性     | 记录Ack  | 记录Ack       | 检查点 | 检查点 |
 | 最大容错   | 高       | 中            | 中     | 低     |
 | 延迟       | 非常低   | 高            | 高     | 低     |
 | 吞吐量     | 低       | 中            | 高     | 高     |
 
