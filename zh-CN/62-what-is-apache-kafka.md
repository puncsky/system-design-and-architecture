---
layout: post
title: "什么是 Apache Kafka?"
date: 2018-09-27 04:06
comments: true
categories: system design
language: zh-cn
abstract: Apache Kafka是一个分布式流平台。它的特点包括分布式发布-订阅(pub-sub)消息传递系统，可将N ^ 2的关系简化成N，发布者和订阅者可以按自己的速率运行；超快速的零复制(zero-copy)技术；支持可容错的数据持久化。
references:
  - https://kafka.apache.org/intro
  - http://www.michael-noll.com/blog/2014/08/18/apache-kafka-training-deck-and-tutorial/
  - https://stackoverflow.com/questions/48271491/where-is-apache-kafka-placed-in-the-pacelc-theorem
  - https://engineering.linkedin.com/kafka/intra-cluster-replication-apache-kafka
---

Apache Kafka是一个分布式流(streaming)平台。



## 为什么使用Apache Kafka?

它的抽象是一个==队列==，它的特点包括

* 分布式发布-订阅(pub-sub)消息传递系统，可将N ^ 2的关系简化成N.发布者和订阅者可以按自己的速率运行。
* 超快速的零复制(zero-copy)技术
* 支持可容错的数据持久化

它可以被应用于

* 按主题打日志
* 消息系统
* 异地备份
* 流处理



## 为什么Kafka如此的快？

Kafka使用零复制技术，其中，CPU不会执行数据跨存储区复制副本(replica)的任务。

不使用零复制技术:

<img src="/img/kafka-without-zero-copy.png" style="width: 100%; max-width: 400px;">


使用零复制技术:

<img src="/img/kafka-with-zero-copy.png" style="width: 100%; max-width: 300px;">


## 构架

从外部看，生产者写给kafka集群，而用户从kafka集群读取内容。

<img src="/img/kafka-pub-sub.png" style="width: 100%; max-width: 300px;">


数据按照主题存储，并分割为可复制副本的分区。

![Kafka Cluster Overview](/img/kafka-cluster-overview.png)


1. 生产者将消息发布到特定主题中。
	* 首先写入内存缓冲区中并更新到磁盘中。
	* 为了实现快速写，使用 append-only 的序列写。
	* 写入后方可读取。
2. 消费者从特定主题中提取消息。
	* 使用“偏移指针”（偏移量为SEQ ID）来跟踪/控制其唯一的读取进度。
3. 一个主题包括分区和负载均衡，其中，每个分区是一个有序,不变的序列的记录。
	* 分区决定用户（组）的并行性。同一时间内，一个用户只可以读取一个分区。


如何序列化数据? Avro

它的网络协议是什么？ TCP

分区内的存储布局是怎样的y？ O（1）磁盘读取

<img src="/img/kafka-partition-data-layout.png" style="width: 100%; max-width: 300px;">



## 如何容错？

==同步副本（ISR）协议==. 其容许 (numReplicas - 1) 的节点挂掉。每个分区有一个 leader, 一个或多个 follower.

`总副本量 = 同步的副本 + 不同步的副本`

1. ISR 是一组活的并且与 leader 同步的副本（注意领导者总是在ISR中）。
2. 当发布新消息时，leader 在提交消息之前等待，直到它到达ISR中的所有副本为止。
3. ==如果 follower 同步失败，它将从ISR中退出，然后 leader 继续用ISR中较少的副本提交新消息。注意，此时系统运行在低副本数量的状态下== 如果一个 leader 失败了，另一个ISR将被选成为一个新的 leader 。
4. 未同步的副本不断的从 leader 那里拉出消息。一旦追赶上 leader ，它将被添加回ISR。



## Kafka是 [CAP 定理](/notes/2018-07-24-replica-and-consistency)中的AP或CP系统吗？?

Jun Rao认为它是CA，因为“我们的目标是支持在单个数据中心内的Kafka集群中进行复制，其中网络分区很少见，因此我们的设计侧重于维护高可用性和强一致性的副本。”


然而，它实际上取决于配置。

1. 如果使用初始配置（min.insync.replicas=1, default.replication.factor=1），你将获得AP系统（最多一次）。

2. 如果想获得CP，你可以设置min.insync.replicas=2，topic replication factor 为3，然后生成一个acks=all的消息将保证CP设置（至少一次），但是，如果没有足够的副本（副本数＜2）用于特定主题/分区时，则无法成功地写。
