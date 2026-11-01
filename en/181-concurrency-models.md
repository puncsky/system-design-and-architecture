---
slug: 181-concurrency-models
id: 181-concurrency-models
title: "Concurrency Models"
date: 2019-10-16 14:04
comments: true
tags: [system design, concurrency, programming-languages]
description: "Five concurrency models — single-threaded async, shared-memory threads with locks, CSP, Actor Model, and Software Transactional Memory — compared on how they share state, how they compose, and what kinds of failure they produce. Notes on when each fits and why language choice often dictates the model more than the problem does."
---

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571262011/web-guiguio/Concurrency_Models_1.png)

Concurrency models are different answers to one question: **how do independent threads of execution coordinate without corrupting each other's data?** Each model makes different trade-offs between performance, composability, and the kinds of bugs it produces. Language choice often forces the model — you can use CSP in any language, but Go makes it the path of least resistance; you can do threads in Erlang, but you won't.

## 1. Single-threaded async

One OS thread, many logical tasks multiplexed via an event loop. Vanilla JavaScript, Node.js, Python asyncio, Tokio (single-threaded runtime).

```
Callback:   fs.read(file, (err, data) => { ... })
Promise:    fs.readFile(file).then(data => ...)
async/await: const data = await fs.readFile(file)
```

- **What you share:** all task state is in the same thread; no data races on memory by construction.
- **What you pay:** any CPU-bound operation blocks the whole event loop. One slow task = everyone waits.
- **Where bugs come from:** unhandled promise rejections, forgetting `await`, callback ordering hazards, long microtask queues starving I/O.
- **When to reach for it:** I/O-heavy workloads (web servers, API gateways, UI). Node.js became popular precisely because most web workloads are I/O-bound.

This model is deceptively easy to write but surprisingly hard to operate at scale. The moment a request does heavy CPU work, you need worker pools, and suddenly you have both models.

## 2. Shared-memory threading with locks

Multiple OS threads sharing address space; mutexes, read/write locks, semaphores protect critical sections. Java, C++, Python threads (with the GIL), C#.

- **What you share:** everything — memory is the communication mechanism.
- **What you pay:** lock contention, deadlocks, priority inversion, memory-model visibility bugs (reads seeing stale values because of CPU reordering or compiler optimizations).
- **Classic failure modes:**
  - **Deadlock:** two locks acquired in different orders by two threads. Every experienced systems engineer has debugged this; most have caused it.
  - **Livelock:** threads keep reacting to each other without making progress.
  - **Race condition:** two threads update shared state without synchronization; the final state depends on timing.
  - **Priority inversion:** low-priority thread holds a lock the high-priority thread needs.
- **When it's unavoidable:** inside databases, kernels, garbage collectors, high-performance libraries. Anywhere the performance cost of message-passing is too high and you have the engineering maturity to manage the failure modes.

Rich Hickey's critique of this model ("Simple Made Easy") is the cleanest articulation of why it produces so many bugs: it conflates identity with value, and gives no mechanism for reasoning about _time_.

## 3. Communicating Sequential Processes (CSP)

Tony Hoare's 1978 model, popularized by Go's goroutines and channels, and by Clojure's `core.async`. Processes are anonymous; channels are first-class.

```go
ch := make(chan int)
go func() { ch <- computeSomething() }()
result := <-ch
```

- **What you share:** nothing by default. State moves _via channels_, not shared memory.
- **What you pay:** channel-passing overhead, some cognitive load in designing the communication graph.
- **Go's slogan** ("Do not communicate by sharing memory; share memory by communicating") captures the discipline: if you need two goroutines to agree on a value, send it on a channel rather than pointing them at the same variable.
- **Strengths:** composable. A channel-consuming function doesn't care who produced the data. Easy to add intermediaries (filters, fan-out, fan-in).
- **Weaknesses:** Go's channels are unbuffered by default, and bounded buffers create deadlock hazards. Goroutine leaks (forgotten goroutines blocking on a channel that will never receive) are a common production bug.
- **When to reach for it:** general-purpose server code where you want concurrency without shared-state pain. Go's popularity in systems-adjacent work (Kubernetes, Docker, Prometheus) is largely due to CSP being the default.

## 4. Actor Model

