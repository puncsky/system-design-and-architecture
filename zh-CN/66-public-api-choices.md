---
slug: 66-public-api-choices
id: 66-public-api-choices
layout: post
title: "公共 API 选择"
date: 2018-10-04 01:38
comments: true
categories: 系统设计
description: 有几种工具可用于公共 API、API 网关或前端后端网关。GraphQL 以其诸如尾随结果、批处理嵌套查询、性能追踪和显式缓存等功能而脱颖而出。
---

总之，在选择公共 API、API 网关或 BFF（前端后端）网关的工具时，我更喜欢 GraphQL，因为它具有尾随结果、批处理嵌套查询、性能追踪和显式缓存等功能。

||JSON RPC|GraphQL|REST|gRPC|
|--- |--- |--- |--- |--- |
|用例|以太坊|Github V2、Airbnb、Facebook BFF / API 网关|Swagger|高性能、谷歌、内部端点|
|单一端点|✅|✅|❌|✅|
|类型系统|✅，与 JSON 一样弱 <br/> 无 uint64|✅ <br/> 无 uint64|✅ w/ Swagger <br/> 无 uint64|✅  <br/>有 uint64|
|定制结果|❌|✅|❌|❌|
|批处理嵌套查询|❌|✅|❌|❌|
|版本控制|❌|模式扩展|是，使用 v1/v2 路由|protobuf 中的字段编号|
|错误处理|结构化|结构化|HTTP 状态码|结构化|
|跨平台|✅|✅|✅|✅|
|游乐场 UI|❌|GraphQL Bin|Swagger|❌|
|性能追踪|?|Apollo 插件|?|?|
|缓存|无或 HTTP 缓存控制|Apollo 插件|HTTP 缓存控制|尚未原生支持，但仍可使用 HTTP 缓存控制|
|问题|缺乏社区支持和工具链 Barrister IDL|42.51 kb 客户端包大小|多个端点的非结构化，便携性差。|Grpc-web 开发进行中，140kb JS 包。兼容性问题：并非所有地方都支持 HTTP2 和 grpc 依赖|