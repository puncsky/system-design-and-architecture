---
layout: post
title: "Designing a Load Balancer or Dropbox Bandaid"
date: 2019-10-19 15:21
comments: true
categories: system design
language: en
slides: false
abstract: Large-scale web services deal with high-volume traffic, but one host could only serve a limited amount of requests. There is usually a server farm to take the traffic altogether. How to route them so that each host could evenly receive the request?
references:
  - https://blogs.dropbox.com/tech/2019/09/enhancing-bandaid-load-balancing-at-dropbox-by-leveraging-real-time-backend-server-load-information/
  - https://medium.com/netflix-techblog/netflix-edge-load-balancing-695308b5548c
  - https://www.nginx.com/blog/nginx-power-of-two-choices-load-balancing-algorithm/#least_conn
---

## Requirements


Internet-scale web services deal with high-volume traffic from the whole world. However, one server could only serve a limited amount of requests at the same time. Consequently, there is usually a server farm or a large cluster of servers to undertake the traffic altogether. Here comes the question: how to route them so that each host could evenly receive and process the request? 

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571516030/web-guiguio/01-s_71d9a66b3d35f2559b6febf625b03c50d20a1b0c11818ddb19fbbadeafbd11d5_1567646267795_image.png)

Since there are many hops and layers of load balancers from the user to the server, specifically speaking, this time our design requirements are

* [designing an L7 Load Balancer inside a data center](https://guigu.io/notes/2018-07-23-load-balancer-types)
* leveraging real-time load information from the backend
* serving 10 m RPS, 10 T traffic per sec

> Note: If Service A depends on (or consumes) Service B, then A is downstream service of B, and B is upstream service of A.


## Challenges
Why is it hard to balance loads? The answer is that it is hard to collect accurate load distribution stats and act accordingly.

### Distributing-by-requests ≠ distributing-by-load

Random and round-robin distribute the traffic by requests. However, the actual load is not per request - some are heavy in CPU or thread utilization, while some are lightweight. 

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571519977/web-guiguio/round-robin_power-of-two-choices.png)

To be more accurate on the load, load balancers have to maintain local states of observed active request number, connection number, or request process latencies for each backend server. And based on them, we can use distribution algorithms like Least-connections, least-time, and Random N choices:

**Least-connections**: a request is passed to the server with the least number of active connections.

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571520022/web-guiguio/least-conn_power-of-two-choices.png)

**latency-based (least-time)**:  a request is passed to the server with the least average response time and least number of active connections, taking into account weights of servers.

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571520022/web-guiguio/least-conn_power-of-two-choices.png)

However, these two algorithms work well only with only one load balancer. If there are multiple ones, there might have **herd effect**. That is to say; all the load balancers notice that one service is momentarily faster, and then all send requests to that service.

**Random N choices** (where N=2 in most cases / a.k.a *Power of Two Choices*): pick two at random and chose the better option of the two, *avoiding the worse choice*.


### Distributed environments.

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571516504/web-guiguio/02-s_71d9a66b3d35f2559b6febf625b03c50d20a1b0c11818ddb19fbbadeafbd11d5_1567573729122_image.png)

Local LB is unaware of global downstream and upstream states, including

* upstream service loads
* upstream service may be super large, and thus it is hard to pick the right subset to cover with the load balancer
* downstream service loads
* the processing time of various requests are hard to predict
    
## Solutions
There are three options to collect load the stats accurately and then act accordingly:

* centralized & dynamic controller 
* distributed but with shared states
* piggybacking server-side information in response messages or active probing

Dropbox Bandaid team chose the third option because it fits into their existing *random N choices* approach well. 

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571519434/web-guiguio/03-s_36fd13246bc17faff0558a94f22b02b1467d2b44c17456e7ff5ae7d2f7c84c87_1567054697304_microservice2.png)

However, instead of using local states, like the original *random N choices* do,  they use real-time global information from the backend servers via the response headers.

**Server utilization**: Backend servers are configured with a max capacity and count the on-going requests, and then they have utilization percentage calculated ranging from 0.0 to 1.0.

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571521419/web-guiguio/04-s_71d9a66b3d35f2559b6febf625b03c50d20a1b0c11818ddb19fbbadeafbd11d5_1567652883718_image.png)

There are two problems to consider:

1. **Handling HTTP errors**: If a server fast fails requests, it attracts more traffic and fails more. 
2. **Stats decay**: If a server’s load is too high, no requests will be distributed there and hence the server gets stuck. They use a decay function of the inverted sigmoid curve to solve the problem.

## Results: requests are more balanced

![](https://res.cloudinary.com/dohtidfqh/image/upload/v1571523160/web-guiguio/06-s_71d9a66b3d35f2559b6febf625b03c50d20a1b0c11818ddb19fbbadeafbd11d5_1567642263885_image-e1568763671660.png)

