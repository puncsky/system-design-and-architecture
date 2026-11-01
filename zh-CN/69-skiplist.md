---
slug: 69-skiplist
id: 69-skiplist
title: 跳表
date: "2018-10-09 12:39"
comments: true
tags:
  - system design
  - data structures
description: "跳表是一种概率性的多层链表，支持 O(log n) 的搜索、插入与删除。被 LevelDB 的 MemTable、Redis 的 Sorted Set 和 Lucene 的倒排索引采用。本文讲解其工作原理、为何相较于平衡 BST 被选中，以及每个真实实现中的具体权衡。"
references:
  - "https://en.wikipedia.org/wiki/Skip_list"
  - https://www.cl.cam.ac.uk/teaching/0506/Algorithms/skiplists.pdf
---

跳表是你可以对其做二分查找的链表。你获得 `O(log n)` 的搜索、插入和删除——与平衡 BST 相同的渐近复杂度——而无需任何再平衡机制。诀窍在于在基础链表之上添加额外的"快车道"，让你可以大步跳跃前进。

## 工作原理

构建一条按键有序的链表，这是第 0 层——基础层。在上面加一条更稀疏的链表（第 1 层），包含大约一半的节点。再上面一层（第 2 层），包含四分之一的节点。以此类推。最终形成一个金字塔，每一层都是下一层的"跳过"版本。

```
第 3 层：    1 --------------------------------> 25
第 2 层：    1 -----> 9 -----------------------> 25
第 1 层：    1 -----> 9 -----> 17 -----> 21 ---> 25
第 0 层：    1 -> 4 -> 9 -> 12 -> 17 -> 19 -> 21 -> 25 -> 31
```

**搜索**从左上角开始。在每一层沿前向指针前进，直到下一个键将越过目标，此时下降一层。下降每次大约把搜索空间减半，期望复杂度 `O(log n)`。

**插入**先像搜索一样找到插入位置，然后反复掷硬币决定新节点升到第几层。每次升级的概率为 `p`（惯例为 `0.5`）。这样在不需要显式再平衡的情况下得到层数的几何分布。

**删除**把节点从所有它出现的层中摘下。

其魅力在于从不需要再平衡——概率性层级分配在统计意义上维持了不变量。最坏情况为 `O(n)`（如果硬币投得极度偏），但概率极小。

## 为什么选跳表而非平衡 BST？

两者都能提供 `O(log n)`。实践中团队选择跳表的三个理由：

1. **实现更简单。** 一个正确的红黑树或 AVL 树真的很难写对——旋转、父指针、颜色不变量。跳表也许只要 60 行代码。对你要维护多年的东西而言，"一眼看上去就对"通常比"理论最优"更有价值。
2. **更好的并发性。** 无锁/细粒度锁的跳表实现已有充分研究，比无锁平衡树（后者以难度著称）更易于处理。并发跳表实现（如 Java 的 `ConcurrentSkipListMap`）是有序并发映射的首选。
3. **范围扫描便宜。** 因为基础层是普通链表，迭代一段键范围只是指针遍历。BST 需要中序遍历加栈状态，实现琐碎。

权衡：跳表因额外的前向指针而比 BST 使用更多内存。在 `p = 0.5` 时，平均内存开销约为 `2n` 个指针。

## 真实实现

### LevelDB / RocksDB MemTable

在写入被刷新为 SSTable 之前收集写入的内存写缓冲。LevelDB 选择跳表的原因是：写入必须有序（以便最终生成的 SSTable 有序），且 MemTable 需要支持并发读 / 单写而不让读操作为锁争用所苦。跳表简洁的并发故事正好契合。Google 的 leveldb 源码中约有 400 行跳表代码，已稳定运行十余年。

### Redis Sorted Set（ZSET）

Redis 的 sorted set 同时支持"按分数范围"和"按名次"两种操作。Redis 使用跳表*加*哈希表——跳表给出按分数的 `O(log n)` 范围查询，哈希表给出 `O(1)` 的成员检测。跳表每层携带额外元数据（span 计数），以支持像 `ZRANGEBYRANK` 这样的排名查询。BST 也能做到，但 Redis 选跳表的理由和 LevelDB 一样——简洁性和并发性。

### Lucene 倒排索引

Lucene 在 posting list 内部使用跳表以加速交集运算。在为布尔 `AND` 查询求两个 term 的 posting list 交集时，你需要从另一个列表中快速前进到目标 docID。跳表的跳跃结构把这变为 `O(log n)` 而非 `O(n)`。这里的跳表是静态的——在索引建立时一次性构造，之后不修改。

## 最小伪代码

```python
search(list, target):
    node = list.head
    for level in list.maxLevel down to 0:
        while node.next[level] and node.next[level].key < target:
            node = node.next[level]
    node = node.next[0]
    return node if node.key == target else null

insert(list, key, value):
    update = array of size maxLevel
    node = list.head
    for level in list.maxLevel down to 0:
        while node.next[level] and node.next[level].key < key:
            node = node.next[level]
        update[level] = node
    lvl = randomLevel()          // 几何分布，p = 0.5
    new_node = Node(key, value, lvl)
    for level in 0 to lvl:
        new_node.next[level] = update[level].next[level]
        update[level].next[level] = new_node
```

`randomLevel()` 一直掷硬币直到出现反面，并以 `maxLevel` 封顶。这样得到第 `k` 层的概率为 `p^k * (1-p)`。

## 何时不要用跳表

- **非常小的 n。** 一个平坦的有序数组加二分查找，在几千个元素以下的常数因子上都能胜过跳表。
- **静态、读多的数据。** 对只读负载，有序数组或 B 树内存更少、缓存局部性更好。
- **持久化 / 磁盘存储。** 跳表节点分散的分配方式对磁盘支持的结构是一场灾难——那是 B 树和 LSM 树的用武之地。

## 参见

- [布隆过滤器](https://tianpan.co/notes/68-bloom-filter) —— 另一个概率性数据结构，常与跳表支撑的 MemTable 配合使用。
- [B 树与 B+ 树](https://tianpan.co/notes/2018-07-22-b-tree-vs-b-plus-tree) —— 当跳表不合适时的磁盘类比。
