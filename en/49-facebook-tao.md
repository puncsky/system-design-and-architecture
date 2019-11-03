---
layout: post
title: "How Facebook Scale its Social Graph Store? TAO"
date: 2018-09-18 22:50
comments: true
categories: system design
language: en
references:
  - http://www.cs.cornell.edu/courses/cs6410/2015fa/slides/tao_atc.pptx
  - https://cs.stanford.edu/~matei/courses/2015/6.S897/slides/tao.pdf
  - https://www.facebook.com/notes/facebook-engineering/tao-the-power-of-the-graph/10151525983993920/
---

## What are the challenges?

Before TAO, use cache-aside pattern

![Before TAO](https://puncsky.com/img/tao-before.png)

Social graph data is stored in MySQL and cached in Memcached


3 problems:

1. list update operation in Memcached is inefficient. cannot append but update the whole list.
2. clients have to manage cache
3. Hard to offer ==read-after-write consistency==


To solve those problems, we have 3 goals:

- online data graph service that is efficiency at scale
- optimize for read (its read-to-write ratio is 500:1)
	- low read latency
	- high read availability (eventual consistency)
- timeliness of writes (read-after-write)



## Data Model

- Objects (e.g. user, location, comment) with unique IDs
- Associations (e.g. tagged, like, author) between two IDs
- Both have key-value data as well as a time field



## Solutions: TAO

1. Efficiency at scale and reduce read latency
	- graph-specific caching
	- a standalone cache layer between the stateless service layer and the DB layer (aka [Functional Decomposition](/notes/41-how-to-scale-a-web-service))
	- subdivide data centers (aka [Horizontal Data Partitioning](/notes/41-how-to-scale-a-web-service))


2. Write timeliness
	- write-through cache
    - follower/leader cache to solve thundering herd problem
	- async replication


3. Read availability
	- Read Failover to alternate data sources



## TAO's Architecture

- MySQL databases → durability
- Leader cache → coordinates writes to each object
- Follower caches → serve reads but not writes. forward all writes to leader.


![Facebook TAO Architecture](https://puncsky.com/img/tao-architecture.png)


Read failover

![Facebook TAO Read Failover](https://puncsky.com/img/tao-read-failover.png)
