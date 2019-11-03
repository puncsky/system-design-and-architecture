---
layout: post
title: "How to design robust and predictable APIs with idempotency?"
date: 2018-09-12 12:55
comments: true
categories: system design
language: en
references:
  - https://stripe.com/blog/idempotency
---

How could APIs be un-robust and un-predictable?

1. Networks are unreliable.
2. Servers are more reliable but may still fail.


How to solve the problem? 3 Principles:

1. Client retries to ensure consistency.


2. Retry with idempotency and idempotency keys to allow clients to pass a unique value.

    1. In RESTful APIs, the PUT and DELETE verbs are idempotent.
    2. However, POST may cause ==“double-charge” problem in payment==.  So we use a ==idempotency key== to identify the request.
        1. If the failure happens before the server, then there is a retry, and the server will see it for the first time, and process it normally.
        2. If the failure happens in the server, then ACID database will guarantee the transaction by the idempotency key.
        3. If the failure happens after the server’s reply, then client retries, and the server simply replies with a cached result of the successful operation.


3. Retry with ==exponential backoff and random jitter==. Be considerate of the ==thundering herd problem== that servers that may be stuck in a degraded state and a burst of retries may further hurt the system.

For example, Stripe’s client retry calculates the delay like this...

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