Carl Hewitt's 1973 model, most famously implemented in Erlang and Akka (Scala/JVM). Everything is an actor — a lightweight process with a private state and a mailbox.

```
Actor receives messages sequentially, one at a time.
State is never shared — only messages cross actor boundaries.
Failures are handled by supervisors, not the actor itself.
```

- **What you share:** nothing. Actor state is private; messages are immutable.
- **Location transparency:** an actor reference works the same whether the actor is in the same process, on the same machine, or across a network. Erlang/OTP was designed for distributed telecom systems where this is load-bearing.
- **Fault tolerance via supervision:** actors are organized into a supervision hierarchy. When an actor crashes, its supervisor decides whether to restart it, restart its siblings, or escalate. Joe Armstrong's "let it crash" philosophy comes from this.
- **When the model shines:** distributed systems where you need soft real-time guarantees, high fault tolerance, and hot code upgrade. WhatsApp and Discord famously run at massive scale on Erlang and Elixir respectively.
- **When it doesn't:** latency-sensitive CPU-bound work (message passing overhead), problems where the natural decomposition isn't actors-with-mailboxes.

Akka has since backed off from pure Actor Model toward typed actors because untyped message handling is error-prone. The core insight — isolation, message passing, supervision — remains the durable contribution.

## 5. Software Transactional Memory (STM)

Treat memory updates like database transactions. Multiple threads speculatively modify shared state; the runtime validates at commit time and retries on conflict. Clojure's `ref`/`dosync` and Haskell's `STM` monad are the best-known implementations.

```
(dosync
  (alter account-a - 100)
  (alter account-b + 100))
```

- **What you share:** transactional references to immutable values.
- **Semantics:** like MVCC or pure functions — commit, abort, retry. The runtime guarantees atomicity of the `dosync` block.
- **Strengths:** composition is trivial. Unlike locks (where composing two locked operations can deadlock), composing two transactions just produces a bigger transaction.
- **Weaknesses:** performance. The bookkeeping of transactions is expensive. Contention amplifies: if many transactions conflict, the retry loop can dominate. STM has never found the mainstream despite decades of research.
- **Where it works:** Haskell's STM is excellent for coordinating a few shared mutable cells in functional code. Clojure's STM pairs well with persistent data structures (where retries are cheap). Almost nowhere else has it taken hold.

## Comparing the models

| Model                 | Share state?      | Composes? | Distributed?      | Typical bugs                        |
| --------------------- | ----------------- | --------- | ----------------- | ----------------------------------- |
| Single-threaded async | Yes (same thread) | OK        | No                | Blocked event loop, forgotten await |
| Shared-memory threads | Yes               | Poorly    | No                | Races, deadlocks, visibility bugs   |
| CSP                   | No                | Well      | Not natively      | Goroutine leaks, buffer deadlocks   |
| Actor Model           | No                | Well      | Yes (transparent) | Mailbox overflow, typing issues     |
| STM                   | Transactionally   | Well      | No                | Contention, retry storms            |

## A few practical observations

**Language often dictates model more than problem does.** Teams pick languages for many reasons (ecosystem, hiring, performance) and inherit the concurrency model as a side effect. Erlang forces actors; Go forces CSP; Java gives you threads. Choose the problem fit deliberately — otherwise you'll use whichever model your stack makes easiest, which isn't always right.

**Real systems mix models.** A typical production service might run a multi-threaded event loop (async + threads for CPU-bound work), talk to a database that uses STM internally, and communicate with sibling services via actor-style message queues (Kafka is structurally actor-model-adjacent). Understanding each model in isolation is preparation for working with the composition.

**The hardest concurrency bugs come from model mismatch.** Using shared-memory threading primitives inside an async runtime, or sharing mutable state across actor boundaries — these are where the worst production incidents hide. If you see a bug that only reproduces under load, check whether two parts of the system are assuming different concurrency models.

## See also

- [Skiplist](https://tianpan.co/notes/69-skiplist) — `ConcurrentSkipListMap` is a case study in shared-memory lock-free data structures.
- [Bloom Filter](https://tianpan.co/notes/68-bloom-filter) — concurrent Bloom filter implementations are a common systems-engineering interview topic.
- [How to scale a web service?](https://tianpan.co/notes/41-how-to-scale-a-web-service) — X-axis cloning assumes your concurrency model lets you run multiple instances without shared state.
