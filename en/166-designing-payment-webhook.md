---
layout: post
title: "Designing payment webhook"
date: 2019-08-19 21:15
comments: true
categories: system design
language: en
slides: false
abstract: Design a webhook that notifies the merchant when the payment succeeds. We need to aggregate the metrics (e.g., success vs. failure) and display it on the dashboard.
references:
  - https://commerce.coinbase.com/docs/#webhooks
  - https://bitworking.org/news/2017/03/prometheus 
---

## 1. Clarifying Requirements

1. Webhook to callback the merchant once the payment succeeds.
2. Analytics & metrics.
3. High availability & Failure-resilience.
    1. Async design. Assuming that the servers of merchants are located across the world, and may have a very high latency like 15s. 
    2. At-least-once delivery. 
    3. Robust & predicable retry.
4. Security: informing the merchants whether a payment succeeds involves real money real transactions, and thus, security is always a concern.


## 2. Sketch out the high-level design
async design + retry + queuing + time-series DB + security

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" height="100%" viewBox="-0.5 -0.5 510 371" content="&lt;mxfile modified=&quot;2019-08-20T04:35:16.956Z&quot; host=&quot;www.draw.io&quot; agent=&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36&quot; etag=&quot;WewxEXrpT1taWR3_cU0F&quot; version=&quot;11.1.5&quot; type=&quot;google&quot; pages=&quot;1&quot;&gt;&lt;diagram id=&quot;PbWMpdjEXtuSdh0sNvo9&quot; name=&quot;Page-1&quot;&gt;1Vldd5s4EP01fowP5sv2Y7Fdt3vSTTfZnk2e9giQQRtAXiH80V+/EhYGWdjBDQRvH1I0SLK4d+bODAyMWbxbErAOv2EfRgNd83cDYz7Q9fHEZn+5YX8wjDTLOlgCgnxhKw1P6CcsJgprhnyYShMpxhFFa9no4SSBHpVsgBC8laetcCT/6hoEUDE8eSBSrX8hn4YH68TSSvsXiIKw+OWRJu7EoJgsDGkIfLytmIzFwJgRjOnhKt7NYMTBK3A5rPt85u7xYAQmtMmCB+gYONU22Q/H/u35y/J3x9Hv9MMuGxBl4oG/QeKFIKEpM+MNJOy/rwmFJIFUPAfdF+CENI7Y1WhgOGwmRQy2e+DC6DtOEUU4YfdcTCmO2QQQoYAbPMh3Y4aIz3SA9xoQnCX+DEeY5Nsaq/xfZdNPYi3Fa2ZNKcGvRzZ0bimg1djAB2kIfTFgd9b8sPEu4P45RDgdDxFzlnToRThj0xwVRwEt/3W4q5gErkuIY0jJnk0Rd6eC4sLJx2K8LT2mMIUVZzGFDQgfDY4blzSyC8HkFawaCqsKdQUw3j5CiZ8Tsg0RhU9r4HH7lsHFbBWGXc4S9O/do+HI3UNG2S5Q2AmmQLA/1doB2LBlhPUahO0ahCddITx+G2HoMyERQ0xoiAOcgGhRWh1yQFS4ajnnHnM/z7H8B1K6F6oIMoplSs4im+KMePDC+U0hpYAEkL6tD/xZLvJEYMQ438ii2Trqkz5AhjtEnyvXL3yroSVG853YOR/si0HCHve5nMiHL8UefFAuy0fFuu4JNW6K0JGaf9LMTT2CXMhPuYF5IjohnYkGlTkiMEU/gZtP4DiuMeIL2WzLGVjzuvRzmlti5Pu5wzTISypNl9xVkbljtSJOLBUEdfJ3pw010zQlCRRENuZJbP6dI1OZglerVGT2KpHHM7yDW00h7gOjtYzQl8qd66JV6z1arb6iNfybPCwmy0/G47+P0+Vskc32r0UyuAVCtYaESnSW7F4k9ATt1hiuxbRXQi1FfflhWVUF3RDjV3b14/HrQJ/xB4Ye4ff4NUj83EIpSoKblefGsisTfN7zL8mzaY2mkjzfjd6nzzt5G7HrWF7fnXibimccfcKOOLsuawztgF8FgMIt2CtuIEf+G83F2UBr3iMc2Sy6MFu49xtdmNVVj6BG158ohncpJAjy7nruKJh12JW1grAlIdx7FzbtNSG10A90V2HYDSuMG+sHCp8sY2aduRFKw/9/NzC9Mi1d7AbGmv2+/NJ9CrFVKsE+5hgpKSSlLIcM+DtTL+SK1XcqMSenqUQVummN0NktCF1t/WH2KnQf1kpdW3mfr6gbVN7GBwndpUNWgiNL83ftZ6vqX4iBGqlRAD3/ytWQY2BSEwKWGgJtvNM+T1dv77TbANQaD+X6aWTqQ7VGNeu+FFgdoTq+HWG53NK3KBBNSyOrT4FQs+ccpKGLAfF7lwZ9JPuxOVK1YdLR965asCYKWItNXmhof2QwU+sJtWQ8fFMsqrsE88B3ViiKTkzNC8c6GmSi2tAUW2bCsFQm6vREv54JNiy/VR9qxPKLv7H4Dw==&lt;/diagram&gt;&lt;/mxfile&gt;" style="background-color: rgb(255, 255, 255);"><defs/><g><path d="M 90.02 130 C 95.26 129.32 99.01 124.15 98.38 118.46 C 97.75 112.76 92.98 108.7 87.74 109.39 C 87.68 100.88 82.18 93.56 74.52 91.78 C 66.86 90 59.08 94.23 55.81 101.96 C 53.39 98.96 49.55 97.83 46.06 99.09 C 42.58 100.35 40.13 103.76 39.85 107.74 C 34.19 107.51 29.42 112.31 29.21 118.46 C 29 124.6 33.43 129.77 39.09 130 Z" fill="#ffffff" stroke="#000000" stroke-width="2" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5,137.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="127" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; white-space: nowrap; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;background-color:#ffffff;">Merchants over Internet</div></div></foreignObject><text x="64" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Merchants over Internet</text></switch></g><path d="M 299 206 C 299 184.67 359 184.67 359 206 L 359 254 C 359 275.33 299 275.33 299 254 Z" fill="#ffffff" stroke="#000000" stroke-miterlimit="10" transform="rotate(90,329,230)" pointer-events="none"/><path d="M 299 206 C 299 222 359 222 359 206" fill="none" stroke="#000000" stroke-miterlimit="10" transform="rotate(90,329,230)" pointer-events="none"/><path d="M 159 110 L 105.37 110" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 100.12 110 L 107.12 106.5 L 105.37 110 L 107.12 113.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 229 110 L 259 110 L 259 230 L 282.63 230" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 287.88 230 L 280.88 233.5 L 282.63 230 L 280.88 226.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(217.5,160.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="90" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; white-space: nowrap; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;background-color:#ffffff;">subscribe events</div></div></foreignObject><text x="45" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">subscribe events</text></switch></g><path d="M 194 135 L 194 183.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 194 188.88 L 190.5 181.88 L 194 183.63 L 197.5 181.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 194 85 L 194 20 L 262.63 20" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 267.88 20 L 260.88 23.5 L 262.63 20 L 260.88 16.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(92.5,48.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="203" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; white-space: nowrap; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;background-color:#ffffff;">get webhook URI, secret, and settings</div></div></foreignObject><text x="102" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">get webhook URI, secret, and settings</text></switch></g><rect x="159" y="85" width="70" height="50" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(169.5,96.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="48" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 50px; white-space: nowrap; overflow-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;white-space:normal;">webhook<br />gateway</div></div></foreignObject><text x="24" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">webhook&lt;br&gt;gateway</text></switch></g><path d="M 164 206 C 164 184.67 224 184.67 224 206 L 224 254 C 224 275.33 164 275.33 164 254 Z" fill="#ffffff" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 164 206 C 164 222 224 222 224 206" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(165.5,228.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="56" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 56px; white-space: nowrap; overflow-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;white-space:normal;">Time-series DB</div></div></foreignObject><text x="28" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Time-series DB</text></switch></g><path d="M 419 110 L 394 110 L 394 230 L 375.37 230" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 370.12 230 L 377.12 226.5 L 375.37 230 L 377.12 233.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(355.5,158.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="77" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; white-space: nowrap; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;background-color:#ffffff;">publish events</div></div></foreignObject><text x="39" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">publish events</text></switch></g><rect x="419" y="80" width="90" height="60" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(426.5,96.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="74" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 76px; white-space: nowrap; overflow-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;white-space:normal;">payment<br />state machine</div></div></foreignObject><text x="37" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">payment&lt;br&gt;state machine</text></switch></g><path d="M 317 40 L 317 56.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 317 61.88 L 313.5 54.88 L 317 56.63 L 320.5 54.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="269" y="0" width="95" height="40" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(281.5,13.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="69" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 69px; white-space: nowrap; overflow-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;white-space:normal;">user settings</div></div></foreignObject><text x="35" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">user settings</text></switch></g><path d="M 296.5 71.5 C 296.5 59.5 336.5 59.5 336.5 71.5 L 336.5 98.5 C 336.5 110.5 296.5 110.5 296.5 98.5 Z" fill="#ffffff" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 296.5 71.5 C 296.5 80.5 336.5 80.5 336.5 71.5" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 194 330 L 194 276.37" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><path d="M 194 271.12 L 197.5 278.12 L 194 276.37 L 190.5 278.12 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="none"/><rect x="154" y="330" width="80" height="40" fill="#ffffff" stroke="#000000" pointer-events="none"/><g transform="translate(164.5,343.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="58" height="12" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 60px; white-space: nowrap; overflow-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;white-space:normal;">Dashboard</div></div></foreignObject><text x="29" y="12" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Dashboard</text></switch></g><g transform="translate(304.5,266.5)"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="38" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 38px; white-space: nowrap; overflow-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;white-space:normal;">Event Queue</div></div></foreignObject><text x="19" y="19" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">Event Queue</text></switch></g></g></svg>


