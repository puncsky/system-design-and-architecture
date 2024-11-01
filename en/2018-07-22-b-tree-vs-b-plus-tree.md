---
slug: 2018-07-22-b-tree-vs-b-plus-tree
id: 2018-07-22-b-tree-vs-b-plus-tree
title: "B tree vs. B+ tree"
date: 2018-07-22 11:54
comments: true
tags: [system design]
description: "A B+ tree can be seen as B tree in which each node contains only keys. Pros of B+ tree can be summarized as fewer cache misses. In B tree, the data is associated with each key and can be accessed more quickly."
references:
    - https://stackoverflow.com/questions/870218/differences-between-b-trees-and-b-trees
---

![B tree vs. B+ tree](https://res.cloudinary.com/dohtidfqh/image/upload/v1566606512/web-guiguio/bMjxUqmqcmytVpJLUd9gAVEzrmGEowwQdqV4bBARLvWVRauXH_IXY01atDp4xgAnRy89RhWy9yzThAUBwIU6xWwk9gHOZT9EdXLp7rwQ3SUFwyo_4O-uUkh34vkk424x13Mlzck.png)

Pros of B tree

- Data associated with each key ⟶ frequently accessed nodes can lie closer to the root, and therefore can be accessed more quickly.

Pros of B+ tree

- No data associated in the interior nodes ⟶ more keys in memory ⟶ fewer cache misses
- Leaf nodes of B+ trees are linked ⟶ easier to traverse ⟶ fewer cache misses
