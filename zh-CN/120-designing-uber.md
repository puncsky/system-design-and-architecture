---
slug: 120-designing-uber
id: 120-designing-uber
title: "设计 Uber"
date: 2019-01-03 18:39
comments: true
tags: [系统设计]
references:
   - https://medium.com/yalantis-mobile/uber-underlying-technologies-and-how-it-actually-works-526f55b37c6f
   - https://www.youtube.com/watch?t=116&v=vujVmugFsKc
   - http://www.infoq.com/news/2015/03/uber-realtime-market-platform
   - https://www.youtube.com/watch?v=kb-m2fasdDY&vl=en
---

免责声明：以下所有内容均来自公共来源或纯原创。这里没有 Uber 机密信息。

## 需求

* 针对全球交通市场的打车服务
* 大规模实时调度
* 后端设计

## 架构

![uber architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1546574738/web-guiguio/uber-architecture_2.jpg)

## 为什么选择微服务？
==康威定律== 表示软件系统的结构是组织结构的复制。

|  | 单体 ==服务== | 微服务 |
|--- |---  |--- |
|  小团队和代码库时的生产力 | ✅ 高  | ❌ 低 |
|  ==大团队和代码库时的生产力== | ❌ 低  |  ✅ 高 (康威定律) |
| ==对工程质量的要求== | ❌ 高 (不合格的开发人员容易导致系统崩溃) | ✅ 低 (运行时被隔离) |
| 依赖性提升 | ✅ 快 (集中管理) | ❌ 慢 |
| 多租户支持 / 生产-预发布隔离 | ✅ 简单 | ❌ 难 (每个独立服务必须 1) 构建连接到其他服务的预发布环境 2) 在请求上下文和数据存储中支持多租户) |
| 可调试性，假设相同模块、指标、日志 | ❌ 低 |  ✅ 高 (使用分布式追踪) |
| 延迟 |  ✅ 低 (本地) | ❌ 高 (远程) |
| DevOps 成本 | ✅ 低 (构建工具成本高) | ❌ 高 (容量规划困难) |

结合单体 ==代码库== 和微服务可以带来双方的好处。

## 调度服务

* 一致性哈希按地理哈希分片
* 数据是瞬态的，存在内存中，因此无需复制。(CAP: AP 优于 CP)
* 在分片中使用单线程或锁定匹配以防止双重调度

## 支付服务

==关键是采用异步设计==，因为支付系统通常在多个系统之间的 ACID 事务中具有非常长的延迟。

* 利用事件队列
* 支付网关与 Braintree、PayPal、Card.io、支付宝等集成
* 密集记录以跟踪所有内容
* [具有幂等性、指数退避和随机抖动的 API](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency)

## 用户资料服务和行程服务

* 低延迟与缓存
* 用户资料服务面临为越来越多类型的用户（司机、乘客、餐厅老板、吃货等）和不同地区和国家的用户架构提供服务的挑战。

## 推送通知服务

* 苹果推送通知服务（可靠性不高）
* 谷歌云消息服务 GCM （可以检测可送达性）或
* 短信服务通常更可靠