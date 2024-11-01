---
slug: 2018-07-24-replica-and-consistency
id: 2018-07-24-replica-and-consistency
layout: post
title: "副本、一致性与CAP定理"
date: 2018-07-24 11:54
comments: true
categories: 系统设计
description: "任何网络系统都有三种理想属性：一致性、可用性和分区容忍性。系统只能拥有这三者中的两者。例如，关系数据库管理系统（RDBMS）更倾向于一致性和分区容忍性，因此成为ACID系统。"
references:
    - https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed
---

## 为什么副本和一致性？

大数据集 ⟶ 扩展 ⟶ 数据分片/分区 ⟶ 1) 数据访问路由 2) 可用性副本 ⟶ 一致性挑战



## CAP定理的一致性权衡

![CAP定理](https://res.cloudinary.com/dohtidfqh/image/upload/v1566606463/web-guiguio/Es1houG50FNQoCgGUo2fGwMPriezTtKqliSVMW9F11CN2W7SSHcI3li61Qdnw0FoOm0UfitYOvbAiJBvJXLmAmrjRH75VDO54uGucIynJrdR2RV51GboaZ17bc5pZt88_GK43PT0.png)

- 一致性：所有节点在同一时间看到相同的数据
- 可用性：保证每个请求都能收到关于其成功或失败的响应
- 分区容忍性：系统在任意消息丢失或部分系统故障的情况下继续运行



任何网络共享数据系统只能拥有三种理想属性中的两种。

- 关系数据库管理系统（rDBMS）倾向于CP ⟶ ACID
- NoSQL倾向于AP ⟶ BASE



## “2 of 3”是误导性的

12年后，作者埃里克·布鲁尔（Eric Brewer）表示“2 of 3”是误导性的，因为

1. 分区是罕见的，当系统没有分区时，几乎没有理由放弃C或A。
2. 选择实际上可以在同一系统内的多个地方以非常细的粒度应用。
3. 选择不是二元的，而是有一定程度的。



因此，当没有分区（节点正确连接）时，这种情况经常发生，我们应该同时拥有AC。当出现分区时，处理它们的步骤如下：

1. 检测分区的开始，
2. 进入可能限制某些操作的显式分区模式，并
3. 当通信恢复时启动分区恢复（补偿错误）。