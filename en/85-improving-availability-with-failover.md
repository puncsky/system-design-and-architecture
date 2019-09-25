---
layout: post
title: "Improving availability with failover"
date: 2018-10-26 12:02
comments: true
categories: system design
language: en
references:
  - https://www.ibm.com/developerworks/community/blogs/RohitShetty/entry/high_availability_cold_warm_hot
---

Cold Standby: Use heartbeat or metrics/alerts to track failure. Provision new standby nodes when a failure occurs. Only suitable for stateless services.

Hot Standby: Keep two active systems undertaking the same role. Data is mirrored in near real time, and both systems will have identical data.

Warm Standby: Keep two active systems but the secondary one does not take traffic unless the failure occurs.

Checkpointing (or like Redis snapshot): Use write-ahead log (WAL) to record requests before processing. Standby node recovers from the log during the failover.

* cons
  * time-consuming for large logs
  * lose data since the last checkpoint
* usercase: Storm, WhillWheel, Samza

Active-active (or all active): Keep two active systems behind a load balancer. Both of them take in parallel. Data replication is bi-directional.
