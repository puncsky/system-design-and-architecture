---
layout: post
title: "Designing a URL shortener"
date: 2018-10-25 14:32
comments: true
categories: system design
language: en
---

Design a system to take user-provided URLs and transform them to a shortened URLs that redirect back to the original. Describe how the system works. How would you allocate the shorthand URLs? How would you store the shorthand to original URL mapping? How would you implement the redirect servers? How would you store the click stats?

Assumptions: I generally don't include these assumptions in the initial problem presentation. Good candidates will ask about scale when coming up with a design.

- Total number of unique domains registering redirect URLs is on the order of 10s of thousands
- New URL registrations are on the order of 10,000,000/day (100/sec)
- Redirect requests are on the order of 10B/day (100,000/sec)
- Remind candidates that those are average numbers - during peak traffic (either driven by time, such as 'as people come home from work' or by outside events, such as 'during the Superbowl') they may be much higher.
- Recent stats (within the current day) should be aggregated and available with a 5 minute lag time
- Long look-back stats can be computed daily

## Assumptions

1B new URLs per day, 100B entries in total
the shorter, the better
show statics (real-time and daily/monthly/yearly)

## Encode Url
http://blog.codinghorror.com/url-shortening-hashes-in-practice/

Choice 1. md5(128 bit, 16 hex numbers, collision, birthday paradox, 2^(n/2) = 2^64) truncate? (64bit, 8 hex number, collision 2^32), Base64.

* Pros: hashing is simple and horizontally scalable.
* Cons: too long, how to purify expired URLs?

Choice 2. Distributed Seq Id Generator. (Base62: a~z, A~Z, 0~9, 62 chars, 62^7), sharding: each node maintains a section of ids.

* Pros: easy to outdate expired entries, shorter
* Cons: coordination (zookeeper)

## KV store

MySQL(10k qps, slow, no relation), KV (100k qps, Redis, Memcached)

A great candidate will ask about the lifespan of the aliases and design a system that purges aliases past their expiration.

## Followup
Q: How will shortened URLs be generated?

* A poor candidate will propose a solution that uses a single id generator (single point of failure) or a solution that requires coordination among id generator servers on every request. For example, a single database server using an auto-increment primary key.
* An acceptable candidate will propose a solution using an md5 of the URL, or some form of UUID generator that can be done independently on any node. While this allows distributed generation of non- colliding IDs, it yields large "shortened" URLs
* A good candidate will design a solution that utilizes a cluster of id generators that reserve chunks of the id space from a central coordinator (e.g. ZooKeeper) and independently allocate IDs from their chunk, refreshing as necessary.

Q: How to store the mappings?

* A poor candidate will suggest a monolithic database. There are no relational aspects to this store. It is a pure key-value store.
* A good candidate will propose using any light-weight, distributed store. MongoDB/HBase/Voldemort/etc.
* A great candidate will ask about the lifespan of the aliases and design a system that ==purges aliases past their expiration==

Q: How to implement the redirect servers?

* A poor candidate will start designing something from scratch to solve an already solved problem
* A good candidate will propose using an off-the-shelf HTTP server with a plug-in that parses the shortened URL key, looks the alias up in the DB, updates click stats and returns a 303 back to the original URL. Apache/Jetty/Netty/tomcat/etc. are all fine.

Q: How are click stats stored?

* A poor candidate will suggest write-back to a data store on every click
* A good candidate will suggest some form of ==aggregation tier that accepts clickstream data, aggregates it, and writes back a persistent data store periodically==

Q: How will the aggregation tier be partitioned?

* A great candidate will suggest a low-latency messaging system to buffer the click data and transfer it to the aggregation tier.
* A candidate may ask how often the stats need to be updated. If daily, storing in HDFS and running map/reduce jobs to compute stats is a reasonable approach If near real-time, the aggregation logic should compute stats

Q: How to prevent visiting restricted sites?

* A good candidate can answer with maintaining a blacklist of hostnames in a KV store.
* A great candidate may propose some advanced scaling techniques like bloom filter.
