---
layout: post
title: "Lambda Architecture"
date: 2018-10-23 10:30
comments: true
categories: system design
language: en
references:
  - https://www.amazon.com/Big-Data-Principles-practices-scalable/dp/1617290343
  - https://mapr.com/resources/stream-processing-mapr/
---

## Why lambda architecture?

To solve three problems introduced by big data

1. Accuracy  (好)
2. Latency (快)
3. Throughput (多)


e.g. problems with scaling a pageview service in a traditional way

1. You start with a traditional relational database.
2. Then adding a pub-sub queue.
3. Then scaling by horizontal partitioning or sharding
4. Fault-tolerance issues begin
5. Data corruption happens

The key point is that ==X-axis dimension alone of the [AKF scale cube](/notes/41-how-to-scale-a-web-service) is not good enough. We should introduce Y-axis / functional decomposition as well. Lambda architecture tells us how to do it for a data system.==



## What is lambda architecture?

If we define a data system as

```txt
Query = function(all data)
```


Then a lambda architecture is

![Lambda Architecture](/img/lambda-architecture.png)


```txt
batch view = function(all data at the batching job's execution time)
realtime view = function(realtime view, new data)

query = function(batch view. realtime view)
```

==Lambda architecture = CQRS (batch layer + serving layer) + speed layer==


![Lambda Architecture for big data systems](https://res.cloudinary.com/dohtidfqh/image/upload/v1548840018/web-guiguio/lambda-architecture-for-big-data-systems.png)
