---
layout: post
title: "如何使用幂等性设计出高可靠的API？"
date: 2018-09-12 12:55
comments: true
categories: system design
language: zh-cn
abstract: 为什么API会不可靠？网络会出错，服务器会出错。解决这个问题的三个原则：客户端用“重试”来保证状态的一致性；重试的请求里要有幂等的唯一性ID；重试要负责任，比如遵循指数退避算法，因为不希望一大波客户端同时重试。 
references:
  - https://stripe.com/blog/idempotency
---

为什么API会不可靠？

1. 网络会出错
2. 服务器会出错


怎么解决这个问题呢？三个原则

1. 客户端用“重试”来保证状态的一致性


2. 重试的请求里要有==幂等的唯一性ID==

    1. 在 RESTful API 设计里面，PUT 和 DELETE 的语义本身是幂等的
    2. 但是 POST 在在线支付领域可能会导致==“重复付两次钱”的问题==，所以我们用“幂等的唯一性ID”来识别某个请求是否被发了多次
        1. 如果错误发生在到达服务器之前，重试过后，服务器第一次见到它，正常处理
        2. 如果错误发生在服务器，基于这个“唯一性ID”，用 ACID 的数据库保证这个事务只发生一次
        3. 如果错误发生在服务器返回结果之后，重试过后，服务器只需要返回缓存过的成功的结果


3. 重试要负责任，比如遵循==指数退避算法==，因为不希望一大波客户端同时重试。

举个例子，Stripe 的客户端是这样计算重试的等待时间的：

```ruby
def self.sleep_time(retry_count)
  # Apply exponential backoff with initial_network_retry_delay on the
  # number of attempts so far as inputs. Do not allow the number to exceed
  # max_network_retry_delay.
  sleep_seconds = [Stripe.initial_network_retry_delay * (2 ** (retry_count - 1)), Stripe.max_network_retry_delay].min

  # Apply some jitter by randomizing the value in the range of (sleep_seconds
  # / 2) to (sleep_seconds).
  sleep_seconds = sleep_seconds * (0.5 * (1 + rand()))

  # But never sleep less than the base sleep seconds.
  sleep_seconds = [Stripe.initial_network_retry_delay, sleep_seconds].max

  sleep_seconds
end
```
