---
layout: post
title: "Skiplist"
date: 2018-10-09 12:39
comments: true
categories: system design, data structures
language: en
references:
  - https://en.wikipedia.org/wiki/Skip_list
---

A skip-list is essentially a linked list that allows you to binary search on it. The way it accomplishes this is by adding extra nodes that will enable you to 'skip' sections of the linked-list. Given a random coin toss to create the extra nodes, the skip list should have O(logn) searches, inserts and deletes.

Usecases

- LevelDB MemTable
- Redis SortedSet
- Lucene inverted index
