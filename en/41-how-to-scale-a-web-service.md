---
layout: post
title: "How to scale a web service?"
date: 2018-09-11 21:32
comments: true
categories: system design
language: en
references:
  - https://akfpartners.com/growth-blog/scale-cube
  - https://akfpartners.com/growth-blog/akf-scale-cube-ze-case-for-z-axis
---

AKF scale cube visualizes the scaling process into three dimensions…


![AKF Scale Cube](/img/akf-scale-cube.gif)


1. ==Horizontal Duplication== and Cloning (X-Axis). Having a farm of identical and preferably stateless instances behind a load balancer or reverse proxy. Therefore, every request can be served by any of those hosts and there will be no single point of failure.
2. ==Functional Decomposition== and Segmentation - Microservices  (Y-Axis). e.g. auth service, user profile service, photo service, etc
3. ==Horizontal Data Partitioning== - Shards (Z-Axis).  Replicate the whole stack to different “pods”.  Each pod can target a specific large group of users. For example, Uber had China and US data centers. Each datacenter might have different “pods” for different regions.

Want an example? Go to see [how Facebook scale its social graph data store](/notes/49-facebook-tao).
