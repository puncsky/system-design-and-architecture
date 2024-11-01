---
slug: 181-concurrency-models
id: 181-concurrency-models
layout: post
title: "并发模型"
date: 2019-10-16 14:04
comments: true
tags: [系统设计]
description: "您可能想了解的五种并发模型：单线程；多处理和基于锁的并发；通信顺序进程 (CSP)；演员模型 (AM)；软件事务内存 (STM)。"
---

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571262011/web-guiguio/Concurrency_Models_1.png)


* 单线程 - 回调、承诺、可观察对象和 async/await：原生 JS
* 线程/多处理，基于锁的并发
    * 保护临界区与性能
* 通信顺序进程 (CSP)
	* Golang 或 Clojure 的 `core.async`。 
	* 进程/线程通过通道传递数据。
* 演员模型 (AM)：Elixir、Erlang、Scala
	* 本质上是异步的，并且具有跨运行时和机器的位置信息透明性 - 如果您有演员的引用 (Akka) 或 PID (Erlang)，您可以通过邮箱向其发送消息。
	* 通过将演员组织成监督层次结构来实现强大的容错能力，您可以在其确切的层次结构级别处理故障。
* 软件事务内存 (STM)：Clojure、Haskell
	* 类似于 MVCC 或纯函数：提交 / 中止 / 重试