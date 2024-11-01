---
slug: 83-lambda-architecture
id: 83-lambda-architecture
layout: post
title: "Lambda 架构"
date: 2018-10-23 10:30
comments: true
categories: 系统设计
language: cn
description: Lambda 架构 = CQRS（批处理层 + 服务层） + 快速层。它解决了大数据的准确性、延迟和吞吐量问题。
references:
  - https://www.amazon.com/Big-Data-Principles-practices-scalable/dp/1617290343
  - https://mapr.com/resources/stream-processing-mapr/
---

## 为什么选择 Lambda 架构？

为了解决大数据带来的三个问题

1. 准确性（好）
2. 延迟（快）
3. 吞吐量（多）


例如，传统方式扩展页面查看服务的问题

1. 你从传统关系数据库开始。
2. 然后添加一个发布-订阅队列。
3. 然后通过水平分区或分片进行扩展。
4. 故障容错问题开始出现。
5. 数据损坏发生。

关键点是 ==[AKF 规模立方体](https://tianpan.co/notes/41-how-to-scale-a-web-service) 的 X 轴维度单独并不足够。我们还应该引入 Y 轴 / 功能分解。Lambda 架构告诉我们如何为数据系统做到这一点。==



## 什么是 Lambda 架构？

如果我们将数据系统定义为

```txt
查询 = 函数（所有数据）
```


那么 Lambda 架构是

![Lambda 架构](/img/lambda-architecture.png)


```txt
批处理视图 = 函数（批处理作业执行时的所有数据）
实时视图 = 函数（实时视图，新数据）

查询 = 函数（批处理视图，实时视图）
```

==Lambda 架构 = CQRS（批处理层 + 服务层） + 快速层==


![适用于大数据系统的 Lambda 架构](https://res.cloudinary.com/dohtidfqh/image/upload/v1548840018/web-guiguio/lambda-architecture-for-big-data-systems.png)

```