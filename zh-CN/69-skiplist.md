---
slug: 69-skiplist
id: 69-skiplist
layout: post
title: "跳表"
date: 2018-10-09 12:39
comments: true
categories: 系统设计, 数据结构
description: "跳表本质上是一种链表，允许您在其上进行二分查找。它通过添加额外的节点来实现这一点，使您能够‘跳过’链表的某些部分。LevelDB MemTable、Redis SortedSet 和 Lucene 倒排索引都使用了这种结构。"
references:
  - https://en.wikipedia.org/wiki/Skip_list
---

跳表本质上是一种链表，允许您在其上进行二分查找。它通过添加额外的节点来实现这一点，使您能够‘跳过’链表的某些部分。通过随机投掷硬币来创建额外节点，跳表的搜索、插入和删除操作的时间复杂度应为 O(logn)。

用例

- LevelDB MemTable
- Redis SortedSet
- Lucene 倒排索引