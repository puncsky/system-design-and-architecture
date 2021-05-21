---
layout: post
title: "ACID vs BASE"
date: 2018-07-26 11:54
comments: true
categories: system design
language: en
references:
    - https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed
---

ACID (Consistency over Availability)

- Atomicity ensures transaction succeeds completely or fails completely.
- Consistency: In ACID, the C means that a transaction preserves all the database rules, such as unique keys, triggers, cascades. In contrast, the C in CAP refers only to single copy consistency, a strict subset of ACID consistency.
- Isolation ensures that concurrent execution of transactions leaves the database in the same state that would have been obtained if the transactions were executed sequentially.
- Durability ensures that once a transaction has been committed, it will remain committed even in the case of a system failure (e.g. power outage or crash).

BASE (Availability over Consistency)

- Basically available indicates that the system is guaranteed to be available
- Soft state indicates that the state of the system may change over time, even without input. This is mainly due to the eventually consistent model.
- Eventual consistency indicates that the system will become consistent over time, given that the system doesn't receive input during that time.

Although most NoSQL takes BASE priciples, they are learning from or moving toward ACID. e.g. Google Spanner provides strong consistency. MongoDB 4.0 adds support for multi-document ACID transactions.
