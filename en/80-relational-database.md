---
layout: post
title: "Intro to Relational Database"
date: 2018-10-18 23:19
comments: true
categories: system design
language: en
references:
  - https://www.puncsky.com/blog/2016-02-13-crack-the-system-design-interview
---

Relational database is the default choice for most storage use cases, by reason of ACID (atomicity, consistency, isolation, and durability). One tricky thing is "consistency" -- it means that any transaction will bring database from one valid state to another, which is different from Consistency in [CAP theorem](/notes/2018-07-24-replica-and-consistency).

## Schema Design and 3rd Normal Form (3NF)

To reduce redundancy and improve consistency, people follow 3NF when designing database schemas:

- 1NF: tabular, each row-column intersection contains only one value
- 2NF: only the primary key determines all the attributes
- 3NF: only the candidate keys determine all the attributes (and non-prime attributes do not depend on each other)

## Db Proxy

What if we want to eliminate single point of failure? What if the dataset is too large for one single machine to hold? For MySQL, the answer is to use a DB proxy to distribute data, <a target="_blank" href="http://dba.stackexchange.com/questions/8889/mysql-sharding-vs-mysql-cluster">either by clustering or by sharding</a>

Clustering is a decentralized solution. Everything is automatic. Data is distributed, moved, rebalanced automatically. Nodes gossip with each other, (though it may cause group isolation).

Sharding is a centralized solution. If we get rid of properties of clustering that we don't like, sharding is what we get. Data is distributed manually and does not move. Nodes are not aware of each other.
