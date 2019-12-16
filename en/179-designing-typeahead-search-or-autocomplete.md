---
layout: post
title: "Designing typeahead search or autocomplete"
date: 2019-10-10 18:33
comments: true
categories: system design
language: en
slides: false
abstract: How to design a realtime typeahead autocomplete service? Linkedin's Cleo lib answers with a multi-layer architecture (browser cache / web tier / result aggregator / various typeahead backend) and 4 elements (inverted / forward index, bloom filter, scorer).
references:
  - https://engineering.linkedin.com/open-source/cleo-open-source-technology-behind-linkedins-typeahead-search
  - http://sna-projects.com/cleo/
---

## Requirements

* realtime / low-latency typeahead and autocomplete service for social networks, like Linkedin or Facebook
* search social profiles with prefixes 
* newly added account appear instantly in the scope  of the search
* not for “query autocomplete” (like the Google search-box dropdown), but for displaying actual search results, including
    * generic typeahead: network-agnostic results from a global ranking scheme like popularity.
    * network typeahead: results from user’s 1st and 2nd-degree network connections, and People You May Know scores.

![Linkedin Search](https://res.cloudinary.com/dohtidfqh/image/upload/v1570758247/web-guiguio/linkedin-typeahead.jpg)

## Architecture

Multi-layer architecture

* browser cache
* web tier
* result aggregator
* various typeahead backend

![Cleo Architecture](https://res.cloudinary.com/dohtidfqh/image/upload/v1570321528/web-guiguio/cleo.png)

## Result Aggregator
The abstraction of this problem is to find documents by prefixes and terms in a very large number of elements. The solution leverages these four major data structures:

1. `InvertedIndex<prefixes or terms, documents>`: given any prefix, find all the document ids that contain the prefix.
2. `for each document, prepare a BloomFilter<prefixes or terms>`: with user typing more, we can quickly filter out documents that do not contain the latest prefixes or terms, by check with their bloom filters.
3. `ForwardIndex<documents, prefixes or terms>`: previous bloom filter may return false positives, and now we query the actual documents to reject them.
4. `scorer(document):relevance`: Each partition return all of its true hits and scores. And then we aggregate and rank.

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1570758116/web-guiguio/cleo-search-flow_0.jpg)

## Performance

* generic typeahead: latency <= 1 ms within a cluster
* network typeahead (very-large dataset over 1st and 2nd degree network):  latency <= 15 ms 
* aggregator: latency <= 25 ms
