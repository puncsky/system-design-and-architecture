---
layout: post
title: "Designing Uber"
date: 2019-01-03 18:39
comments: true
categories: system design
language: en
references:
   - https://medium.com/yalantis-mobile/uber-underlying-technologies-and-how-it-actually-works-526f55b37c6f
   - https://www.youtube.com/watch?t=116&v=vujVmugFsKc
   - http://www.infoq.com/news/2015/03/uber-realtime-market-platform
   - https://www.evernote.com/shard/s75/res/3915a501-e697-430b-877a-b5a06a167abc
   - https://www.youtube.com/watch?v=kb-m2fasdDY&vl=en
---

Disclaimer: All things below are collected from public sources or purely original. No Uber-confidential stuff here.

## Requirements

* ride hailing service targeting the transportation markets around the world
* realtime dispatch in massive scale
* backend design



## Architecture

![uber architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1546574738/web-guiguio/uber-architecture_2.jpg)



## Why micro services?
==Conway's law== says structures of software systems are copies of the organization structures.

|  | Monolithic ==Service== | Micro Services |
|--- |---  |--- |
|  Productivity, when teams and codebases are small | ✅ High  | ❌ Low |
|  ==Productivity, when teams and codebases are large== | ❌ Low  |  ✅ High (Conway's law) |
| ==Requirements on Engineering Quality== | ❌ High (under-qualified devs break down the system easily) | ✅ Low (runtimes are segregated) |
| Dependency Bump | ✅ Fast (centrally managed) | ❌ Slow |
| Multi-tenancy support / Production-staging Segregation | ✅ Easy | ❌ Hard (each individual service has to either 1) build staging env connected to others in staging 2) Multi-tenancy support across the request contexts and data storage) |
| Debuggability, assuming same modules, metrics, logs | ❌ Low |  ✅ High (w/ distributed tracing) |
| Latency |  ✅ Low (local) | ❌ High (remote) |
| DevOps Costs | ✅ Low (High on building tools) | ❌ High (capacity planning is hard) |

Combining monolithic ==codebase== and micro services can bring benefits from both sides.

## Dispatch Service

* consistent hashing sharded by geohash
* data is transient, in memory, and thus there is no need to replicate. (CAP: AP over CP)
* single-threaded or locked matching in a shard to prevent double dispatching



## Payment Service

==The key is to have an async design==, because payment systems usually have a very long latency for ACID transactions across multiple systems.

* leverage event queues
* payment gateway w/ Braintree, PayPal, Card.io, Alipay, etc.
* logging intensively to track everything
* [APIs with idempotency, exponential backoff, and random jitter](https://puncsky.com/notes/43-how-to-design-robust-and-predictable-apis-with-idempotency)


## UserProfile Service and Trip Service

* low latency with caching
* UserProfile Service has the challenge to serve users in increasing types (driver, rider, restaurant owner, eater, etc) and user schemas in different regions and countries.

## Push Notification Service

* Apple Push Notifications Service (not quite reliable)
* Google Cloud Messaging Service GCM （it can detect the deliverability) or
* SMS service is usually more reliable
