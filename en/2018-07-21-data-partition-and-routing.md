---
layout: post
title: "Data Partition and Routing"
date: 2018-07-20 11:54
comments: true
categories: system design
language: en
---

## Why data partition and routing?

large dataset ⟶ scale out ⟶ data shard / partition ⟶ 1) routing for data access 2) replica for availability

- Pros
    - availability
    - read(parallelization, single read efficiency)
- Cons
    - consistency

## How to do data partition and routing?

The routing abstract model is essentially just two maps: 1) key-partition map 2) partition-machine map



### Hash partition

1. hash and mod
    - (+) simple
    - (-) flexibility (tight coupling two maps: adding and removing nodes (partition-machine map) disrupt existing key-partition map)

2. Virtual buckets: key--(hash)-->vBucket, vBucket--(table lookup)-->servers
    - Usercase: Membase a.k.a Couchbase, Riak
    - (+) flexibility, decoupling two maps
    - (-) centralized lookup table

3. Consistent hashing and DHT
    - [Chord] implementation
    - virtual nodes: for load balance in heterogeneous data center
    - Usercase: Dynamo, Cassandra
    - (+) flexibility, hashing space decouples two maps. two maps use the same hash, but adding and removing nodes ==only impact succeeding nodes==.
    - (-) network complexity, hard to maintain



### Range partition

sort by primary key, shard by range of primary key

range-server lookup table (e.g. HBase .META. table) + local tree-based index (e.g. LSM, B+)

(+) search for a range
(-) log(n)

Usercase: Yahoo PNUTS, Azure, Bigtable
