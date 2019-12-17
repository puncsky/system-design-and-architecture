---
layout: post
title: "Designing Memcached or an in-memory KV store"
date: 2019-10-03 22:04
comments: true
categories: system design
language: en
abstract: Memcached = rich client + distributed servers + hash table + LRU. It features a simple server and pushes complexity to the client) and hence reliable and easy to deploy.
references:
  - https://github.com/memcached/memcached/wiki/Overview
  - https://people.cs.uchicago.edu/~junchenj/34702/slides/34702-MemCache.pdf
  - https://en.wikipedia.org/wiki/Hash_table
---

## Requirements 

1. High-performance, distributed key-value store
 * Why distributed? 
   * Answer: to hold a larger size of data 
 <img style="width: 200px;" src="https://res.cloudinary.com/dohtidfqh/image/upload/v1569196539/web-guiguio/memcached2.png"/>
2. For in-memory storage of small data objects
3. Simple server (pushing complexity to the client) and hence reliable and easy to deploy

## Architecture
Big Picture: Client-server

<img style="width: 256px;" src="https://res.cloudinary.com/dohtidfqh/image/upload/v1569196539/web-guiguio/memcached1.png"/>

* client
 * given a list of Memcached servers
 * chooses a server based on the key
* server
 * store KVs into the internal hash table
 * LRU eviction


The Key-value server consists of a fixed-size hash table + single-threaded handler + coarse locking

![hash table](https://res.cloudinary.com/dohtidfqh/image/upload/v1569197517/web-guiguio/900px-Hash_table_5_0_1_1_1_1_1_LL.svg.png)

How to handle collisions? Mostly three ways to resolve:

1. Separate chaining: the collided bucket chains a list of entries with the same index, and you can always append the newly collided key-value pair to the list.
2. open addressing: if there is a collision, go to the next index until finding an available bucket.
3. dynamic resizing: resize the hash table and allocate more spaces; hence, collisions will happen less frequently.

## How does the client determine which server to query?

See [Data Partition and Routing](https://puncsky.com/notes/2018-07-21-data-partition-and-routing)

## How to use cache?

See [Key value cache](https://puncsky.com/notes/122-key-value-cache)

## How to further optimize?

See [How Facebook Scale its Social Graph Store? TAO](https://puncsky.com/notes/49-facebook-tao)
