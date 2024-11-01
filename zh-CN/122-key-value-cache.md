---
slug: 122-key-value-cache
id: 122-key-value-cache
layout: post
title: "键值缓存"
date: 2019-01-06 23:24
comments: true
language: cn
abstract: "键值缓存用于减少数据访问的延迟。什么是读穿、写穿、写后、写回、写后和旁路缓存模式？"
categories: 系统设计
---

KV 缓存就像一个巨大的哈希映射，用于减少数据访问的延迟，通常通过

1. 将来自慢速且便宜介质的数据转移到快速且昂贵的介质上。
2. 从基于树的数据结构的 `O(log n)` 索引转为基于哈希的数据结构的 `O(1)` 进行读写。

有各种缓存策略，如读穿/写穿（或写回）和旁路缓存。总体而言，互联网服务的读写比为 100:1 到 1000:1，因此我们通常会优化读取。

在分布式系统中，我们根据业务需求和上下文选择这些策略，并在 [CAP 定理](https://puncsky.com/notes/2018-07-24-replica-and-consistency) 的指导下进行选择。

## 常规模式

* 读取
    * 读穿：客户端通过缓存层从数据库读取数据。当读取命中缓存时，缓存返回；否则，它从数据库获取数据，缓存后再返回值。
* 写入
    * 写穿：客户端写入缓存，缓存更新数据库。缓存在完成数据库写入后返回。
    * 写后 / 写回：客户端写入缓存，缓存立即返回。在缓存写入的背后，缓存异步写入数据库。
    * 绕过写入：客户端直接写入数据库，绕过缓存。

## 旁路缓存模式
当缓存不支持原生的读穿和写穿操作，并且资源需求不可预测时，我们使用这种旁路缓存模式。

* 读取：尝试命中缓存。如果未命中，则从数据库读取，然后更新缓存。
* 写入：先写入数据库，然后 ==删除缓存条目==。这里一个常见的陷阱是 [人们错误地用值更新缓存，而在高并发环境中双重写入会使缓存变脏](https://www.quora.com/Why-does-Facebook-use-delete-to-remove-the-key-value-pair-in-Memcached-instead-of-updating-the-Memcached-during-write-request-to-the-backend)。

==在这种模式下仍然存在缓存变脏的可能性。== 当满足以下两个条件时，会发生这种情况：

1. 读取数据库并更新缓存
2. 更新数据库并删除缓存

## 缓存放在哪里？

* 客户端
* 独立层
* 服务器端

## 如果数据量达到缓存容量怎么办？使用缓存替换策略
* LRU（最近最少使用）：检查时间，驱逐最近使用的条目，保留最近使用的条目。
* LFU（最不常用）：检查频率，驱逐最常用的条目，保留最常用的条目。
* ARC（自适应替换缓存）：其性能优于 LRU。通过同时保留最常用和频繁使用的条目，以及驱逐历史来实现。（保留 MRU + MFU + 驱逐历史。）

## 谁是缓存使用的王者？
[Facebook TAO](https://puncsky.com/notes/49-facebook-tao)