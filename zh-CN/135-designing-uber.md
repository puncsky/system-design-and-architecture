---
layout: post
title: "设计优步打车服务"
date: 2019-02-08 22:18
comments: true
categories: system design
abstract: 优步打车设计的要求：为全球的交通运输市场提供服务；大规模的实时调度；后端设计；优步打车设计流程：架构；微服务；调度服务；支付服务；用户档案服务和行程记录服务、通知推送服务。
language: zh-cn
references:
   - https://medium.com/yalantis-mobile/uber-underlying-technologies-and-how-it-actually-works-526f55b37c6f
   - https://www.youtube.com/watch?t=116&v=vujVmugFsKc
   - http://www.infoq.com/news/2015/03/uber-realtime-market-platform
   - https://www.evernote.com/shard/s75/res/3915a501-e697-430b-877a-b5a06a167abc
   - https://www.youtube.com/watch?v=kb-m2fasdDY&vl=en
---

免责声明：以下所有内容均来自公共资源或纯粹原创。 这里不包含优步的涉密内容。

## 要求

* 为全球的交通运输市场提供服务
* 大规模的实时调度
* 后端设计



## 架构

![uber architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1546574738/web-guiguio/uber-architecture_2.jpg)



## 为何要微服务？
==Conway定律== 软件的系统结构会对应企业的组织结构。

|  | 单体 ==服务== | 微服务 |
|--- |---  |--- |
|  当团队规模和代码库很小时，生产力 | ✅ 高  | ❌ 低 |
|  ==当团队规模和代码库很大时，生产力== | ❌ 低  |  ✅ 高 (Conway定律) |
| ==对工程质量的要求== | ❌ 高 (能力不够的开发人员很容易破坏整个系统) | ✅ 低 (运行时是隔离的) |
| dependency 版本升级 | ✅ 快 (集中管理) | ❌ 慢 |
| 多租户支持 / 生产-staging状态隔离 | ✅ 容易 | ❌ 困难 (每项服务必须 1) 要么建立一个staging环境连接到其他处于staging状态的服务 2) 要么跨请求上下文和数据存储的多租户支持) |
| 可调试性，假设相同的模块，参数，日志 | ❌ 低 |  ✅ 高 (如果有分布式tracing) |
| 延迟 |  ✅ 低 (本地) | ❌ 高 (远程) |
| DevOps成本 | ✅ 低 (构建工具成本高) | ❌ 高 (容量规划很难) |

结合单体 ==代码库== 和微服务可以同时利用两者的长处.

## 调度服务

* 由geohash提供一致的哈希地址
* 数据在内存中是瞬态的，因此不需要复制. (CAP: AP高于CP)
* 分片中使用单线程或者锁，以防止双重调度



## 支付服务

==关键是要有异步设计==, 因为跨多个系统的ACID交易支付系统通常具有非常长的延迟.

* 利用事件队列
* 支付接口集成 Braintree, PayPal, Card.io, Alipay 等
* 通过详尽的 log 来记录所有 event
* [使用具有等幂性、指数退避和随机抖动的API](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency)


## 用户档案服务和行程记录服务

* 使用缓存降低延迟
* 随着 1) 支持更多的国家和地区 2) 用户角色（司机，骑手，餐馆老板，食客等）逐渐增加，为这些用户提供用户档案服务也面临着巨大的挑战。

## 通知推送服务

* 苹果通知推送服务 (不可靠)
* 谷歌云消息服务GCM （它可以检测到是否成功递送) 或者
* 短信服务通常更可靠
