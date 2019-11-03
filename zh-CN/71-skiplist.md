---
layout: post
title: "跳跃表"
date: 2018-10-09 12:39
comments: true
categories: data structures, system design
language: zh-cn
abstract: 跳跃表本质上是一个允许对其进行二分搜索的链表。它实现这一点的方法是添加额外的节点，使你能够“跳过”链接列表的部分。对于给定一个正反随机数来创建额外的节点，跳跃表具有O(logn)复杂度的查询、插入和删除。
references:
  - https://en.wikipedia.org/wiki/Skip_list
---

跳跃表本质上是一个允许对其进行二分搜索的链表。它实现这一点的方法是添加额外的节点，使你能够“跳过”链接列表的部分。对于给定一个正反随机数来创建额外的节点，跳跃表具有O(logn)复杂度的查询、插入和删除。

用例

- LevelDB MemTable
- Redis 有序集合(Redis SortedSet)
- 倒排索引(Lucene inverted index)
