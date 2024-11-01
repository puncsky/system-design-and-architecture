---
slug: 166-designing-payment-webhook
id: 166-designing-payment-webhook
layout: post
title: "Designing payment webhook"
date: 2019-08-19 21:15
updateDate: 2024-04-06 17:29
comments: true
tags: [system design]
slides: false
description: Design a webhook that notifies the merchant when the payment succeeds. We need to aggregate the metrics (e.g., success vs. failure) and display it on the dashboard.
references:
  - https://commerce.coinbase.com/docs/#webhooks
  - https://bitworking.org/news/2017/03/prometheus
  - https://workos.com/blog/building-webhooks-into-your-application-guidelines-and-best-practices

---

## 1. Clarifying Requirements

1. Webhook will call the merchant back once the payment succeeds.
    1. Merchant developer registers webhook information with us.
    2. Make a POST HTTP request to the webhooks reliably and securely.
2. High availability, error-handling, and failure-resilience.
    1. Async design. Assuming that the servers of merchants are located across the world, and may have a very high latency like 15s.
    2. At-least-once delivery. Idempotent key.
    3. Order does not matter.
    4. Robust & predictable retry and short-circuit.
3. Security, observability & scalability
    1. Anti-spoofing.
    2. Notify the merchant when their receivers are broken.
    3. easy to extend and scale.



## 2. Sketch out the high-level design

async design + retry + queuing + observability + security

![](https://tp-misc.b-cdn.net/blockeden/designing-payment-webhook@2x.webp)

## 3. Features and Components

### Core Features

1. Users go to dashboard frontend to register webhook information with us - like the URL to call, the scope of events they want to subscribe, and then get an API key from us.
2. When there is a new event, publish it into the queue and then get consumed by callers. Callers get the registration and make the HTTP call to external services.

###  Webhook callers

1. Subscribe to the event queue for payment success events published by a payment state machine or other services.

2. Once callers accept an event, fetch webhook URI, secret, and settings from the user settings service. Prepare the request based on those settings. For security...

  * All webhooks from user settings must be in HTTPs

  * If the payload is huge, the prospect latency is high, and we wants to make sure the target reciever is alive, we can verify its existance with a ping carrying a challenge. e.g. [Dropbox verifies webhook endpoints](https://www.dropbox.com/developers/reference/webhooks#documentation) by sending a GET request with a “challenge” param (a random string) encoded in the URL, which your endpoint is required to echo back as a response.
  * All callback requests are with header `x-webhook-signature`. So that the receiver can authenticate the request.
    * For symetric signature, we can use HMAC/SHA256 signature. Its value is `HMAC(webhook secret, raw request payload);`. Telegram takes this.
    * For asymmetric signature, we can use RSA/SHA256 signature. Its value is `RSA(webhook private key, raw request payload);` Stripe takes this.
    * If it's sensitive information, we can also consider encryption for the payload instead of just signing.

3. Make an HTTP POST request to the external merchant's endpoints with event payload and security headers.

### API Definition

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
      "code": "66BEOV2A", // or order ID the user need to fulfill
      "name": "The Sovereign Individual",
      "description": "Mastering the Transition to the Information Age",
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

The merchant server should respond with a 200 HTTP status code to acknowledge receipt of a webhook.

### Error-handling

If there is no acknowledgment of receipt, we will [retry with idempotency key and exponential backoff for up to three days. The maximum retry interval is 1 hour.](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency) If it's reaching a certain limit, short-circuit / mark it as broken. Sending out an Email to the merchant.

### Metrics

The Webhook callers service emits statuses into the time-series DB for metrics.

Using Statsd + Influx DB vs. Prometheus?

* InfluxDB: Application pushes data to InfluxDB. It has a monolithic DB for metrics and indices.
* Prometheus: Prometheus server pulls the metrics values from the running application periodically. It uses LevelDB for indices, but each metric is stored in its own file.

Or use the expensive DataDog or other APM services if you have a generous budget.
