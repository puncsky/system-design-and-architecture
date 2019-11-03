---
layout: post
title: "B tree vs. B+ tree"
date: 2018-07-22 11:54
comments: true
categories: system design
language: en
references:
    - https://stackoverflow.com/questions/870218/differences-between-b-trees-and-b-trees
---

![B tree vs. B+ tree](https://res.cloudinary.com/dohtidfqh/image/upload/v1566606512/web-guiguio/bMjxUqmqcmytVpJLUd9gAVEzrmGEowwQdqV4bBARLvWVRauXH_IXY01atDp4xgAnRy89RhWy9yzThAUBwIU6xWwk9gHOZT9EdXLp7rwQ3SUFwyo_4O-uUkh34vkk424x13Mlzck.png)

Pros of B tree

- Data associated with each key ⟶ frequently accessed nodes can lie closer to the root, and therefore can be accessed more quickly.

Pros of B+ tree

- No data associated in the interior nodes ⟶ more keys in memory ⟶ fewer cache misses
- Leaf nodes of B+ trees are linked ⟶ easier to traverse ⟶ fewer cache misses
