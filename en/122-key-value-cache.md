---
layout: post
title: "Key value cache"
date: 2019-01-06 23:24
comments: true
language: en
categories: system design
---

KV cache is like a giant hash map and used to reduce the latency of data access, typically by

1. Putting data from slow and cheap media to fast and expensive ones.
2. Indexing from tree-based data structures of `O(log n)` to hash-based ones of  `O(1)` to read and write


There are various cache policies like read-through/write-through(or write-back), and cache-aside. By and large, Internet services have a read to write ratio of 100:1 to 1000:1, so we usually optimize for read.

In distributed systems, we choose those policies according to the business requirements and contexts, under the guidance of [CAP theorem](https://puncsky.com/notes/2018-07-24-replica-and-consistency).



## Regular Patterns

* Read
    * Read-through: the clients read data from the database via the cache layer. The cache returns when the read hits the cache; otherwise, it fetches data from the database, caches it, and then return the vale.
* Write
    * Write-through: clients write to the cache and the cache updates the database. The cache returns when it finishes the database write.
    * Write-behind / write-back: clients write to the cache, and the cache returns immediately. Behind the cache write, the cache asynchronously writes to the database.
    * Write-around: clients write to the database directly, around the cache.



## Cache-aside pattern
When a cache does not support native read-through and write-through operations, and the resource demand is unpredictable, we use this cache-aside pattern.

* Read: try to hit the cache. If not hit, read from the database and then update the cache.
* Write: write to the database first and then ==delete the cache entry==. A common pitfall here is that [people mistakenly update the cache with the value, and double writes in a high concurrency environment will make the cache dirty](https://www.quora.com/Why-does-Facebook-use-delete-to-remove-the-key-value-pair-in-Memcached-instead-of-updating-the-Memcached-during-write-request-to-the-backend).


==There are still chances for dirty cache in this pattern.== It happens when these two cases are met in a racing condition:

1. read database and update cache
2. update database and delete cache



## Where to put the cache?

* client-side
* distinct layer
* server-side



## What if data volume reaches the cache capacity? Use cache replacement policies
* LRU(Least Recently Used): evict the most recently used entries and keep the most recently used ones.
* LFU(Least Frequently Used): evict the most frequently used entries and keep the most frequently used ones.
* ARC(Adaptive replacement cache): it has a better performance than LRU. It is achieved by keeping both the most frequently and frequently used entries, as well as a history for eviction. (Keeping MRU+MFU+eviction history.)



## Who are the King of the cache usage?
[Facebook TAO](https://puncsky.com/notes/49-facebook-tao)
