---
layout: post
title: "如何构建大规模的网站服务?"
date: 2018-09-11 21:32
comments: true
categories: system design
language: zh-cn
abstract: 如何构建大规模的网站服务？一个字：拆。AKF扩展立方告诉了我们”拆”的三个纬度：水平扩展；业务拆分；数据分割。
references:
  - https://akfpartners.com/growth-blog/scale-cube
  - https://akfpartners.com/growth-blog/akf-scale-cube-ze-case-for-z-axis
---

==一个字：拆==

==AKF扩展立方==告诉了我们"拆"的三个纬度：


![AKF Scale Cube](/img/akf-scale-cube.gif)


1. ==水平扩展== 把很多无状态的服务器放在负载均衡器或者反向代理的后面，这样每个请求都能被其中任意一个服务器受理，就不会有单点故障了。
2. ==业务拆分== 典型的按照功能分的微服务，比如 auth service, user profile service, photo service, etc
3. ==数据分割== 分割出整套技术栈和数据存储专门给特定的一大组用户，比如优步有中国和美国的数据中心，每个数据中心内部有不同的 Pod 给不同的城市或地区。
