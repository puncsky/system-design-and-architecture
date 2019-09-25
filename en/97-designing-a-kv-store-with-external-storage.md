---
layout: post
title: "Designing a KV store with external storage"
date: 2018-11-10 12:39
comments: true
categories: system design
language: en
references:
  - http://basho.com/wp-content/uploads/2015/05/bitcask-intro.pdf
---

## Requirements

1. Data size: Data size of values is too large to be held in memory, and we should leverage the external storage for them. However, we can still keep the data keys in memory.
2. Single-host solution. No distributed design.
3. Optimize for write.



## Solution
* In-memory hashmap index + index hint file + data files
* Append-only for write optimization. Have only one active data file for write. And compact active data to the older data file(s) for read.



## Components

1. In-memory `HashMap<Key, <FildId, ValueOffset, ValueSize, Timestamp>>`

2. Data file layout

```txt
|crc|timestamp|key_size|value_size|key|value|
...
```

3. (index) hint file that the in-memory hashmap can recover from



## Operations

Delete: get the location by the in-memory hashmap, if it exists, then go to the location on the disk to set the value to a magic number.

Get: get the location by the in-memory hashmap, and then go to the location on the disk for the value.

Put: append to the active data file and update the in-memory hash map.


Periodical compaction strategies

* Copy latest entries: In-memory hashmap is always up-to-date. Stop and copy into new files. Time complexity is O(n) n is the number of valid entries.
    * Pros: Efficient for lots of entries out-dated or deleted.
    * Cons: Consume storage if little entries are out-dated. May double the space. (can be resolved by having a secondary node do the compression work with GET/POST periodically. E.g., Hadoop secondary namenode).


* Scan and move: foreach entry, if it is up-to-date, move to the tail of the validated section. Time complexity is O(n) n is the number of all the entries.
    * Pros:
        * shrink the size
        * no extra storage space needed
    * Cons:
        * Complex and need to sync hashmap and storage with transactions. May hurt performance.


Following up questions

* How to detect records that can be compacted?
    * Use timestamp.
* What if one hashmap cannot fit into a single machine’s memory?
    * Consistent hashing, chord DHT, query time complexity is O(logn) with the finger table, instead of O(1) here with a hashmap.
