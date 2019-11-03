---
layout: post
title: "Lambda 架构"
date: 2018-10-23 10:30
comments: true
categories: architecture, system design
language: zh-cn
abstract: 使用Lambda可以解决大数据所带来的三个问题：准确性（好）；延迟（快）；吞吐量（多）。lambda 架构可以指导我们如何为一个数据系统实现扩展。
references:
  - https://www.amazon.com/Big-Data-Principles-practices-scalable/dp/1617290343
---

## 为什么要使用lambda架构？

为了解决大数据所带来的三个问题

1. 准确性（好）
2. 延迟（快）
3. 吞吐量（多）


例如：以传统方式扩展网页浏览数据记录的问题

1. 首先使用传统的关系数据库
2. 然后添加一个“发布/订阅”模式队列
3. 然后通过横向分区或者分片的方式来扩展规模
4. 容错性问题开始出现
5. 数据损坏(data corruption)的现象开始出现


关键问题在于[AKF扩展立方体](/notes/42-how-to-scale-a-web-service)中，==仅有X轴的水平分割一个维度是不够的，我们还需要引入Y轴的功能分解。而 lambda 架构可以指导我们如何为一个数据系统实现扩展==。


## 什么是lambda架构

如果我们将一个数据系统定义为以下形式：

```txt
Query=function(all data)
```


那么一个lamda架构就是

![Lambda Architecture](/img/lambda-architecture.png)

```txt
batch view = function(all data at the batching job's execution time)
realtime view = function(realtime view, new data)

query = function(batch view. realtime view)
```

==lambda架构 = 读写分离(批处理层 + 服务层) + 实时处理层==


![Lambda Architecture for big data systems](https://res.cloudinary.com/dohtidfqh/image/upload/v1548840018/web-guiguio/lambda-architecture-for-big-data-systems.png)
