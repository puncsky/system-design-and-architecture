---
slug: 2018-07-10-cloud-design-patterns
id: 2018-07-10-cloud-design-patterns
title: "云设计模式"
date: 2018-07-10 11:16
comments: true
tags: [design patterns, system design]
description: "云设计模式分为三类。可用性模式包括健康端点监控和限流。数据管理模式包括缓存旁路和静态内容托管。安全模式包括联邦身份认证。"
references:
  - https://docs.microsoft.com/en-us/azure/architecture/patterns/
---

## 可用性模式
  - 健康端点监控（Health Endpoint Monitoring）：在应用中实现功能性检查，外部工具可以通过暴露的端点定期访问。
  - 基于队列的负载平衡（Queue-Based Load Leveling）：在任务和它调用的服务之间使用队列作为缓冲，平滑间歇性的高负载。
  - 限流（Throttling）：控制单个应用实例、单个租户或整个服务所消耗的资源。



## 数据管理模式
  - 缓存旁路（Cache-Aside）：按需从数据存储加载数据到缓存
  - 命令查询职责分离（CQRS）：通过分离的接口将读取数据的操作与更新数据的操作分开。
  - 事件溯源（Event Sourcing）：使用只追加的存储来记录描述领域内对数据采取的操作的完整事件序列。
  - 索引表（Index Table）：在数据存储中频繁被查询引用的字段上创建索引。
  - 物化视图（Materialized View）：当数据未以适合所需查询操作的格式存在时，在一个或多个数据存储上生成预填充的视图。
  - 分片（Sharding）：将数据存储划分为一组水平分区或分片。
  - 静态内容托管（Static Content Hosting）：将静态内容部署到基于云的存储服务，能直接交付给客户端。



## 安全模式
  - 联邦身份认证（Federated Identity）：将认证委托给外部身份提供者。
  - 守门人模式（Gatekeeper）：使用专用的主机实例作为客户端和应用或服务之间的代理来保护应用和服务，验证和清理请求，并在两者之间传递请求和数据。
  - 代客钥匙模式（Valet Key）：使用 token 或 key 为客户端提供对特定资源或服务的受限直接访问。
