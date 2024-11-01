---
slug: 2018-07-22-b-tree-vs-b-plus-tree
id: 2018-07-22-b-tree-vs-b-plus-tree
layout: post
title: "B 树与 B+ 树"
date: 2018-07-22 11:54
comments: true
categories: 系统设计
language: cn
abstract: "B+ 树可以被视为 B 树，其中每个节点仅包含键。B+ 树的优点可以总结为更少的缓存未命中。在 B 树中，数据与每个键相关联，可以更快地访问。"
references:
    - https://stackoverflow.com/questions/870218/differences-between-b-trees-and-b-trees
---

![B 树与 B+ 树](https://res.cloudinary.com/dohtidfqh/image/upload/v1566606512/web-guiguio/bMjxUqmqcmytVpJLUd9gAVEzrmGEowwQdqV4bBARLvWVRauXH_IXY01atDp4xgAnRy89RhWy9yzThAUBwIU6xWwk9gHOZT9EdXLp7rwQ3SUFwyo_4O-uUkh34vkk424x13Mlzck.png)

B 树的优点

- 与每个键相关联的数据 ⟶ 频繁访问的节点可以更靠近根节点，因此可以更快地访问。

B+ 树的优点

- 内部节点没有关联数据 ⟶ 内存中更多的键 ⟶ 更少的缓存未命中
- B+ 树的叶子节点是链接的 ⟶ 更容易遍历 ⟶ 更少的缓存未命中