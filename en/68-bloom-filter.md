---
slug: 68-bloom-filter
id: 68-bloom-filter
title: "Bloom Filter"
date: 2018-10-09 12:39
comments: true
tags: [system design, data structures, probabilistic]
description: "A Bloom filter is a compact probabilistic set-membership data structure — ~10 bits per element for 1% false positives, zero false negatives. Notes on how it works, the math for picking parameters, where real systems use it (Cassandra, HBase, Chrome, CDNs), and when to reach for counting / cuckoo / quotient variants instead."
references:
  - https://en.wikipedia.org/wiki/Bloom_filter
  - https://hur.st/bloomfilter/
---

A Bloom filter tests set membership with far less space than storing the set itself — at the cost of a small, tunable false-positive rate. The trade-off is memorable: **no false negatives, possible false positives**. If the filter says "not in the set," you can trust that completely. If it says "possibly in the set," you need a second, authoritative check.

That asymmetry is exactly what makes it useful: it's a cheap _negative cache_ that lets expensive systems skip work on items they don't have.

## How it works

Allocate a bit array of size `m`, initialized to zero, and pick `k` independent hash functions that each map any element to a position in `[0, m)`.

**Insert(x):** compute `k` hashes of `x`, set all `k` bits to 1.

**Contains(x):** compute the same `k` hashes. If any of the `k` bits is 0, `x` is definitely _not_ in the set. If all `k` bits are 1, `x` is _probably_ in the set — but could be a false positive (all `k` bits happened to be set by other inserts).

```
m = 16 bits, k = 2 hash functions

insert("cat"):   hashes → (3, 11)    bits: 0001000000010000
insert("dog"):   hashes → (1, 7)     bits: 0101000100010000

contains("cat"): hashes → (3, 11)    both 1 → "probably in"
contains("fox"): hashes → (1, 3)     both 1 → false positive!
contains("owl"): hashes → (5, 9)     bit 5 is 0 → "definitely not in"
```

Standard implementation uses two hash functions and derives the `k` positions via `h_i(x) = h1(x) + i·h2(x)` — the "Kirsch-Mitzenmacher" trick — to avoid computing `k` separate hashes.

## The math (picking m and k)

Given an expected number of elements `n` and a desired false-positive rate `p`, the optimal sizing is:

```
m = -(n · ln(p)) / (ln(2))²       ≈ 9.6 · n bits for p = 0.01
k = (m / n) · ln(2)               ≈ 7 hash functions for p = 0.01
```

Practical rules of thumb:

- **~10 bits per element** gets you a 1% false-positive rate.
- **~14 bits per element** gets you 0.1%.
- **~20 bits per element** gets you ~0.007%.

Every 10× reduction in false-positive rate costs a constant ~4.8 extra bits per element (10% → 1% → 0.1% needs ~4.8 → ~9.6 → ~14.4 bits). Memory grows with `log(1/p)`, and linearly with `n`.

Online calculator: [hur.st/bloomfilter](https://hur.st/bloomfilter/) is the standard reference for picking parameters.

## What you _can't_ do

- **Delete elements.** Once a bit is set, you can't clear it without potentially corrupting membership for other elements that also set that bit. If you need deletion, use a counting Bloom filter (cells are counters rather than bits) or a cuckoo filter.
- **Enumerate elements.** A Bloom filter only answers membership queries. It doesn't know _what_ it contains.
- **Get the exact count.** You can estimate `n` from the number of set bits, but it's approximate.
- **Grow dynamically.** If you insert more elements than the filter was sized for, the false-positive rate degrades silently. Scalable Bloom filters work around this with a cascade of sub-filters.

## Where real systems use it

### Cassandra / RocksDB / LevelDB SSTables

The canonical LSM-tree use case. Each immutable sorted file (SSTable / SST) has an in-memory Bloom filter of the keys it contains. On a read, the system checks filters across all SSTables before touching disk. A 1% false positive rate means 99% of reads for non-existent keys skip disk entirely — which is the difference between "fast" and "unusable" under a key-space that doesn't fit in the block cache.

### HBase

Same pattern as Cassandra, but offers both row-level and row+column-level Bloom filters. Column-level is more expensive to maintain but lets narrow scans skip even more I/O.

### Chrome Safe Browsing (historical)

Google Chrome used a Bloom filter locally to check URLs against a list of known-malicious sites. The filter fit in a few MB and was refreshed periodically; any hit triggered a real server call. The design was replaced by a variant (Chrome now uses a hash prefix + Update protocol).

### CDN cache eviction and hot-key detection

CDN edge nodes use Bloom filters to track "have we seen this key at all recently?" before promoting to cache. This avoids caching one-hit wonders that would pollute the LRU.

### Anti-fraud and blocklists

Bloom filters are ideal for "is this user banned?" or "is this email on the suppression list?" — the blocklist can be huge, the check is O(1), and a false positive (reject a legitimate user) is tolerable if rare and the system falls back to an authoritative check.

### Bitcoin SPV clients

Simplified Payment Verification wallets send a Bloom filter to full nodes to request transactions relevant to their addresses, without revealing which addresses are theirs. This has known privacy weaknesses (BIP 37) but illustrates the "request more than I need, filter locally" pattern.

## Variants worth knowing

- **Counting Bloom filter.** Each cell is a small counter (e.g. 4 bits) instead of a bit. Supports deletion at ~4x the space cost.
- **Scalable Bloom filter.** Cascade of filters where a new one is added when the current fills; queries check all. Handles unknown `n`.
- **Cuckoo filter.** Similar space/FPR profile to Bloom, but supports deletions natively and has better cache locality. Often a drop-in replacement when you need deletes.
- **Quotient filter.** Better cache behavior and merge support. Used in newer storage systems.
- **Partitioned Bloom filter.** Divides `m` into `k` disjoint regions, one per hash function. Slightly worse FPR at the same size but simpler analysis and better parallelism.
- **Blocked Bloom filter.** Each insert touches a single cache line. Much faster on modern CPUs at a small FPR cost. Used in ClickHouse, Impala, and similar analytical engines.

## When not to use a Bloom filter

- **Membership is the answer, not a prefilter.** If a false positive has no cheap fallback check, you can't use a probabilistic structure. Use a hash set.
- **The set is tiny.** For `n < ~1000`, a hash set is faster and simpler. Bloom filters win on space, not time.
- **Deletes are frequent and unbounded.** Counting Bloom filters decay in accuracy over many inserts and deletes. Cuckoo filters degrade too, just more gracefully.
- **You need to enumerate or serialize the elements.** A Bloom filter is a one-way structure.

## See also

- [Skiplist](https://tianpan.co/notes/69-skiplist) — the in-memory structure that Bloom filters typically sit in front of in LSM-tree MemTables.
- [B-tree vs B+ tree](https://tianpan.co/notes/2018-07-22-b-tree-vs-b-plus-tree) — the on-disk storage structures that Bloom filters protect from unnecessary reads.
- [How to scale a web service?](https://tianpan.co/notes/41-how-to-scale-a-web-service) — Bloom filters are a common tool when sharded storage needs to avoid cross-shard lookups.
