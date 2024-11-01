---
slug: 166-designing-payment-webhook
id: 166-designing-payment-webhook
title: "设计支付 webhook"
date: 2019-08-19 21:15
updateDate: 2024-04-06 17:29
comments: true
tags: [系统设计]
slides: false
description: 设计一个 webhook，当支付成功时通知商家。我们需要汇总指标（例如，成功与失败）并在仪表板上显示。
references:
  - https://commerce.coinbase.com/docs/#webhooks
  - https://bitworking.org/news/2017/03/prometheus
  - https://workos.com/blog/building-webhooks-into-your-application-guidelines-and-best-practices

---

## 1. 澄清需求

1. 一旦支付成功，webhook 将回调商家。
    1. 商家开发者向我们注册 webhook 信息。
    2. 可靠且安全地向 webhook 发起 POST HTTP 请求。
2. 高可用性、错误处理和故障恢复。
    1. 异步设计。假设商家的服务器分布在全球，可能会有高达 15 秒的延迟。
    2. 至少一次交付。幂等密钥。
    3. 顺序无关。
    4. 强大且可预测的重试和短路机制。
3. 安全性、可观察性和可扩展性。
    1. 防伪造。
    2. 当商家的接收器出现故障时通知商家。
    3. 易于扩展和规模化。

## 2. 概述高层设计

异步设计 + 重试 + 排队 + 可观察性 + 安全性

![](https://tp-misc.b-cdn.net/blockeden/designing-payment-webhook@2x.webp)

## 3. 功能和组件

### 核心功能

1. 用户访问仪表板前端向我们注册 webhook 信息 - 例如要调用的 URL、他们希望订阅的事件范围，然后从我们这里获取 API 密钥。
2. 当有新事件时，将其发布到队列中，然后被调用者消费。调用者获取注册信息并向外部服务发起 HTTP 调用。

### webhook 调用者

1. 订阅由支付状态机或其他服务发布的支付成功事件队列。

2. 一旦调用者接受事件，从用户设置服务获取 webhook URI、密钥和设置。根据这些设置准备请求。为了安全...

  * 所有来自用户设置的 webhook 必须使用 HTTPS。

  * 如果负载很大，预期延迟很高，并且我们希望确保目标接收器是活跃的，我们可以通过携带挑战的 ping 验证其存在。例如，[Dropbox 通过发送带有“challenge”参数（一个随机字符串）的 GET 请求来验证 webhook 端点](https://www.dropbox.com/developers/reference/webhooks#documentation)，您的端点需要将其回显作为响应。
  * 所有回调请求都带有头部 `x-webhook-signature`。这样接收者可以验证请求。
    * 对于对称签名，我们可以使用 HMAC/SHA256 签名。其值为 `HMAC(webhook secret, raw request payload);` Telegram 使用此方法。
    * 对于非对称签名，我们可以使用 RSA/SHA256 签名。其值为 `RSA(webhook private key, raw request payload);` Stripe 使用此方法。
    * 如果是敏感信息，我们还可以考虑对负载进行加密，而不仅仅是签名。

3. 向外部商家的端点发起带有事件负载和安全头的 HTTP POST 请求。

### API 定义

```json5
// POST https://example.com/webhook/
{
  "id": 1,
  "scheduled_for": "2017-01-31T20:50:02Z",
  "event": {
    "id": "24934862-d980-46cb-9402-43c81b0cdba6",
    "resource": "event",
    "type": "charge:created",
    "api_version": "2018-03-22",
    "created_at": "2017-01-31T20:49:02Z",
    "data": {
      "code": "66BEOV2A", // 或用户需要履行的订单 ID
      "name": "主权个体",
      "description": "掌握信息时代的过渡",
      "hosted_url": "https://commerce.coinbase.com/charges/66BEOV2A",
      "created_at": "2017-01-31T20:49:02Z",
      "expires_at": "2017-01-31T21:49:02Z",
      "metadata": {},
      "pricing_type": "CNY",
      "payments": [
        // ...
      ],
      "addresses": {
        // ...
      }
    }
  }
}
```

商家服务器应以 200 HTTP 状态码响应以确认收到 webhook。

### 错误处理

如果没有收到确认，我们将[使用幂等性密钥和指数退避重试，最长可达三天。最大重试间隔为 1 小时。](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency) 如果达到某个限制，则短路/标记为损坏。向商家发送电子邮件。

### 指标

Webhook 调用者服务将状态发射到时序数据库以获取指标。

使用 Statsd + Influx DB 还是 Prometheus？

* InfluxDB：应用程序将数据推送到 InfluxDB。它有一个用于指标和索引的单体数据库。
* Prometheus：Prometheus 服务器定期从运行的应用程序中拉取指标值。它使用 LevelDB 进行索引，但每个指标存储在自己的文件中。

或者如果您有宽裕的预算，可以使用昂贵的 DataDog 或其他 APM 服务。