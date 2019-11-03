---
layout: post
title: "Bloom Filter"
date: 2018-10-09 12:39
comments: true
categories: system design, data structures
language: en
references:
  - https://en.wikipedia.org/wiki/Bloom_filter
---

A Bloom filter is a data structure used to detect whether an element is in a set in a time and space efficient way.

False positive matches are possible, but false negatives are not – in other words, a query returns either "possibly in set" or "definitely not in set". Elements can be added to the set, but not removed (though this can be addressed with a "counting" bloom filter); the more elements that are added to the set, the larger the probability of false positives.

Usecases

- Cassandra uses Bloom filters to determine whether an SSTable has data for a particular row.
- An HBase Bloom Filter is an efficient mechanism to test whether a StoreFile contains a specific row or row-col cell.
- A website's anti-fraud system can use bloom filters to reject banned users effectively.
- The Google Chrome web browser used to use a Bloom filter to identify malicious URLs.
