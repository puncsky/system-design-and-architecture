---
slug: 177-designing-Airbnb-or-a-hotel-booking-system
id: 177-designing-Airbnb-or-a-hotel-booking-system
layout: post
title: "设计 Airbnb 或酒店预订系统"
date: 2019-10-06 01:39
comments: true
slides: false
categories: 系统设计
language: cn
abstract: 对于客人和房东，我们使用关系数据库存储数据，并建立索引以按位置、元数据和可用性进行搜索。我们可以使用外部供应商进行支付，并通过优先队列提醒预订。
references:
  - https://www.vertabelo.com/blog/designing-a-data-model-for-a-hotel-room-booking-system/
---

## 需求
* 对于客人
    * 按位置、日期、房间数量和客人数量搜索房间
    * 获取房间详情（如图片、名称、评论、地址等）和价格
    * 按日期和房间 ID 从库存中支付并预订房间
        * 作为访客结账 
        * 用户已登录
    * 通过电子邮件和移动推送通知进行通知
* 对于酒店或租赁管理员（供应商/房东）
    * 管理员（接待员/经理/租赁所有者）：管理房间库存并帮助客人办理入住和退房
    * 清洁工：定期清理房间

## 架构

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1570439920/web-guiguio/hotel-booking-system_2.png)

## 组件

### 库存 \<\> 预订 \<\> 用户（客人和房东）

供应商在库存中提供他们的房间详情。用户可以相应地搜索、获取和预订房间。在预订房间后，用户的付款也会更改 `reserved_room` 的 `status`。您可以在 [这篇文章](https://www.vertabelo.com/blog/designing-a-data-model-for-a-hotel-room-booking-system/) 中查看数据模型。

### 如何查找可用房间？

* 按位置：使用 [空间索引](https://en.wikipedia.org/wiki/Spatial_database) 进行地理搜索，例如 geo-hash 或四叉树。
* 按房间元数据：在查询数据库时应用过滤器或搜索条件。
* 按入住和退房日期及可用性。两种选择：
    * 选项 1：对于给定的 `room_id`，检查今天或更晚的所有 `occupied_room`，将数据结构转换为按天的占用数组，最后在数组中找到可用的时间段。这个过程可能会耗时，因此我们可以建立可用性索引。
    * 选项 2：对于给定的 `room_id`，始终为占用的日期创建一个条目。这样更容易按日期查询不可用的时间段。

### 对于酒店，同步数据

如果这是一个酒店预订系统，那么它可能会发布到 GDS、聚合器和批发商等预订渠道。

![酒店预订生态系统](https://res.cloudinary.com/dohtidfqh/image/upload/v1570439485/web-guiguio/scheme.png)

为了在这些地方同步数据，我们可以

1. [使用幂等性重试来提高外部调用的成功率，并确保没有重复订单](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency)。
2. 向外部供应商提供 webhook 回调 API，以在内部系统中更新状态。

### 支付与记账

数据模型：[复式记账](https://puncsky.com/notes/167-designing-paypal-money-transfer#payment-service)

为了执行支付，由于我们调用外部支付网关，如银行或 Stripe、Braintree 等，保持不同地方的数据同步至关重要。[我们需要在交易表和外部银行及供应商之间同步数据。](https://puncsky.com/#how-to-sync-across-the-transaction-table-and-external-banks-and-vendors)

### 提醒/警报的通知者

通知系统本质上是一个延迟调度器（优先队列 + 订阅者）加上 API 集成。

例如，每日定时任务将查询数据库以获取今天要发送的通知，并按日期将其放入优先队列。订阅者将从优先队列中获取最早的通知，并在达到预期时间戳时发送。如果没有，则将任务放回队列，并让 CPU 空闲以进行其他工作，如果今天有新的警报添加，可以中断此过程。