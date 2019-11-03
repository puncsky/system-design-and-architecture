---
layout: post
title: "Public API Choices"
date: 2018-10-04 01:38
comments: true
categories: system design
language: en
---

In summary, to choose a tool for the public API, API gateway, or BFF (Backend For Frontend) gateway, I prefer GraphQL for its features like tailing results, batching nested queries, performance tracing, and explicit caching.

||JSON RPC|GraphQL|REST|gRPC|
|--- |--- |--- |--- |--- |
|Usecases|Etherum|Github V2, Airbnb, Facebook BFF / API Gateway|Swagger|High performance, Google, internal endpoints|
|Single Endpoint|✅|✅|❌|✅|
|Type System|✅ as weak as JSON <br/> No uint64|✅ <br/> No uint64|✅ w/ Swagger <br/> No uint64|✅  <br/>has uint64|
|Tailored Results|❌|✅|❌|❌|
|Batch nested queries|❌|✅|❌|❌|
|Versioning|❌|Schema Extension|Yes, w/ v1/v2 route s|Field Numbers in protobuf|
|Error Handling|Structured|Structured|HTTP Status Code|Structured|
|Cross-platform|✅|✅|✅|✅|
|Playground UI|❌|GraphQL Bin|Swagger|❌|
|Performance tracing|?|Apollo plugin|?|?|
|caching|No or HTTP cache control|Apollo plugin|HTTP cache control|Native support not yet.  but still yes w/ HTTP cache control|
|Problem|Lack of community support and toolchainBarrister IDL|42.51 kb client-side bundle size|Unstructured with multiple endpoints. awful portability.|Grpc-web dev in progress140kb JS bundle. Compatibility issues: not all places support HTTP2 and grpc dependencies|
