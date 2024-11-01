---
slug: 41-how-to-scale-a-web-service
id: 41-how-to-scale-a-web-service
title: "如何扩展网络服务？"
date: 2018-09-11 21:32
comments: true
tags: [系统设计]
references:
  - https://akfpartners.com/growth-blog/scale-cube
  - https://akfpartners.com/growth-blog/akf-scale-cube-ze-case-for-z-axis
---

AKF 规模立方体将扩展过程可视化为三个维度…

![AKF 规模立方体](/img/akf-scale-cube.gif)

1. ==水平复制== 和克隆 (X 轴)。在负载均衡器或反向代理后面拥有一组相同且最好是无状态的实例。因此，每个请求都可以由这些主机中的任何一个来处理，并且不会有单点故障。
2. ==功能分解== 和分段 - 微服务 (Y 轴)。例如，身份验证服务、用户资料服务、照片服务等。
3. ==水平数据分区== - 分片 (Z 轴)。将整个堆栈复制到不同的“集群”。每个集群可以针对特定的大用户群。例如，Uber 在中国和美国都有数据中心。每个数据中心可能会有不同区域的“集群”。

想要一个例子吗？去看看 [Facebook 如何扩展其社交图谱数据存储](https://tianpan.co/notes/49-facebook-tao)。