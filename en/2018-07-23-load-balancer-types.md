---
slug: 2018-07-23-load-balancer-types
id: 2018-07-23-load-balancer-types
title: "Load Balancer Types"
date: 2018-07-23 11:54
comments: true
tags: [system design, networking, infrastructure]
description: "Three categories of load balancer — DNS round robin, L3/L4 network load balancer, and L7 application load balancer. Notes on what each actually does at the packet level, which algorithms (round robin, least connections, consistent hashing) fit which use case, and where health checks and sticky sessions break."
references:
  - https://www.amazon.com/Practice-Cloud-System-Administration-Practices/dp/032194318X
  - https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-types.html
---

Load balancers fall into three categories based on which OSI layer they operate at. The choice isn't really "which LB is best"; it's "what does the traffic look like and what routing decisions do I need to make?"

## The three categories

### DNS round robin

The client resolves a hostname and receives a randomly-ordered list of IP addresses. It typically tries the first one and falls through on failure.

- **Pros:** Free, trivial to configure, no infrastructure to run.
- **Cons:** DNS caching at every layer (resolver, OS, browser) makes it impossible to react quickly to a failed host. Clients hold stale records for TTL minutes after you remove a host from rotation. No health awareness — DNS returns dead hosts until you update the record.
- **When to use:** Distributing across geographically separated clusters ("send EU users to eu.example.com"), or as a first hop in front of regional LBs. Almost never as the only layer.

### Network (L3/L4) load balancer

Routes traffic based on IP addresses and ports. Operates on TCP/UDP without inspecting payload.

- **L3** (network layer): IP-level routing. Rare as a pure L3 LB; most products that call themselves L3 are actually L3+L4.
- **L4** (transport layer): TCP/UDP session-level routing. Examples: AWS NLB, HAProxy in TCP mode, LVS, Cloudflare Spectrum.

**How it actually works:** most L4 LBs use one of two techniques. _Direct Server Return_ (DSR) rewrites the destination IP so the packet arrives at a backend, but the backend replies directly to the client, bypassing the LB — this handles massive throughput because the LB only sees one direction. _NAT mode_ rewrites both directions and the LB sees all traffic; simpler but throughput-bound.

- **Pros:** Enormous throughput (millions of connections per second). Very low latency (sub-millisecond overhead). No protocol-specific logic means it works for anything that runs over TCP — HTTP, Redis, Kafka, custom protocols.
- **Cons:** Can't make routing decisions based on HTTP headers, paths, or cookies. Health checks are limited to "is this TCP port accepting connections," which often passes even when the application is broken.
- **When to use:** Non-HTTP protocols, extreme-throughput HTTP where per-packet overhead matters, or as the first tier in front of L7 LBs.

### Application (L7) load balancer

Parses the application protocol — almost always HTTP/HTTPS — and routes based on what's in the request.

- **Examples:** AWS ALB, nginx, HAProxy in HTTP mode, Envoy, Traefik, Caddy, Kubernetes Ingress controllers.
- **Routing capabilities:** path prefix, Host header, cookies, headers, query strings, geo-IP, user agent.
- **Other L7 features:** TLS termination, HTTP/2 → HTTP/1.1 downgrading for backends, request/response header manipulation, compression, rate limiting, WAF integration, authentication/OAuth handoff.

**Pros:** Routing decisions with full request context. Semantic health checks (return `200` from `/healthz`). Observability — per-request logs, percentile latency per path, error rates by route. A/B testing and canary deployments are trivial.

**Cons:** More CPU per request (payload parsing, TLS). Higher latency (single-digit milliseconds rather than sub-ms). TCP-state handling gets complex with long-lived connections (WebSocket, HTTP/2 streams, gRPC).

**When to use:** Default choice for any HTTP traffic, unless you're hitting scale or protocol constraints that force L4.

## The load-balancing algorithms

Separate from layer choice is the _algorithm_ used to pick a backend. The common ones:

