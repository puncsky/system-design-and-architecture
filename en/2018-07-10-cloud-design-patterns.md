---
layout: post
title: "Cloud Design Patterns"
date: 2018-07-10 11:16
comments: true
categories: design patterns, system design
language: en
references:
  - https://docs.microsoft.com/en-us/azure/architecture/patterns/
---

## Availability patterns
  - Health Endpoint Monitoring: Implement functional checks in an application that external tools can access through exposed endpoints at regular intervals.
  - Queue-Based Load Leveling: Use a queue that acts as a buffer between a task and a service that it invokes in order to smooth intermittent heavy loads.
  - Throttling: Control the consumption of resources used by an instance of an application, an individual tenant, or an entire service.



## Data Management patterns
  - Cache-Aside: Load data on demand into a cache from a data store
  - Command and Query Responsibility Segregation: Segregate operations that read data from operations that update data by using separate interfaces.
  - Event Sourcing: Use an append-only store to record the full series of events that describe actions taken on data in a domain.
  - Index Table: Create indexes over the fields in data stores that are frequently referenced by queries.
  - Materialized View: Generate prepopulated views over the data in one or more data stores when the data isn't ideally formatted for required query operations.
  - Sharding: Divide a data store into a set of horizontal partitions or shards.
  - Static Content Hosting: Deploy static content to a cloud-based storage service that can deliver them directly to the client.



## Security Patterns
  - Federated Identity: Delegate authentication to an external identity provider.
  - Gatekeeper: Protect applications and services by using a dedicated host instance that acts as a broker between clients and the application or service, validates and sanitizes requests, and passes requests and data between them.
  - Valet Key: Use a token or key that provides clients with restricted direct access to a specific resource or service.
