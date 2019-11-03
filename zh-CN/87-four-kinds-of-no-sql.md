---
layout: post
title: "4种非关系型数据库（No-SQL）"
date: 2018-10-27 01:02
comments: true
categories: architecture, system design
language: zh-cn
abstract: 为了优化读取性能，通过添加冗余数据或分组数据引入了“去正规化”。这里提供了四种非关系型数据库帮助优化：键值存储；文档存储；面向列存储；图数据库
references:
  - https://www.puncsky.com/blog/2016-02-13-crack-the-system-design-interview
---

在常规的互联网服务中，读写的比例大约是100:1到1000:1。但是，从硬盘读取数据时，数据库的连接操作非常耗时，99%的时间都花在磁盘查找上，更不用说跨网络的分布式连接操作了。

为了优化读取性能，通过添加冗余数据或分组数据引入了 **去正规化**。这里提供了四种非关系型数据库帮助优化。



## 键值存储

键值存储的抽象表现是一个巨大的散列表/散列映射/字典。

我们希望使用键值缓存的主要原因是为了减少访问活动数据的延迟。在快速而昂贵的存储媒体(如内存或SSD)上实现O(1)复杂度的读写性能，而不是在缓慢而廉价的媒体(通常是硬盘驱动器)上实现传统的O(logn)复杂度读写。

在设计缓存时，有三个主要因素需要考虑。

1. 模式：如何缓存？它是直读/直写/写入/回写/缓存吗？
2. 放置：缓存放置的位置是什么？ 客户端/不同的层/服务器端？
3. 更换：何时过期/更换数据？LRU/LFU/ARC？

可用选择：Redis还是Memcache?Redis支持数据持久性，而Memcache不支持。除此之外，还有 Riak, Berkeley DB, HamsterDB, Amazon Dynamo, Project Voldemort等。

## 文档存储

文档存储的抽象表现类似于键值存储，但是文档（如XML，JSON，BSON等）存储在该对的值部分中。

我们使用文档存储的主要原因是为了提高灵活性和性能。通过无模式文档实现了灵活性，通过破坏3NF提高了性能。创业公司的业务需求不断变化，灵活的架构使他们能够快速行动。

可用选择：MongoDB，CouchDB，Terrastore，OrientDB，RavenDB等。



## 面向列存储

面向列的存储的抽象就像一个巨大的嵌套映射:ColumnFamily<RowKey, Columns<Name, Value, Timestamp>>。

我们想要使用面向列的存储的主要原因是它是分布式的，且拥有高可用性，并且针对数据写入进行了优化。

可用选择：Cassandra，HBase，Hypertable，Amazon SimpleDB等。



## 图数据库

顾名思义，这个数据库的抽象表现是一个图。它允许我们存储实体和它们之间的关系。

如果使用关系数据库存储图形，那么添加/删除关系可能涉及到模式更改和数据移动，而使用图形数据库时则不是这样。另一方面，当我们在关系数据库中为图形创建表时，需基于我们想要的遍历建立模型；如果遍历发生更改，则数据必须更改。

可用选择:Neo4J、Infinitegraph、OrientDB、FlockDB等。