- **Round robin.** Send request N to backend N mod K. Simple, uniform, and wrong when backends have different capacities or request costs vary widely.
- **Least connections.** Send to the backend with the fewest in-flight connections. Better when request duration varies (long polls, streaming).
- **Least response time.** Blend of least connections and observed latency. Better under mixed load.
- **Weighted round robin / weighted least connections.** Backends have assigned weights based on capacity. Necessary in heterogeneous fleets.
- **Consistent hashing.** Request key → stable backend. Critical for cache-affinity systems (Memcached, CDN origin), session affinity, and sharded data stores. Tolerates backend additions/removals without a full rehash.
- **Power of two choices.** Pick two random backends, send to the less loaded one. Tight bounds on max load, no central coordination, and resilient to stale load info. Widely used in modern service meshes.
- **Random.** Uniform random pick. Performs surprisingly well at high RPS and is trivially load-information-free.

Choice heuristic: round robin for homogeneous stateless, least connections for variable request duration, consistent hashing for anything with cache or state affinity, power-of-two for large dynamic fleets.

## Health checks — where LBs silently go wrong

Health checks are the least glamorous part of LB configuration and the most common source of incidents.

- **Passive vs active:** active checks hit `/healthz` on a schedule; passive checks watch production traffic for error rates. Active-only misses transient issues; passive-only reacts too slowly. Both together is the right default.
- **Check the dependency chain.** A healthz endpoint that returns 200 without verifying the database connection is worse than no health check — it lets broken instances stay in rotation confidently.
- **Don't check too aggressively.** 100ms health-check intervals on 1000 backends = 10K req/s of health-check traffic. At scale, health checks can be a significant fraction of backend load.
- **Separate liveness from readiness.** Kubernetes distinguishes these explicitly; other systems often conflate them. Liveness = "is the process alive?" Readiness = "is it ready to serve traffic?" Conflating leads to restart loops during warmup.

## Sticky sessions (affinity) — mostly an anti-pattern

Session affinity routes a given client to the same backend for the duration of a "session," usually via a cookie or source-IP hash.

- **The usual reason given:** the backend holds in-memory session state that would be lost on failover.
- **The real problem:** sticky sessions mean any backend failure loses _every_ in-flight user on that host, and load becomes uneven as sessions accumulate on long-running hosts.

The correct fix is usually to make backends stateless (session state in Redis or a JWT). Sticky sessions are acceptable for short-duration stickiness (a multi-step checkout flow) but a smell when applied at session scale.

## TLS termination

Where to terminate TLS affects security posture and cost:

- **At the L7 LB (most common):** LB decrypts, routes based on request, re-encrypts to backend or sends plaintext over a private network. Easiest to operate; backends don't need certs.
- **At the L4 LB with pass-through:** LB doesn't see plaintext; backend handles TLS. Necessary when the LB shouldn't see decrypted content (e.g. end-to-end encryption), or when you need SNI-based L4 routing.
- **Terminated twice (edge + internal):** edge LB terminates, internal LB re-terminates. Expensive but sometimes required by compliance.

For most web services, terminate once at the L7 LB and run plaintext internally on a trusted network. The double-termination pattern is a compliance artifact, not a security improvement in most cases.

## Real-world stacks

- **Small SaaS:** AWS ALB → EC2/ECS. One tier, L7 only.
- **Mid-scale SaaS:** AWS NLB → ALB → backends. NLB handles extreme-volume TCP; ALB does request routing.
- **Hyperscale consumer:** BGP Anycast → edge L4 LB → regional L7 LB → service mesh (Envoy sidecar). Four tiers because each solves a different problem.
- **Kubernetes:** cloud LB (L4) → Ingress controller (L7, nginx/Traefik/Envoy) → service (kube-proxy, L4) → pod. Four layers of LB are normal inside K8s.

## See also

- [How to scale a web service?](https://tianpan.co/notes/41-how-to-scale-a-web-service) — load balancers are the front door of X-axis scaling.
- [Concurrency Models](https://tianpan.co/notes/181-concurrency-models) — backend concurrency choice affects which LB algorithm fits best.
