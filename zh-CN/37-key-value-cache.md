---
layout: post
title: "键值缓存有哪些用法？"
date: 2018-09-06 21:32
comments: true
categories: system design
language: zh-cn
abstract: Key Value Cache的本质是为了减少访问数据的延迟。Cache设计的常见策略有read-through/write-through和cache aside.具体的策略要根据你的业务需求具体选择。
references:
  - https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf
  - https://coolshell.cn/articles/17416.html
  - https://msdn.microsoft.com/en-us/library/dn589799.aspx
---

KV Cache的本质是为了减少访问数据的延迟。比如，把存在又贵又慢的媒体上的数据库的`O(logN)`的读写和复杂的查询，变成存在又快又贵的媒体上的
`O(1)`的读写。cache 的设计有很多策略，常见的有 read-through/write-through(or write-back) 和 cache aside.

常见的互联网服务读写比是 100:1 到 1000:1，我们常常对读做优化。

在分布式系统中，这些 pattern 的组合都是 consistency, availability, partition tolerance 之间的 trade-off，要根据你的业务需求具体
选择。

## 一般的策略

- 读
    - Read-through: clients 和 databases 之间加一层 cache layer，clients 不直接访问数据库，clients 通过 cache 间接访问数据库。
读的时候 cache 里面没有东西则从database更新再返回，有则直接返回。
- 写
    - Write-through: clients 先写数据到 cache，cache 更新 database，只有 database 最终更新了，操作才算完成。
    - write-behind/Write-back: clients 先写数据到 cache，先返回。回头将 cache 异步更新到 database. 一般来讲 write-back 是最快的
    - Write-around: client 写的时候绕过 cache 直接写数据库。

## cache aside pattern

Cache 不支持 read-through 和 write-through/write-behind 的时候用 Cache aside pattern

读数据? 命中 cache 读 cache，没命中 cache 读 database 存 cache
改数据? 先改 database，后删除 cache entry

[为什么不是写完数据库后更新缓存？](https://www.quora.com/Why-does-Facebook-use-delete-to-remove-the-key-value-pair-in-Memcached-instead-of-updating-the-Memcached-during-write-request-to-the-backend)主要是怕两个并发的 database 写操作导致两个并发的 cache 更新导致脏数据。

是不是Cache Aside这个就不会有并发问题了？还是有很低的概率有可能发生脏数据，就是一边读 database 并更新 cache 的时候，一边更新 database 并删除 cache entry

## 缓存放在哪？

- client side,
- distinct layer
- server side

## 缓存大小不够用的话怎么办？缓存回收策略(cache replacement policies)

- LRU - least-recently used 看时间，只保留最近时间使用的，回收最近时间没使用的
- LFU - least-frequently used 看次数，只保留使用次数最多的，回收使用次数最少的
- ARC 性能比LRU好，大致做法是既保持 RU，又保持 FU，还记录了最近回收的历史。

## 缓存用起来谁家强？

<a target="_blank" href="https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf">Facebook TAO</a>