## 3. Features and Components

###  Webhook Gateway

1. Subscribe to the event queue for payment success events published by a payment state machine or other services.
2. Once accept an event, fetch webhook URI, secret, and settings from the user settings service. Prepare the request based on those settings.
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

If there is no acknowledgment of receipt, we will [retry with exponential backoff for up to three days. The maximum retry interval is 1 hour.](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency) 

#### Security

* All webhooks from user settings must be in https
* All callback requests are with header `x-webhook-signature` SHA256 HMAC signature. Its value is `HMAC(webhook secret, raw request payload);`. We generate the secret for the developer to use.

> Background Knowledge: HMAC (message authentication code).
> A short piece of information used to authenticate a message — In other words, to confirm that the message came from the stated sender (its authenticity) and has not been changed in transit (its integrity). The integrity can be verified by the shared secret between trusted parties against the digest of the original message.



### Metrics

The webhook gateway service emits statuses into the time-series DB for metrics.  

Using Influx DB vs. Prometheus?

* InfluxDB: Application pushes data to InfluxDB. It has a monolithic DB for metrics and indices.
* Prometheus: Prometheus server pulls the metrics values from the running application periodically. It uses LevelDB for indices, but each metric is stored in its own file.

I will probably choose InfluxDB for easier maintenance of the monolithic data store.

Depending on how much further data aggregation we need, we can build more advanced data pipeline. However, for just counting success/ failures, a simple time-series DB solves the problem.

