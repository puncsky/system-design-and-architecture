---
slug: 85-improving-availability-with-failover
id: 85-improving-availability-with-failover
layout: post
title: "通过故障转移提高可用性"
date: 2018-10-26 12:02
comments: true
tags: [系统设计]
description: 为了通过故障转移提高可用性，有几种方法可以实现这一目标，例如冷备份、热备份、温备份、检查点和全活动。
references:
  - https://www.ibm.com/developerworks/community/blogs/RohitShetty/entry/high_availability_cold_warm_hot
---

冷备份：使用心跳或指标/警报来跟踪故障。当发生故障时，配置新的备用节点。仅适用于无状态服务。

热备份：保持两个活动系统承担相同的角色。数据几乎实时镜像，两个系统将拥有相同的数据。

温备份：保持两个活动系统，但第二个系统在故障发生之前不接收流量。

检查点（或类似于 Redis 快照）：使用预写日志（WAL）在处理之前记录请求。备用节点在故障转移期间从日志中恢复。

* 缺点
  * 对于大型日志来说耗时较长
  * 自上次检查点以来丢失数据
* 使用案例：Storm、WhillWheel、Samza

主动-主动（或全活动）：在负载均衡器后保持两个活动系统。它们并行处理。数据复制是双向的。