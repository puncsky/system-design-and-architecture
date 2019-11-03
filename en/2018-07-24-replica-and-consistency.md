---
layout: post
title: "Replica, Consistency, and CAP theorem"
date: 2018-07-24 11:54
comments: true
categories: system design
language: en
references:
    - https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed
---

## Why replica and consistency?

large dataset ⟶ scale out ⟶ data shard / partition ⟶ 1) routing for data access 2) replica for availability ⟶ consistency challenge



## Consistency trade-offs for CAP theorem

![CAP Theorem](https://res.cloudinary.com/dohtidfqh/image/upload/v1566606463/web-guiguio/Es1houG50FNQoCgGUo2fGwMPriezTtKqliSVMW9F11CN2W7SSHcI3li61Qdnw0FoOm0UfitYOvbAiJBvJXLmAmrjRH75VDO54uGucIynJrdR2RV51GboaZ17bc5pZt88_GK43PT0.png)

- Consistency: all nodes see the same data at the same time
- Availability: a guarantee that every request receives a response about whether it succeeded or failed
- Partition tolerance: system continues to operate despite arbitrary message loss or failure of part of the system



Any networked shared-data system can have only two of three desirable properties.

- rDBMS prefer CP ⟶ ACID
- NoSQL prefer AP ⟶ BASE



## "2 of 3" is mis-leading

12 years later, the author Eric Brewer said "2 of 3" is mis-leading, because

1. partitions are rare, there is little reason to forfeit C or A when the system is not partitioned.
2. choices can be actually applied to multiple places within the same system at very fine granularity.
3. choices are not binary but with certain degrees.



Consequently, when there is no partition (nodes are connected correctly), which is often the case, we should have both AC. When there are partitions, deal them with 3 steps:

1. detect the start of a partition,
2. enter an explicit partition mode that may limit some operations, and
3. initiate partition recovery (compensate for mistakes) when communication is restored.
