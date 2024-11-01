---
slug: 80-relational-database
id: 80-relational-database
title: "关系数据库简介"
date: 2018-10-18 23:19
comments: true
tags: [系统设计]
description: 关系数据库是大多数存储使用案例的默认选择，原因在于原子性、一致性、隔离性和持久性。这里的一致性与 CAP 定理中的一致性有什么不同？我们为什么需要 3NF 和数据库代理？
references:
  - https://www.puncsky.com/blog/2016-02-13-crack-the-system-design-interview
---

关系数据库是大多数存储使用案例的默认选择，原因在于 ACID（原子性、一致性、隔离性和持久性）。一个棘手的问题是“一致性”——它意味着任何事务都会将数据库从一个有效状态转变为另一个有效状态，这与 [CAP 定理](https://tianpan.co/notes/2018-07-24-replica-and-consistency) 中的一致性不同。

## 模式设计和第三范式 (3NF)

为了减少冗余并提高一致性，人们在设计数据库模式时遵循 3NF：

- 1NF：表格形式，每个行列交集只包含一个值
- 2NF：只有主键决定所有属性
- 3NF：只有候选键决定所有属性（且非主属性之间不相互依赖）

## 数据库代理

如果我们想消除单点故障怎么办？如果数据集太大，无法由单台机器承载怎么办？对于 MySQL，答案是使用数据库代理来分配数据，<a target="_blank" href="http://dba.stackexchange.com/questions/8889/mysql-sharding-vs-mysql-cluster">可以通过集群或分片</a>。

集群是一种去中心化的解决方案。一切都是自动的。数据会自动分配、移动和重新平衡。节点之间互相传递信息（尽管这可能导致组隔离）。

分片是一种集中式解决方案。如果我们去掉不喜欢的集群属性，分片就是我们得到的结果。数据是手动分配的，不会移动。节点之间互不知晓。