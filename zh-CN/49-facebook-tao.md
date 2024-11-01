---
slug: 49-facebook-tao
id: 49-facebook-tao
layout: post
title: "Facebook 如何扩展其社交图谱存储？TAO"
date: 2018-09-18 22:50
comments: true
categories: system design
language: cn
description: "在 TAO 之前，Facebook 使用缓存旁路模式来扩展其社交图谱存储。存在三个问题：列表更新操作效率低；客户端必须管理缓存，且很难提供读后写一致性。通过 TAO，这些问题得以解决。"
references:
  - http://www.cs.cornell.edu/courses/cs6410/2015fa/slides/tao_atc.pptx
  - https://cs.stanford.edu/~matei/courses/2015/6.S897/slides/tao.pdf
  - https://www.facebook.com/notes/facebook-engineering/tao-the-power-of-the-graph/10151525983993920/
---

## 面临的挑战是什么？

在 TAO 之前，使用缓存旁路模式

![在 TAO 之前](https://puncsky.com/img/tao-before.png)

社交图谱数据存储在 MySQL 中，并缓存于 Memcached 中


三个问题：

1. Memcached 中的列表更新操作效率低。无法追加，只能更新整个列表。
2. 客户端必须管理缓存
3. 难以提供 ==读后写一致性==


为了解决这些问题，我们有三个目标：

- 高效扩展的在线数据图服务
- 优化读取（其读写比为 500:1）
	- 低读取延迟
	- 高读取可用性（最终一致性）
- 写入的及时性（读后写）



## 数据模型

- 具有唯一 ID 的对象（例如用户、地点、评论）
- 两个 ID 之间的关联（例如标签、喜欢、作者）
- 两者都有键值数据以及时间字段



## 解决方案：TAO

1. 高效扩展并减少读取延迟
	- 图特定缓存
	- 在无状态服务层和数据库层之间的独立缓存层（即 [功能分解](https://tianpan.co/notes/41-how-to-scale-a-web-service)）
	- 数据中心的细分（即 [水平数据分区](https://tianpan.co/notes/41-how-to-scale-a-web-service)）


2. 写入及时性
	- 写透缓存
    - 领导/跟随缓存以解决雷鸣般的拥挤问题
	- 异步复制


3. 读取可用性
	- 读取故障转移到备用数据源



## TAO 的架构

- MySQL 数据库 → 持久性
- 领导缓存 → 协调对每个对象的写入
- 跟随缓存 → 提供读取但不提供写入。将所有写入转发给领导。


![Facebook TAO 架构](https://puncsky.com/img/tao-architecture.png)


读取故障转移

![Facebook TAO 读取故障转移](https://puncsky.com/img/tao-read-failover.png)