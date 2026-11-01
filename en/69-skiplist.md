---
slug: 69-skiplist
id: 69-skiplist
title: "Skiplist"
date: 2018-10-09 12:39
comments: true
tags: [system design, data structures]
description: "A skip list is a probabilistic, multi-level linked list that supports O(log n) search, insert, and delete. Used by LevelDB's MemTable, Redis's Sorted Set, and Lucene's inverted index. Notes on how it works, why it's chosen over balanced BSTs, and the concrete trade-offs in each real-world implementation."
references:
  - https://en.wikipedia.org/wiki/Skip_list
  - https://www.cl.cam.ac.uk/teaching/0506/Algorithms/skiplists.pdf
---

A skip list is a linked list you can binary-search on. You get `O(log n)` search, insert, and delete — the same asymptotic complexity as a balanced BST — without any of the rebalancing machinery. The trick is adding extra "express lanes" on top of the base list so you can skip ahead in large jumps.

## How it works

Build a linked list sorted by key. That list is level 0 — the base. Now add a sparser list on top (level 1) that contains roughly half the nodes. On top of _that_, another list (level 2) with a quarter of the nodes. And so on. The result is a pyramid of linked lists where each level is a "skip ahead" version of the level below.

```
level 3:    1 --------------------------------> 25
level 2:    1 -----> 9 -----------------------> 25
level 1:    1 -----> 9 -----> 17 -----> 21 ---> 25
level 0:    1 -> 4 -> 9 -> 12 -> 17 -> 19 -> 21 -> 25 -> 31
```

**Search** walks from the top-left. At each level, follow forward pointers until the next key would overshoot the target, then drop down a level. The drop-down cuts the search space roughly in half each time, giving `O(log n)` expected.

**Insert** searches for the insertion point (same as above), then flips a coin repeatedly to decide how many levels to promote the new node to. Each promotion has probability `p` (conventionally `0.5`). This is what gives you the geometric distribution of levels without any explicit rebalancing.

**Delete** splices the node out of every level it appears in.

The magic is that no rebalancing is ever needed — the probabilistic level assignment maintains the invariant statistically. Worst-case is `O(n)` (if the coin flips go pathologically in one direction), but the probability is vanishingly small.

## Why choose a skip list over a balanced BST?

Both give `O(log n)` operations. Three reasons teams pick skip list in practice:

1. **Simpler implementation.** A correct red-black tree or AVL tree is genuinely hard to get right — rotations, parent pointers, color invariants. A skip list is maybe 60 lines of code. For something you'll maintain for years, "obviously correct" beats "theoretically optimal" most of the time.
2. **Better concurrency.** Lock-free / fine-grained-locking skip lists are well-studied and more tractable than lock-free balanced trees, which are notoriously difficult. Concurrent skip list implementations (like Java's `ConcurrentSkipListMap`) are a go-to for sorted concurrent maps.
3. **Cheap range scans.** Because the base level is a plain linked list, iterating a key range is a pointer walk. BSTs require an in-order traversal with stack state, which is fiddly.

The trade-off: skip lists use more memory than a BST because of the extra forward pointers. Average memory overhead is about `2n` pointers for `p = 0.5`.

## Real-world implementations

### LevelDB / RocksDB MemTable

The in-memory write buffer that collects writes before they're flushed to disk as an SSTable. LevelDB picked skip list because writes must be ordered (so the eventual SSTable is sorted) and the MemTable needs to be concurrent-read / single-writer without lock contention on readers. Skip list's simple concurrency story fits perfectly. Google's leveldb source is ~400 lines of skip list code and it's been stable for over a decade.

### Redis Sorted Set (ZSET)

Redis sorted sets support both "get by score range" and "get by rank" operations. Redis uses a skip list _plus_ a hash table — the skip list gives `O(log n)` range queries by score, and the hash table gives `O(1)` membership tests. The skip list carries extra metadata per level (span counts) to support rank queries like `ZRANGEBYRANK`. A BST could do this too, but Redis chose skip list for the same simplicity/concurrency reasons as LevelDB.

### Lucene inverted index

Lucene uses skip lists inside posting lists to accelerate intersection. When you intersect two term posting lists for a boolean `AND` query, you need to fast-forward one list to a target docID from the other. Skip list's jump structure makes this `O(log n)` rather than `O(n)`. The skip list here is static — built once at index time, not modified.

## Minimal pseudocode

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
    lvl = randomLevel()          // geometric distribution, p = 0.5
    new_node = Node(key, value, lvl)
    for level in 0 to lvl:
        new_node.next[level] = update[level].next[level]
        update[level].next[level] = new_node
```

`randomLevel()` flips coins until one comes up tails, capped at `maxLevel`. This yields level `k` with probability `p^k * (1-p)`.

## When not to use a skip list

- **Very small n.** A flat sorted array with binary search beats skip list on constants up to a few thousand elements.
- **Static, read-heavy data.** A sorted array or a B-tree will use less memory and have better cache locality for read-only workloads.
- **Persistent / on-disk storage.** Skip list's scattered node allocation is a disaster for disk-backed structures — that's what B-trees and LSM-trees are for.

## See also

- [Bloom Filter](https://tianpan.co/notes/68-bloom-filter) — another probabilistic data structure, often used alongside skip-list-backed MemTables.
- [B-tree vs B+ tree](https://tianpan.co/notes/2018-07-22-b-tree-vs-b-plus-tree) — the on-disk analogue when skip list isn't the right fit.
