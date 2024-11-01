---
slug: 2018-07-23-load-balancer-types
id: 2018-07-23-load-balancer-types
layout: post
title: "负载均衡器类型"
date: 2018-07-23 11:54
comments: true
categories: 系统设计
language: cn
abstract: "通常，负载均衡器分为三类：DNS 轮询、网络负载均衡器和应用负载均衡器。DNS 轮询很少使用，因为它难以控制且响应不佳。网络负载均衡器具有更好的粒度，简单且响应迅速。"
references:
    - https://www.amazon.com/Practice-Cloud-System-Administration-Practices/dp/032194318X
    - https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-types.html
---

一般来说，负载均衡器分为三类：

- DNS 轮询（很少使用）：客户端获得一个随机顺序的 IP 地址列表。
    - 优点：易于实现且免费
    - 缺点：难以控制且响应不佳，因为 DNS 缓存需要时间过期
- 网络（L3/L4）负载均衡器：流量通过 IP 地址和端口进行路由。L3 是网络层（IP）。L4 是会话层（TCP）。
    - 优点：更好的粒度，简单，响应迅速
- 应用（L7）负载均衡器：流量根据 HTTP 协议中的内容进行路由。L7 是应用层（HTTP）。