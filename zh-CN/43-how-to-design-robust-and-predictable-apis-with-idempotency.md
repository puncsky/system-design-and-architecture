---
slug: 43-how-to-design-robust-and-predictable-apis-with-idempotency
id: 43-how-to-design-robust-and-predictable-apis-with-idempotency
layout: post
title: "如何设计健壮且可预测的 API 以实现幂等性？"
date: 2018-09-12 12:55
comments: true
tags: [系统设计]
description: "API 可能不够健壮且不可预测。为了解决这个问题，应遵循三个原则。客户端重试以确保一致性。使用幂等性、指数退避和随机抖动进行重试。"
references:
  - https://stripe.com/blog/idempotency
---

API 如何可能不够健壮且不可预测？

1. 网络不可靠。
2. 服务器更可靠，但仍可能出现故障。

如何解决这个问题？三个原则：

1. 客户端重试以确保一致性。

2. 使用幂等性和幂等性键进行重试，以允许客户端传递唯一值。

    1. 在 RESTful API 中，PUT 和 DELETE 动词是幂等的。
    2. 然而，POST 可能导致==“双重收费”问题==。因此，我们使用==幂等性键==来识别请求。
        1. 如果故障发生在服务器之前，则会进行重试，服务器将首次看到该请求，并正常处理。
        2. 如果故障发生在服务器中，则 ACID 数据库将通过幂等性键保证事务。
        3. 如果故障发生在服务器回复之后，则客户端重试，服务器简单地回复成功操作的缓存结果。

3. 使用==指数退避和随机抖动==进行重试。要考虑==雷鸣般的群体问题==，即服务器可能处于降级状态，突发的重试可能会进一步损害系统。

例如，Stripe 的客户端重试计算延迟如下...

```ruby
def self.sleep_time(retry_count)
  # 根据到目前为止的尝试次数应用初始网络重试延迟的指数退避。不要让这个数字超过最大网络重试延迟。
  sleep_seconds = [Stripe.initial_network_retry_delay * (2 ** (retry_count - 1)), Stripe.max_network_retry_delay].min

  # 通过在 (sleep_seconds / 2) 到 (sleep_seconds) 范围内随机化值来应用一些抖动。
  sleep_seconds = sleep_seconds * (0.5 * (1 + rand()))

  # 但永远不要少于基础睡眠秒数。
  sleep_seconds = [Stripe.initial_network_retry_delay, sleep_seconds].max

  sleep_seconds
end
```