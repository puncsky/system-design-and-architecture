---
slug: 2018-07-26-acid-vs-base
id: 2018-07-26-acid-vs-base
layout: post
title: "ACID vs BASE"
date: 2018-07-26 11:54
comments: true
categories: system design
language: zh
abstract: "ACID 和 BASE 代表了不同的设计理念。ACID 更注重一致性而非可用性。在 ACID 中，C 表示事务保留所有数据库规则。而 BASE 更侧重于可用性，表示系统确保可用。"
references:
    - https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed
---

ACID（一致性优先于可用性）

- 原子性确保事务要么完全成功，要么完全失败。
- 一致性：在 ACID 中，C 表示事务保留所有数据库规则，如唯一键、触发器、级联等。相比之下，CAP 中的 C 仅指单一副本一致性，是 ACID 一致性的严格子集。
- 隔离性确保并发执行的事务使数据库保持在与顺序执行事务相同的状态。
- 持久性确保一旦事务提交，即使在系统故障（如断电或崩溃）情况下也会保持提交状态。

BASE（可用性优先于一致性）

- 基本可用表示系统确保可用。
- 软状态表示系统的状态可能随时间变化，即使没有输入。这主要是由于最终一致性模型导致的。
- 最终一致性表示只要系统在一定时间内不接收输入，系统最终将达到一致状态。

虽然大多数 NoSQL 采用 BASE 原则，但它们正逐渐学习或转向 ACID，例如，Google Spanner 提供强一致性，MongoDB 4.0 增加了对多文档 ACID 事务的支持。
