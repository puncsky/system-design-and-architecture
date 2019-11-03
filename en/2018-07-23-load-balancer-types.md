---
layout: post
title: "Load Balancer Types"
date: 2018-07-23 11:54
comments: true
categories: system design
language: en
references:
    - https://www.amazon.com/Practice-Cloud-System-Administration-Practices/dp/032194318X
    - https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-types.html
---

Generally speaking, load balancers fall into three categories:

- DNS Round Robin (rarely used): clients get a randomly-ordered list of IP addresses.
    - pros: easy to implement and free
    - cons: hard to control and not responsive, since DNS cache needs time to expire
- Network (L3/L4) Load Balancer: traffic is routed by IP address and ports.L3 is network layer (IP). L4 is session layer (TCP).
    - pros: better granularity, simple, responsive
- Application (L7) Load Balancer: traffic is routed by what is inside the HTTP protocol. L7 is application layer (HTTP).
